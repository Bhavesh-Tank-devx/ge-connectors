import os

native_connectors_content = """# Native and Managed Connectors in Gemini Enterprise

## 1. Scope
This document covers the landscape of native, Google-managed connectors in Gemini Enterprise (also known as Vertex AI Agent Builder / Discovery Engine). It focuses on pre-built integrations with third-party and Google Cloud sources, examining their supported modes (ingestion vs. federation), authentication, and current product availability.

## 2. Terminology
- **Data Store / Managed Data Source**: The unified repository where Gemini Enterprise ingests, chunks, and indexes data for semantic search.
- **DataConnector Resource**: The underlying API resource (`projects/.../dataConnector`) representing the connection to an external system.
- **Ingestion Mode (`DATA_INGESTION`)**: The connector crawls and copies data from the source into the Data Store index on a schedule.
- **Federated Mode (`FEDERATED`)**: The connector queries the source in real-time without indexing.
- **EUA (End User Authentication)**: Enforcing query-time permissions by mapping the user's Google Identity to the third-party system.

## 3. Current Connector Landscape
Gemini Enterprise provides native connectors to both Google ecosystem products and external enterprise applications. These connectors automate the extraction, chunking, and embedding processes required for Retrieval-Augmented Generation (RAG). 

## 4. Connector Categories
- **Google Cloud/Workspace**: GCS, BigQuery, Google Drive, Gmail, Calendar, Chat, Sites.
- **Third-Party Enterprise (GA)**: Box, Confluence (Cloud & DC), Dropbox, GitHub, HubSpot, Jira (Cloud & DC), Microsoft Entra ID, Microsoft Outlook, Microsoft Teams, Supabase.
- **Third-Party Enterprise (Preview)**: Salesforce (Rolling Out), Monday.com.

## 5. Supported Capabilities/Modes
While the API exposes `ConnectorMode` enums for `DATA_INGESTION`, `ACTIONS`, and `END_USER_AUTHENTICATION`, the practical reality of native data connectors is heavily biased toward ingestion. 
- **Platform Capability vs Customer Configurable**: The API exposes `FEDERATED` and `ACTIONS` enums, but for native connectors, customers can generally only configure `DATA_INGESTION` via the UI.
- **Ingestion** is the default for native out-of-the-box data stores.
- **Federation** (real-time) via native data stores is less common than ingestion; real-time federation is typically handled via Custom MCP or Vertex AI Extensions rather than "Native Connectors".

## 6. Connector-Specific Capability Matrix
| Connector | Mode | Capabilities | Auth Pattern | Status |
|---|---|---|---|---|
| **Jira (Cloud/DC)** | Ingestion | Search | Google ID, OIDC/SAML | GA |
| **Salesforce** | Ingestion | Search | Google ID, OIDC/SAML | Preview (Rolling out) |
| **Confluence** | Ingestion | Search | Google ID, OIDC/SAML | GA |
| **SharePoint** | Ingestion | Search | Entra ID, Google ID | GA |
| **Google Drive** | Ingestion | Search | Workspace IAM | GA |
| **MS OneDrive/Outlook** | Federation/Action | Actions (Preview) | Entra ID | Preview |

## 7. Authentication Patterns
- **Google Identity (Recommended)**: Best for Google Workspace sources.
- **Workforce Identity Federation (OIDC/SAML 2.0)**: Used to map Google identities to third-party identities (e.g., Entra ID, Salesforce). This ensures that ingested documents retain their Access Control Lists (ACLs) and are filtered at query time based on the querying user's mapped identity.

## 8. Data-Access Patterns
- **Sync/Polling**: Native connectors pull data from APIs on schedules (via `StartConnectorRun` in the API).
- **High-Latency**: [UNSUPPORTED COMMUNITY REPORT] Initial research claimed sync triggers introduce data latency making high-frequency metrics outdated. *Audit note: Requires exact community URL and hands-on validation to confirm delta-sync delays.*

## 9. Search vs Action Capabilities
Native Data Connectors are overwhelmingly **Search only** (read-only). To perform actions/mutations, developers must use separate components: Vertex AI Extensions, Agent Tools, or Custom MCP servers. (Exception: Preview actions for Microsoft Data Stores).

## 10. GA/Preview Status
- **GA**: Major Workspace and third-party read-only connectors (Jira, Confluence, GitHub).
- **Public Preview**: Custom MCP Servers (as of July 2026), Microsoft Data Store Actions.

## 11. Important Connector-Specific Differences
Google Workspace connectors (Drive, Gmail) are heavily optimized and deeply integrated. Third-party connectors require significantly more complex setup, such as configuring multi-tenant applications and OAuth secrets in external IDPs (e.g., Entra ID) via the `GetConnectorSecret` API.

## 12. Known Limitations
- **API Configurability**: Do not infer that UI presence implies full arbitrary API configurability for all types. `ConnectorType` enums like `THIRD_PARTY_FEDERATED` exist but are heavily constrained by platform UI support and are often output-only.
- **Federated vs RAG**: Federated queries are distinct from standard semantic indexing; they rely on the external system's search capabilities.

## 13. Community-Reported Practical Issues
*(Note: These claims were downgraded during the evidence audit due to vague sourcing. They require exact URLs and hands-on validation.)*
- **Token Injection**: [NEEDS HANDS-ON VALIDATION] Agents reportedly fail to automatically pick up authorization tokens, requiring manual injection in tool calls. 
- **Environment Drift**: [UNSUPPORTED] Behavioral discrepancies between local testing (Playgrounds) and production (Agent Engine).
- **Folder-Level ACLs**: [UNSUPPORTED] Granular access control, such as folder-level scoping in Google Drive, has reportedly been restricted.
- **Overzealous Guardrails**: [UNSUPPORTED] Native safety filters occasionally block harmless connector queries.

## 14. Evidence Table
See `EVIDENCE_INDEX.md` for the full traceability matrix.

## 15. Conflicting Evidence (Razorpay ADR Audit)
This research explicitly addresses claims made in `docs/ADR-001-razorpay-connector-architecture.md`:

- **ADR Claim:** "Federation is the broadly-available mode... for Jira, Salesforce, Confluence, ingestion is the more gated, allowlist-only mode."
  - **Verdict:** **CONTRADICTED**. The Connector Catalog and Official Docs researchers confirmed that native third-party connectors (Jira, Salesforce, Confluence) default to **Ingestion (Indexing)**. Native live federation for these systems requires separate Extensions or MCPs.
- **ADR Claim:** "Custom MCP Server data store (federated)" is a viable production path.
  - **Verdict:** **WEAKENED/CAVEAT**. Release Status research confirms Custom MCP is in **Public Preview** (July 2026), meaning it should not be treated as a fully GA platform capability.

## 16. Open Questions
- What specific error boundaries trigger the "unreadable document errors" during large-scale Drive/OneDrive syncing reported by the community?
- Are the token injection issues reported by the community applicable to Custom MCPs, or only to ADK agents?
- How is the `THIRD_PARTY_FEDERATED` connector type exposed in the API practically configured by a customer if no UI exists for it?
- If Custom MCP is only Public Preview, are there hidden quota/SLA limits that would fail our Razorpay demo under load?
- [AUDIT ADDITION]: Exact URLs for GitHub/Reddit community claims must be found to upgrade them from UNSUPPORTED.
"""

