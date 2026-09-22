# Federation and EUA

## 1. What is Federation?
**FACT**: Federation is real-time delegated search. Gemini Enterprise intercepts the user's prompt, generates a search query, and proxies it to a remote enterprise search engine (e.g., Jira Cloud, Google Drive) without duplicating the data into a GCP index.
*Source: https://cloud.google.com/agent-builder/docs/about-third-party-data-sources*

## 2. What is EUA (End User Authentication)?
**FACT**: EUA ensures that Gemini Enterprise queries a data source acting as the specific human user, rather than using a highly-privileged service account.

## 3. What is FEDERATED_AND_EUA?
**FACT**: This is an integration mode where the query is proxied live to the remote search engine (Federated) AND is executed using an OAuth token or identity claim bound to the user (EUA), ensuring the remote system enforces its own access controls.

## 4. Architectural Reality: No Arbitrary Federation
**FACT**: Customers cannot configure a generic REST API (like the Razorpay case study) as a federated data store. Federation requires the remote system to have a compatible enterprise search index.

## 4. The `FEDERATED_AND_EUA` Mode
**FACT**: The API and Google Cloud Terraform provider formally define `FEDERATED_AND_EUA` as a hybrid mode. It combines zero data copying (live query) with user-delegated OAuth credential forwarding (Source-Side Authorization).
**FACT**: When `FEDERATED_AND_EUA` is used with native apps (e.g. ServiceNow), the live API request arrives at the third-party system tagged with the individual user's OAuth token. The third-party system executes its own internal security logic, achieving **1:1 access parity with the external system's native web UI**.

## 5. Architectural Decision: When to Federate
- **Ingest (`DATA_INGESTION`)**: Low Volatility, High Latency Tolerance. (e.g. Confluence, SharePoint Docs, Policy Docs). Optimized for broad semantic vector search.
- **Federate (`FEDERATED_AND_EUA`)**: High Volatility, Low Latency Tolerance. (e.g. Active Jira Tickets, ServiceNow Incidents, Razorpay Payroll). Mandatory when real-time freshness is required and data duplication is restricted by compliance.
