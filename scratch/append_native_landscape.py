import os

native_updates = """
## 4. The `ConnectorMode` Enum & Operational Realities (August 2026)
**FACT**: The Discovery Engine API defines four operational modes in the `ConnectorMode` enum:
- `DATA_INGESTION`: Batch crawling and chunking into managed Data Stores.
- `FEDERATED`: Real-time pass-through querying without data replication.
- `ACTIONS`: Agentic execution of write operations and mutations.
- `EUA` (End User Authentication): Query-time security mapping.

**FACT**: Jira Cloud and Salesforce natively support both Ingestion and Federation. However, Confluence, SharePoint, Google Drive, Box, and GitHub strictly operate via **Data Ingestion (Indexing)** and do not natively offer federation.
"""

with open('research/native_connectors.md', 'a') as f:
    f.write(native_updates)

new_evidence = """| EVI-042 | A `DataConnector` is a singleton resource managing ingestion, federation, actions, and secrets. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1alpha/projects.locations.collections.dataConnector |
| EVI-043 | `ConnectorMode` enum explicitly includes `DATA_INGESTION`, `FEDERATED`, `ACTIONS`, and `EUA`. | FACT | google.cloud.discoveryengine.v1alpha |
| EVI-044 | Jira Cloud data store natively supports both "Data ingestion" and "Federated search" modes. | FACT | https://cloud.google.com/gemini/docs |
| EVI-045 | Jira Cloud connector supports agentic actions (create/update issue, add comment, assign). | FACT | https://cloud.google.com/gemini/docs |
| EVI-046 | Confluence, SharePoint, and Google Drive strictly operate via Data Ingestion and lack federation. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-047 | Enforcing VPC-SC on existing Salesforce data stores is not supported without recreation. | FACT | https://cloud.google.com/agent-builder/docs |
| EVI-048 | Data store sync for Jira, Confluence, and Salesforce entered Private Preview August 13, 2026. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/release-notes |
| EVI-049 | Google Drive connector cannot restrict ingestion to a specific folder or subdirectory. | FACT | Verified via Agent Builder Console |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("Native Connector Landscape evidence and files updated successfully.")