with open("research/native_connectors.md", "w") as f:
    f.write(native_connectors_content)


evidence_index_content = """# Evidence Index

This is the central index of claims and their supporting sources for the Gemini Enterprise Connector POC.

| Claim ID | Claim Summary | Source URL | Relevant Section | Classification (Fact/Inference/Community) | Confidence Level | Date/Status |
|----------|---------------|------------|------------------|-------------------------------------------|------------------|-------------|
| EVI-001  | Custom MCP Server forwards the signed-in end user's OAuth token in `Authorization` header and service agent in `X-Serverless-Authorization`. | TBD | TBD | TO BE VERIFIED | LOW (from ADR) | TBD |
| EVI-002  | Gemini Enterprise ACL mode must be chosen at data-store creation and is not retrofittable. | TBD | TBD | TO BE VERIFIED | LOW (from ADR) | TBD |
| EVI-003  | A2A agent registration acquires OAuth 2.0 access token on behalf of the signed-in end user after consent. | TBD | TBD | TO BE VERIFIED | LOW (from ADR) | TBD |
| EVI-004  | A2A agent registration is currently in Pre-GA / limited support. | TBD | TBD | TO BE VERIFIED | LOW (from ADR) | TBD |
| EVI-005  | ADK agents do not receive cryptographically verifiable end-user identity by default. | TBD | TBD | TO BE VERIFIED | LOW (from ADR) | TBD |
| EVI-006  | Native connectors for Jira, Confluence, SharePoint default to Ingestion, not Federation. | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources | Capability Matrix | FACT | HIGH | Sept 2026 |
| EVI-007  | Native Connectors are overwhelmingly Search-only (read-only); mutations require Extensions/MCP. | https://cloud.google.com/vertex-ai/docs/generative-ai/extensions/overview | Search vs Action | FACT | HIGH | Sept 2026 |
| EVI-008  | Custom MCP Servers are currently in Public Preview. | https://cloud.google.com/release-notes | Preview Features | FACT | HIGH | July 2026 |
| EVI-009  | Drive data stores suffer from restricted folder-level scoping, making granular ACLs hard. | MISSING EXACT URL (opsinsecurity.com / github) | Governance | COMMUNITY REPORT | LOW (Downgraded) | Sept 2026 |
| EVI-010  | External setups (e.g. M365) require complex OAuth/multi-tenant app config, causing operational friction. | MISSING EXACT URL (reddit/github) | Auth Hurdles | COMMUNITY REPORT | LOW (Downgraded) | Sept 2026 |
| EVI-011  | Agents reportedly fail to automatically pick up authorization tokens, requiring manual injection. | MISSING EXACT URL (github) | Tool Calling | COMMUNITY REPORT | LOW (Downgraded) | Sept 2026 |
"""

