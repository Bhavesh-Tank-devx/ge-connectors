# ADR-001: Data Connector Architecture for RazorpayX Payroll Access via Gemini Enterprise

**Status:** Proposed (options presented, decision pending)
**Date:** 2026-09-21
**Deciders:** Bhavesh Tank; reopens the architecture previously marked "locked" in session S613 (2026-09-21, earlier same day)

---

## Context

We're building a POC that lets end users ask a Gemini Enterprise assistant about their own RazorpayX Payroll data (payslips, etc.) and demonstrates that architecture to a wider audience alongside a live demo.

Two constraints make this harder than a typical connector:

1. **RazorpayX Payroll's API has no per-user auth model.** It's authenticated with a single org-level API key and addressed by employee ID — there is no OAuth scoping, no per-employee token, nothing Razorpay itself can use to prevent the API key from being used to fetch *any* employee's data. Access control must be enforced entirely by whatever sits between the end user and Razorpay.
2. **The audience for the demo will specifically probe identity/authorization**, since "can User A see User B's payslip" is the obvious adversarial test of any payroll integration. The architecture has to make that failure mode structurally impossible, not just unlikely.

A design was provisionally selected earlier the same day (session S613): an ADK agent on Agent Runtime, with the tool reading the end user's identity from `tool_context.session.user_id`, on the assumption that this is a verified, platform-asserted value Gemini Enterprise injects automatically.

**That assumption did not hold up under direct verification.** Deeper research this session found:
- One official Google doc states ADK agents "receive the user's email address from Gemini Enterprise" — under a *personalization* heading, with no stated wire mechanism.
- A Google ADK engineer, on the `google/adk-python` GitHub discussions, states the opposite as the default: *"By default, Gemini Enterprise authenticates to Agent Engine using its own service identity and doesn't pass any information about the end user to the agent."*
- ADK's own docs describe the session `user_id` as **caller-supplied**, not verified ("Choose your own user ID").

Whichever claim is more accurate, **no official source claims this value is cryptographically verifiable by agent code**. Building the payroll access-control boundary on it was the actual point of failure in the original design, not merely a caveat — and it's why this ADR exists.

Also relevant: a first pass at this research (recorded as project memory before this session) assumed federated (live, no-copy) connector access was only available for a small Google-curated allowlist of enterprise systems, and that this ruled out any live/federated custom path for a source like Razorpay. **This turned out to be backwards.** Federation is the broadly-available mode in the current (Sept 2026) Gemini Enterprise connector catalog — for several major connectors (Jira Data Center, Salesforce, Confluence Data Center) *ingestion* is the more gated, allowlist-only mode, not federation. And Google ships a first-class federated path for arbitrary custom sources: **Custom MCP Server**, which was not previously considered.

### Environment assumptions (apply to every option below unless noted)

- GCP project with Gemini Enterprise (formerly Agentspace) provisioned, org policy admin access available (needed to allow custom data sources).
- End users authenticate to Gemini Enterprise via a real corporate identity (Google Workspace, Cloud Identity, or Workforce Identity Federation to an external IdP such as Entra ID/Okta) — i.e., every employee has a real, federation-authenticatable identity even though Razorpay itself has no concept of one.
- A mapping table exists or can be built: `corporate identity ↔ Razorpay employee_id`.
- Razorpay access is exclusively via the org-level API key; no Razorpay-side auth changes are possible or assumed.
- This is a POC/demo, not a production rollout — but the architecture should be defensible as a real design, since it will be presented and scrutinized, not just run once.

---

## Background: connector architecture patterns (general)

Before the Gemini-Enterprise-specific analysis, the general landscape this maps onto:

|  | **Ingested / indexed** | **Federated / live** |
|---|---|---|
| **Native (vendor-built)** | Vendor ships and maintains the connector (Salesforce AppExchange, BigQuery Data Transfer Service, GE's prebuilt Jira/SharePoint/Slack connectors). Maintenance burden sits with the vendor. | Vendor's connector queries the source live at request time (GE's connectors running in "federated search" mode; conceptually similar to Trino/Presto or Denodo doing live cross-source SQL). |
| **Custom (you build)** | You build a Fetch → Transform → Sync pipeline into a store you control (Airbyte CDK, Singer taps, GE's "Custom Connector" feature). You own maintenance: schema drift, rate limits, auth changes. | You expose a live adapter the platform calls at query/tool-call time (GE's "Custom MCP Server", A2A, an ADK tool). Functionally federated, architecturally closer to "agent/tool calling" than to a classic connector. |

**Core tradeoff, either axis:** ingestion buys query speed and reduced load on the source, at the cost of freshness lag and duplicated storage/governance. Federation buys always-fresh, no-duplication data, at the cost of per-query latency and load on the live source.

**Patterns that don't fit the 2×2:** iPaaS/unified-API layers (Truto, Merge.dev, Nango) normalize a messy source before any connector touches it; hybrid designs index metadata/summaries while federating the sensitive detail record.

---

## Decision

**Not yet made** — this document lays out the credible options so the choice can be made deliberately, per your instruction to see the full comparison before committing.

Two options are recommended as leading candidates (Option A and Option B below); the others are documented for completeness and to show why they were set aside.

---

## Options Considered

### Ruled out before detailed comparison

**Native connector catalog** — Razorpay is not, and given its niche/regional nature is unlikely to become, one of Gemini Enterprise's ~16 GA or ~100 Public Preview named connectors. There is no "register any REST API" option inside that catalog. Not viable.

**iPaaS / unified-API layer (Truto, Merge.dev, Nango)** — verified directly: no Google Cloud Marketplace listing, partner directory entry, or documentation page mentions any of these as recommended, certified, or integrated with Gemini Enterprise. It would be a purely unofficial layer sitting in front of whichever option below you pick — added complexity with no platform backing. Not worth it for a POC; worth reconsidering only if RazorpayX's API turns out to need heavier normalization than expected.

---

### Option A: Custom Connector — Ingestion + ACL / Identity Mapping Store

A scheduled job pulls payslip data from RazorpayX (using the org key) and writes it into a Gemini Enterprise data store as Documents, each tagged with `acl_info.readers[].principals[].externalEntityId = <razorpay_employee_id>`. A one-time **Identity Mapping Store** load maps `razorpay_employee_id → corporate_email`. Gemini Enterprise resolves the mapping and enforces the ACL **server-side, natively, at query time** — "the same query can return different results for two users" per Google's own documentation.

| Dimension | Assessment |
|---|---|
| Complexity | Medium — mapping store setup is one-time; ingestion pipeline is a scheduled Cloud Run/Function job you own |
| Identity trust | **Strong** — enforcement is Google's platform code against a real authenticated principal, not a claim your code has to trust |
| Freshness | Bounded by your sync cadence (you control it; no managed scheduler for raw Document API calls) |
| Data residency | Full copy of payroll data lives in Google's index — a real consideration for payroll-sensitivity data even in a POC |
| Reversibility | **Low** — ACL mode must be chosen at data-store *creation* and is documented as not retrofittable |

**Pros:**
- The only option where per-user isolation is *provably* enforced by the platform, not by trusting an identity signal your code received.
- Straightforward to demo: show the same query from two different logged-in users producing different results, with no code-level identity check to interrogate.
- No dependency on Pre-GA features or org-policy overrides.

**Cons:**
- Payroll data ends up duplicated into Google's managed index — harder to defend as "least privilege" even if access is controlled.
- Not live — a payslip change on Razorpay's side isn't visible until the next sync.
- ACL-mode-at-creation is an unusually stiff constraint to get right on the first try.

**Assumed environment:** willing to stand up a scheduled sync job (Cloud Scheduler + Cloud Run/Functions) and accept storing a copy of payroll data in GCP; fine with batch freshness for a demo.

---

### Option B: Custom MCP Server data store (federated) — recommended

You host an MCP-compliant server (e.g. on Cloud Run) and register it as a **Custom MCP Server data store** in Gemini Enterprise. Verified directly against the docs: Gemini Enterprise forwards the signed-in end user's own OAuth token intact, via the `Authorization` header, to your server on every call (a separate `X-Serverless-Authorization` header authenticates the Gemini Enterprise service agent itself). Your server validates that token, maps the identity to a `razorpay_employee_id`, calls Razorpay with the org key, filters server-side, and returns live data. Nothing is stored in Google's index.

| Dimension | Assessment |
|---|---|
| Complexity | Medium-high — you're building and hosting a real MCP server with its own OAuth validation logic |
| Identity trust | **Strong** — the token forwarded is the user's own, independently validated by your code (not a platform claim you have to trust blind) |
| Freshness | Live — every query hits Razorpay directly |
| Data residency | Nothing duplicated — Razorpay stays the system of record |
| Gating | Blocked by default; requires an org-policy override to allow the `custom_mcp` data source |

**Pros:**
- Best architecture story for a presentation: live data, no duplication, and a security model that matches the MCP spec's own guidance almost exactly — *"The MCP server MUST NOT pass through the token it received from the MCP client [to upstream APIs]"* — i.e., validate the user's token, then independently call Razorpay with the org key, never forward anything to Razorpay.
- No Pre-GA risk (unlike A2A).
- Demonstrates the more interesting and more current Gemini Enterprise capability (Custom MCP Server is new enough that most audiences won't have seen it used this way).

**Cons:**
- Requires you to build and operate a small stateful service, including its own OAuth/OIDC validation — more moving parts than a scheduled ingestion job.
- Needs an org-policy change before it will even register — a step to plan for, not just a config toggle in the app itself.
- Live calls to Razorpay on every query — need to be mindful of Razorpay-side rate limits under demo load (not currently characterized).

**Assumed environment:** comfortable standing up and hosting a small server (Cloud Run is the natural fit given the header-forwarding default), and able to get an org-policy override applied.

---

### Option C: ADK agent on Agent Runtime, with the identity gap patched

Keep the originally-locked shape (ADK agent, registered via Agent Registry, custom tool calling Razorpay), but stop trusting `tool_context.session.user_id` for authorization. Instead, the tool independently runs its own OIDC flow (ADK's `AuthConfig`/`request_credential()` machinery, the same mechanism Gemini Enterprise's own "Agent Identity" 3-legged OAuth manager uses) to obtain a verified identity claim, before doing the employee_id mapping and Razorpay call.

Note: standard 3-legged OAuth delegation (Agent Identity) is **categorically inapplicable to Razorpay itself**, since it requires the third party to run an OAuth authorization server — Razorpay doesn't. The OIDC verification step here has to terminate at your own identity provider (Workspace/Entra/Okta), not at Razorpay.

| Dimension | Assessment |
|---|---|
| Complexity | Medium — reuses the already-designed ADK shape, adds an explicit OIDC verification step in the tool |
| Identity trust | Strong, *if* implemented correctly — but now depends on your own OIDC code being right, since the platform's automatic signal is exactly what we just found reason not to trust |
| Freshness | Live |
| Rework cost | Partial — most of the already-built ADK agent scaffold survives; the tool's identity-handling logic needs to change |

**Pros:**
- Preserves most of the work already done on the locked design.
- Live data, familiar ADK development model.

**Cons:**
- The thing that made this attractive originally (automatic, zero-friction identity from the platform) is gone — you're now building the same kind of manual identity verification Option B gets more cleanly, but inside an agent framework not purpose-built for it.
- Harder to defend in a presentation: "we didn't trust the platform's own identity signal, so we added our own OIDC check" invites the follow-up question of why not use the connector type built for exactly this.

**Assumed environment:** same as Option B in terms of needing your own OIDC verification code, but layered inside ADK rather than a standalone MCP server.

---

### Option D: A2A agent

Register an A2A agent with an OAuth2/OIDC security scheme in its AgentCard. Verified directly: Gemini Enterprise "acquires an OAuth 2.0 access token or ID token on behalf of the signed-in end user after they grant consent, and sends it in the standard Authorization header" — mechanically very close to Option B.

| Dimension | Assessment |
|---|---|
| Complexity | Medium — similar shape to Option B |
| Identity trust | Strong — confirmed OAuth/OIDC forwarding, same pattern as Option B |
| Maturity | **Pre-GA** — the registration page carries an explicit Pre-GA Offerings Terms notice |

**Pros:** same identity-trust strength as Option B, standards-based protocol.
**Cons:** explicit Pre-GA status is a real risk for anything described as "architecture" rather than "experiment" — not recommended to build the flagship demo on a feature Google itself flags as limited-support.

**Assumed environment:** same as Option B; only worth it over Option B if A2A interoperability with other agents is itself a goal of the demo.

---

## Trade-off Analysis

The real fork is **Option A (ingestion) vs. Option B (federated MCP)** — both give provable, platform- or protocol-backed identity enforcement, which is the property that actually matters here. Options C and D are variations that either give up the clean identity story (C) or add unnecessary maturity risk (D) without adding anything Option B doesn't already have.

- Choose **Option A** if: the demo audience will value "the platform itself enforces this, full stop" over live data, or if a scheduled batch job is simply less to build/operate under a deadline than a standalone server.
- Choose **Option B** if: "live data, nothing duplicated, current best-practice pattern" is the story you want to tell, and you're comfortable standing up and hosting a small MCP server plus getting an org-policy override.

Given the audience will likely probe the cross-user case directly, **either A or B is defensible; C and D are not recommended** — C reintroduces exactly the trust problem this ADR exists to fix, and D adds Pre-GA risk for no identity-strength benefit over B.

## Consequences

- Whichever of A/B is chosen, the two test scenarios already specified in S613 still apply: same-user payslip retrieval (returns data) and cross-user request (declines explicitly, no Razorpay call made for A; no successful identity-to-employee_id mapping for B).
- Choosing B means an org-policy change is a dependency to sequence early — don't discover the `custom_mcp` gate the day before the demo.
- Choosing A means the data-store ACL-mode decision has to be right the first time (not retrofittable) — build it correctly from the start rather than iterating.
- Project memory (S613, obs 4547–4550) should be updated once a decision is made — the current entries reflect the superseded assumption.

## Action Items

1. [ ] Decide between Option A and Option B (or confirm neither C nor D)
2. [ ] If B: request the `custom_mcp` org-policy override early
3. [ ] If A: confirm ACL-mode data-store creation parameters before first ingestion run
4. [ ] Build the chosen path's identity-mapping table (`razorpay_employee_id ↔ corporate identity`)
5. [ ] Implement the two test scenarios (same-user success, cross-user decline) as scripted demo steps
6. [ ] Update project memory to replace the superseded S613 architecture decision
7. [ ] (Optional, strengthens the presentation) Stand up a second, throwaway demo of a *native* connector (e.g. Google Drive) in federated mode, to make the native-vs-custom and ingestion-vs-federated contrast concrete rather than only discussed
