# Architecture Decision Framework

### 1. What should be indexed vs queried live?
- **Index (Custom Connector)**: Large document corpora, historical knowledge bases, static policies. Requires full-text or semantic search across millions of records.
- **Query Live (MCP)**: Highly volatile transactional data, user-specific profiles, financial balances, PII where duplication violates governance.

### 2. The Razorpay Case Study Architecture
**Problem**: Razorpay API uses an org-level API key, lacking per-user OAuth scoping.
**Decision**: **Custom MCP**.
**Why**: 
1. We cannot use Federation (the Razorpay API is not an enterprise search engine).
2. We cannot use Ingestion without duplicating sensitive payroll data into a Google index.
3. Custom MCP allows a Cloud Run middleware server to validate the user's OIDC identity, map it to an Employee ID, and securely append the Org-Level API key on the backend, enforcing zero-trust isolation regardless of LLM hallucinations.