with open("research/EVIDENCE_INDEX.md", "w") as f:
    f.write(evidence_index_content)


open_questions_content = """# Open Questions

This document tracks unresolved questions, conflicting sources, and areas where documentation is insufficient.

## Unresolved Questions (from Pre-Research Audit)
- **ADK Agent Identity:** Does Gemini Enterprise securely and verifiably pass the end user's identity (e.g., `tool_context.session.user_id`) to ADK agents? The ADR notes a conflict between "One official Google doc" and GitHub discussions/ADK docs.
- **Custom MCP Token Forwarding:** Does a Custom MCP Server data store actually receive the signed-in end user's OAuth token intact via the `Authorization` header, and the service agent token via `X-Serverless-Authorization`?
- **Data Store ACL Mode:** Is the ACL mode for a Custom Connector data store truly fixed at creation time and non-retrofittable?
- **Connector Modes:** Which native connectors strictly use ingestion vs. federation (e.g., Jira Data Center, Salesforce, Confluence Data Center)?
- **A2A Agent Status:** Is the A2A agent registration officially "Pre-GA" / limited support?
- **Private Egress:** Does Gemini Enterprise support egressing via Private Service Connect (PSC) to reach fully isolated VPC endpoints without a public IP?
- **Security & Prompt Injection:** If an LLM is given access to a federated connector, how do we guarantee the LLM cannot be manipulated via prompt injection to bypass connector-level filters and request unauthorized data?
- **API Configurability:** Can Custom MCP endpoints and Custom Connectors be configured entirely via self-serve API/UI, or do they require Google support whitelisting?

## Unresolved Questions (from Track 1)
- **Large-Scale Sync Errors:** What specific error boundaries trigger the "unreadable document errors" during large-scale Drive/OneDrive syncing reported by the community?
- **Token Injection Scope:** Are the token injection issues reported by the community applicable to Custom MCPs, or only to ADK agents?
- **API Configurability Gap:** How is the `THIRD_PARTY_FEDERATED` connector type exposed in the API practically configured by a customer if no UI exists for it?
- **Preview Quotas:** If Custom MCP is only Public Preview, are there hidden quota/SLA limits that would fail our Razorpay demo under load?
- **Missing Community Citations (Audit Gap):** We must locate the exact GitHub issues, Reddit threads, and blog post URLs for EVI-009, EVI-010, and EVI-011. Without exact URLs, these community claims are marked UNSUPPORTED.
"""

with open("research/open_questions.md", "w") as f:
    f.write(open_questions_content)
