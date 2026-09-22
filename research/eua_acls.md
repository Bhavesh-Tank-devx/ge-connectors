# ACLs and Authorization Enforcement

## 1. How are ACLs represented and enforced?
**FACT**: In an Ingestion architecture, ACLs are represented as `aclInfo` metadata on the Document resource during ingestion.
**FACT**: Enforcement happens server-side in the Discovery Engine index before the LLM receives any context. If a user's principal does not match the document's `aclInfo`, the chunk is pruned.
*Source: https://cloud.google.com/generative-ai-app-builder/docs/about-access-control*

## 2. Where is authorization enforced in each architecture?
- **Ingestion**: Enforced at the GCP Data Store (Search Index) based on synchronized `aclInfo`.
- **Federation**: Enforced at the remote source (e.g., Jira) during the proxied query using EUA.
- **MCP**: Enforced by the middleware Custom MCP Server validating the user's OIDC token.

## 3. What happens when permissions change?
**FACT**: For ingestion, permission changes in the source system do not take effect in Gemini Enterprise until the ingestion pipeline re-syncs and updates the Document's `aclInfo`.
**INFERENCE**: This introduces an access vulnerability window proportional to the sync latency.
