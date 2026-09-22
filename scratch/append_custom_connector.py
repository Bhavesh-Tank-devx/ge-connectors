import os

custom_mcp_updates = """
## 4. Prerequisites for Custom MCP
**FACT**: Custom MCP Server data stores are gated by Google Cloud Organization Policies. To deploy, an Org Policy Administrator must set `constraints/discoveryengine.managed.disableCustomMcpServerConnector` to **Off** and add `custom_mcp` to `constraints/discoveryengine.managed.allowedDataSources`.
**FACT**: The MCP transport protocol is strictly restricted to `StreamableHTTP`. The server must possess a valid TLS certificate from a publicly trusted CA (internal CAs are blocked in the public console registration).
"""

with open('research/custom_mcp.md', 'a') as f:
    f.write(custom_mcp_updates)

new_evidence = """| EVI-032 | Custom connectors follow a Fetch, Transform, and Sync pipeline to prepare and upload JSON data. | FACT | https://cloud.google.com/gemini/enterprise/docs/ |
| EVI-033 | Custom MCP Servers can be registered as Data Stores, communicating exclusively via StreamableHTTP with public CA TLS. | FACT | https://cloud.google.com/gemini/enterprise/docs/ |
| EVI-034 | Custom MCP Server data stores are blocked by default and require overriding org policy constraints. | FACT | https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints |
| EVI-035 | The `DataConnector` API (`SetUpDataConnector`) cannot be used to author arbitrary connectors; `dataSource` is restricted to Google's catalog. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1alpha/projects.locations/setUpDataConnector |
| EVI-036 | Document-level security supports `acl_info` containing `externalEntityId` mapped via `IdentityMappingStore`. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1alpha/projects.locations.identityMappingStores |
| EVI-037 | Data Store ACL mode and `identityMappingStore` binding must be established at creation and are immutable. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1/projects.locations.collections.dataStores |
| EVI-038 | `importDocuments` supports `INCREMENTAL` and `FULL` reconciliation modes. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1/projects.locations.collections.dataStores.branches.documents/import |
| EVI-039 | Gemini Enterprise forwards the signed-in user's OAuth access token in the `Authorization` header to Custom MCP Servers. | FACT | https://cloud.google.com/gemini/enterprise/docs/ |
| EVI-040 | Custom MCP server data stores are capped at 100 enabled actions at a time. | FACT | https://cloud.google.com/gemini/enterprise/docs/ |
| EVI-041 | Native third-party connectors (Jira, Salesforce, Confluence) default to Ingestion; federated search is not freely configurable across arbitrary endpoints. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("Custom Connector Evidence updated successfully.")
