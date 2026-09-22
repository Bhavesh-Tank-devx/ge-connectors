import os

federation_updates = """
## 4. The `FEDERATED_AND_EUA` Mode
**FACT**: The API and Google Cloud Terraform provider formally define `FEDERATED_AND_EUA` as a hybrid mode. It combines zero data copying (live query) with user-delegated OAuth credential forwarding (Source-Side Authorization).
**FACT**: When `FEDERATED_AND_EUA` is used with native apps (e.g. ServiceNow), the live API request arrives at the third-party system tagged with the individual user's OAuth token. The third-party system executes its own internal security logic, achieving **1:1 access parity with the external system's native web UI**.

## 5. Architectural Decision: When to Federate
- **Ingest (`DATA_INGESTION`)**: Low Volatility, High Latency Tolerance. (e.g. Confluence, SharePoint Docs, Policy Docs). Optimized for broad semantic vector search.
- **Federate (`FEDERATED_AND_EUA`)**: High Volatility, Low Latency Tolerance. (e.g. Active Jira Tickets, ServiceNow Incidents, Razorpay Payroll). Mandatory when real-time freshness is required and data duplication is restricted by compliance.
"""

with open('research/federation.md', 'a') as f:
    f.write(federation_updates)

new_evidence = """| EVI-053 | `ConnectorMode` enum supports `DATA_INGESTION`, `ACTIONS`, `FEDERATED`, `EUA`, and `FEDERATED_AND_EUA`. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rpc/google.cloud.discoveryengine.v1 |
| EVI-054 | `FEDERATED_AND_EUA` is defined as a hybrid connector for federated search and End User Authentication in Terraform. | FACT | https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/discovery_engine_data_connector |
| EVI-055 | Federated search retrieves data directly from source at query time without copying into Google index. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-056 | Federated search quality may be lower because data is not pre-indexed by Google; queries traverse to external backends. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-057 | `FederatedSearchConfig` configures federated stores using `ThirdPartyOauthConfig` (`app_name`, `instance_name`). | FACT | https://cloud.google.com/discovery-engine/docs/reference/rpc/google.cloud.discoveryengine.v1 |
| EVI-058 | `oauthStaticIpAddresses` provides dedicated static IPs for OAuth/EUA endpoints separate from general traffic. | FACT | https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/discovery_engine_data_connector |
| EVI-062 | ServiceNow connector natively supports Federated Search, Ingestion, and Actions via OAuth. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("Federation and EUA evidence updated successfully.")
