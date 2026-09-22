# Native and Managed Connectors in Gemini Enterprise

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
The API exposes `ConnectorMode` enums for `DATA_INGESTION`, `FEDERATED`, `ACTIONS`, `EUA`, and `FEDERATED_AND_EUA`. While historically biased toward ingestion, the practical reality of native data connectors is heavily biased toward ingestion. 
- **Platform Capability vs Customer Configurable**: The API exposes `FEDERATED` and `ACTIONS` enums, but for native connectors, customers can generally only configure `DATA_INGESTION` via the UI.
- **Ingestion** is the default for native out-of-the-box data stores.
- **Federation** (real-time) via native data stores is less common than ingestion; real-time federation is typically handled via Custom MCP or Vertex AI Extensions rather than "Native Connectors".

## 6. Connector-Specific Capability Matrix
| Connector | Mode | Capabilities | Auth Pattern | Status |
|---|---|---|---|---|
| **Jira (Cloud)** | Ingestion & Fed | Search & Actions | Google ID, OIDC/SAML | GA |
| **Salesforce** | Ingestion & Fed | Search | Google ID, OIDC/SAML | Preview (Rolling out) |
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
Historically Native Data Connectors were **Search only** (read-only), but Jira Cloud and Microsoft Connectors now natively support **Actions** (Preview). For other read-only connectors, developers must use Custom MCP servers: Vertex AI Extensions, Agent Tools, or Custom MCP servers. (Exception: Preview actions for Microsoft Data Stores).

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
  - **Verdict:** **PARTIALLY CONTRADICTED**. Jira Cloud and Salesforce actually *do* support both Ingestion and Federation natively. However, Confluence, SharePoint, and Google Drive default strictly to **Ingestion (Indexing)** and do not natively support federation.
- **ADR Claim:** "Custom MCP Server data store (federated)" is a viable production path.
  - **Verdict:** **WEAKENED/CAVEAT**. Release Status research confirms Custom MCP is in **Public Preview** (July 2026), meaning it should not be treated as a fully GA platform capability.

## 16. Open Questions
- What specific error boundaries trigger the "unreadable document errors" during large-scale Drive/OneDrive syncing reported by the community?
- Are the token injection issues reported by the community applicable to Custom MCPs, or only to ADK agents?
- How is the `THIRD_PARTY_FEDERATED` connector type exposed in the API practically configured by a customer if no UI exists for it?
- If Custom MCP is only Public Preview, are there hidden quota/SLA limits that would fail our Razorpay demo under load?
- [AUDIT ADDITION]: Exact URLs for GitHub/Reddit community claims must be found to upgrade them from UNSUPPORTED.

## 4. The `ConnectorMode` Enum & Operational Realities (August 2026)
**FACT**: The Discovery Engine API defines four operational modes in the `ConnectorMode` enum:
- `DATA_INGESTION`: Batch crawling and chunking into managed Data Stores.
- `FEDERATED`: Real-time pass-through querying without data replication.
- `ACTIONS`: Agentic execution of write operations and mutations.
- `EUA` (End User Authentication): Query-time security mapping.

**FACT**: Jira Cloud and Salesforce natively support both Ingestion and Federation. However, Confluence, SharePoint, Google Drive, Box, and GitHub strictly operate via **Data Ingestion (Indexing)** and do not natively offer federation.
