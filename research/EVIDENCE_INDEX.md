# Evidence Index

This is the central index of claims and their supporting sources for the Gemini Enterprise Connector POC.

| Claim ID | Claim Summary | Source URL | Relevant Section | Classification (Fact/Inference/Community) | Confidence Level | Date/Status |
|----------|---------------|------------|------------------|-------------------------------------------|------------------|-------------|
| EVI-006  | Native connectors for Jira, Confluence, SharePoint default to Ingestion, not Federation. | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources | Capability Matrix | FACT | HIGH | Sept 2026 |
| EVI-007  | Native Connectors are overwhelmingly Search-only (read-only); mutations require Extensions/MCP. | https://cloud.google.com/vertex-ai/docs/generative-ai/extensions/overview | Search vs Action | FACT | HIGH | Sept 2026 |
| EVI-098  | Custom MCP Servers are currently in Public Preview. | https://cloud.google.com/release-notes | Preview Features | FACT | HIGH | July 2026 |
| EVI-099  | Drive data stores suffer from restricted folder-level scoping, making granular ACLs hard. | MISSING EXACT URL (opsinsecurity.com / github) | Governance | COMMUNITY REPORT | LOW (Downgraded) | Sept 2026 |
| EVI-010  | External setups (e.g. M365) require complex OAuth/multi-tenant app config, causing operational friction. | MISSING EXACT URL (reddit/github) | Auth Hurdles | COMMUNITY REPORT | LOW (Downgraded) | Sept 2026 |
| EVI-011  | Agents reportedly fail to automatically pick up authorization tokens, requiring manual injection. | MISSING EXACT URL (github) | Tool Calling | COMMUNITY REPORT | LOW (Downgraded) | Sept 2026 |
| EVI-001 | Custom MCP Server receives the end user's OAuth token in `Authorization` and the Gemini service agent ID token in `X-Serverless-Authorization`. | FACT | https://cloud.google.com/run/docs/authenticating/service-to-service |
| EVI-002 | Gemini Enterprise Custom MCP requires `StreamableHTTP` transport; SSE is unsupported. Requires CA-signed TLS. | FACT | https://cloud.google.com/gemini/docs/enterprise/ |
| EVI-003 | Custom MCP Server data store is currently in **Public Preview** (as of mid-2026) and requires an Org Policy override. | FACT | https://cloud.google.com/gemini/docs/enterprise/ |
| EVI-004 | Discovery Engine `DataStore.aclEnabled` is **immutable** and must be specified at data store creation time. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/projects.locations.collections.dataStores |
| EVI-005 | Identity Mapping Stores map Google Cloud / corporate identities to 3P identifiers via `externalEntityId`. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/projects.locations.identityMappingStores |
| EVI-008 | A2A (Agent-to-Agent) agent registration in Gemini Enterprise is subject to Pre-GA Offerings Terms. | FACT | https://cloud.google.com/vertex-ai/docs/agent-builder/a2a |
| EVI-009 | ADK `tool_context.session.user_id` is caller-supplied and not cryptographically verifiable by agent tools. | COMMUNITY REPORT / FACT | https://github.com/google/adk-python |
| EVI-012 | Default 3P incremental sync is 3 hours (30m-7d); ACL refresh default is 30 mins (30m-7d). | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-013 | Initial connector crawl triggers approximately 1 hour after connector provisioning. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-014 | `ReconciliationMode.INCREMENTAL` upserts by ID; `ReconciliationMode.FULL` purges missing documents with zero downtime. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1alpha/projects.locations.collections.dataStores.branches.documents/import#ReconciliationMode |
| EVI-015 | `ConnectorRun` lifecycle includes PENDING, RUNNING, SUCCEEDED, FAILED, WARNING, SKIPPED, CANCELLED. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1alpha/projects.locations.collections.dataConnector.connectorRuns#State |
| EVI-016 | Overlapping scheduled runs enter SKIPPED state if prior run is still ongoing. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1alpha/projects.locations.collections.dataConnector.connectorRuns |
| EVI-017 | Document write quota is 12,000 requests/minute/project; max data stores and engines are 500 per project. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/quotas |
| EVI-019 | Audit logs generated under `protoPayload.serviceName="discoveryengine.googleapis.com"`. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/audit-logging |
| EVI-021 | Data residency confined to `us` or `eu` multi-regions, including ML inference and tuning. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/locations |
| EVI-026 | `discoveryengine.googleapis.com` is a supported service for VPC Service Controls. Existing data stores must be recreated when applying perimeters. | FACT | https://cloud.google.com/vpc-service-controls/docs/supported-products |
| EVI-027 | Cloud Run supports Direct VPC Egress without Serverless VPC Access connectors (up to 1 Gbps/instance). | FACT | https://cloud.google.com/run/docs/configuring/vpc-direct-vpc |
| EVI-028 | Agent Gateway secures outbound traffic against Agent Registry allowlists and IAM policies. | FACT | https://cloud.google.com/agent-gateway/docs |
| EVI-029 | Agent Identity provisions short-lived SPIFFE IDs and X.509 certs, using mTLS and RFC 9449 DPoP. | FACT | https://datatracker.ietf.org/doc/html/rfc9449 |
| EVI-030 | Model Armor provides pre- and post-inference screening up to 65,536 tokens for prompt injection and jailbreaks. | FACT | https://cloud.google.com/security/products/model-armor |
| EVI-031 | The Check Grounding API validates factual support scores between generated text and retrieved chunks. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/check-grounding |
| EVI-032 | Custom connectors follow a Fetch, Transform, and Sync pipeline to prepare and upload JSON data. | FACT | https://cloud.google.com/gemini/enterprise/docs/ |
| EVI-033 | Custom MCP Servers can be registered as Data Stores, communicating exclusively via StreamableHTTP with public CA TLS. | FACT | https://cloud.google.com/gemini/enterprise/docs/ |
| EVI-034 | Custom MCP Server data stores are blocked by default and require overriding org policy constraints. | FACT | https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints |
| EVI-035 | The `DataConnector` API (`SetUpDataConnector`) cannot be used to author arbitrary connectors; `dataSource` is restricted to Google's catalog. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1alpha/projects.locations/setUpDataConnector |
| EVI-036 | Document-level security supports `acl_info` containing `externalEntityId` mapped via `IdentityMappingStore`. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1alpha/projects.locations.identityMappingStores |
| EVI-037 | Data Store ACL mode and `identityMappingStore` binding must be established at creation and are immutable. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1/projects.locations.collections.dataStores |
| EVI-038 | `importDocuments` supports `INCREMENTAL` and `FULL` reconciliation modes. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1/projects.locations.collections.dataStores.branches.documents/import |
| EVI-039 | Gemini Enterprise forwards the signed-in user's OAuth access token in the `Authorization` header to Custom MCP Servers. | FACT | https://cloud.google.com/gemini/enterprise/docs/ |
| EVI-040 | Custom MCP server data stores are capped at 100 enabled actions at a time. | FACT | https://cloud.google.com/gemini/enterprise/docs/ |
| EVI-041 | Native third-party connectors (Jira, Salesforce, Confluence) default to Ingestion; federated search is not freely configurable across arbitrary endpoints. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-MCP-01 | In MCP spec, capabilities are "tools"; in Gemini Enterprise data stores, they are "actions" (interchangeable). | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-02 | StreamableHTTP transport is exclusively supported; SSE transport is not supported. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-03 | Public and private MCP servers must have TLS signed by a publicly trusted CA. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-04 | Requests send user OAuth token in `Authorization` and Discovery Engine service agent ID token in `X-Serverless-Authorization`. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-05 | `X-Serverless-Authorization` is only automatically sent to default `.run.app` URLs, not custom domains. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-06 | Service agent requires `roles/run.invoker` (`service-<NUM>@gcp-sa-discoveryengine.iam.gserviceaccount.com`). | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-08 | Maximum of 100 enabled actions per custom MCP server data store. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-09 | Actions require user confirmation by default; bypassed with `readOnlyHint: True` and `destructiveHint: False`. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-10 | Creation blocked by `constraints/discoveryengine.managed.disableCustomMcpServerConnector`. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/override-constraint-for-custom-mcp-data-stores |
| EVI-MCP-12 | Custom MCP server data store released in Public Preview on April 28, 2026. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/release-notes |
| EVI-042 | A `DataConnector` is a singleton resource managing ingestion, federation, actions, and secrets. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rest/v1alpha/projects.locations.collections.dataConnector |
| EVI-043 | `ConnectorMode` enum explicitly includes `DATA_INGESTION`, `FEDERATED`, `ACTIONS`, and `EUA`. | FACT | google.cloud.discoveryengine.v1alpha |
| EVI-044 | Jira Cloud data store natively supports both "Data ingestion" and "Federated search" modes. | FACT | https://cloud.google.com/gemini/docs |
| EVI-045 | Jira Cloud connector supports agentic actions (create/update issue, add comment, assign). | FACT | https://cloud.google.com/gemini/docs |
| EVI-046 | Confluence, SharePoint, and Google Drive strictly operate via Data Ingestion and lack federation. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-047 | Enforcing VPC-SC on existing Salesforce data stores is not supported without recreation. | FACT | https://cloud.google.com/agent-builder/docs |
| EVI-048 | Data store sync for Jira, Confluence, and Salesforce entered Private Preview August 13, 2026. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/release-notes |
| EVI-049 | Google Drive connector cannot restrict ingestion to a specific folder or subdirectory. | FACT | Verified via Agent Builder Console |
| EVI-053 | `ConnectorMode` enum supports `DATA_INGESTION`, `ACTIONS`, `FEDERATED`, `EUA`, and `FEDERATED_AND_EUA`. | FACT | https://cloud.google.com/discovery-engine/docs/reference/rpc/google.cloud.discoveryengine.v1 |
| EVI-054 | `FEDERATED_AND_EUA` is defined as a hybrid connector for federated search and End User Authentication in Terraform. | FACT | https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/discovery_engine_data_connector |
| EVI-055 | Federated search retrieves data directly from source at query time without copying into Google index. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-056 | Federated search quality may be lower because data is not pre-indexed by Google; queries traverse to external backends. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-057 | `FederatedSearchConfig` configures federated stores using `ThirdPartyOauthConfig` (`app_name`, `instance_name`). | FACT | https://cloud.google.com/discovery-engine/docs/reference/rpc/google.cloud.discoveryengine.v1 |
| EVI-058 | `oauthStaticIpAddresses` provides dedicated static IPs for OAuth/EUA endpoints separate from general traffic. | FACT | https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/discovery_engine_data_connector |
| EVI-062 | ServiceNow connector natively supports Federated Search, Ingestion, and Actions via OAuth. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-068 | `acl_info` schema uses `readers` containing `principals` (`user_id`, `group_id`, `external_entity_id`) and `idp_wide`. | FACT | https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.DiscoveryEngine.V1/latest/Google.Cloud.DiscoveryEngine.V1.Document.Types.AclInfo |
| EVI-069 | `Principal` is a protobuf oneof supporting `UserId`, `GroupId`, and `ExternalEntityId` (max 100 chars). | FACT | https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.DiscoveryEngine.V1/latest/Google.Cloud.DiscoveryEngine.V1.Principal |
| EVI-070 | DataStore `aclEnabled` and `identityMappingStore` fields are immutable and can only be set at creation time. | FACT | https://docs.cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/projects.locations.collections.dataStores |
| EVI-071 | Maximum limit of 3,000 readers per document; Data > Documents console tab is disabled for ACL-enabled data stores. | FACT | https://docs.cloud.google.com/generative-ai-app-builder/docs/data-source-access-control |
| EVI-072 | `DocumentService.GetDocument` and `ListDocuments` are disabled when `aclEnabled: true`. | FACT | https://docs.cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/projects.locations.collections.dataStores |
| EVI-073 | `IdentityMappingStore` stores `IdentityMappingEntry` linking `external_identity` to `user_id` or `group_id`. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/identity-mapping |
| EVI-075 | `importIdentityMappings` supports up to 500,000 entries per import operation and file sizes up to 2 GB. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/identity-mapping |
| EVI-077 | Authorization is evaluated server-side at query time; the generative LLM only receives documents passing the reader filter. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/identity-mapping |
| EVI-080 | `VertexAiSearchTool` cannot pass user OAuth credentials for query-time ACL filtering. | COMMUNITY REPORT | https://github.com/google/adk-python/issues/897 |
| EVI-081 | Hidden Agent Engine SA (`service-...@gcp-sa-aiplatform-cc...`) triggers `403 PERMISSION_DENIED`. | COMMUNITY REPORT | https://github.com/google/adk-python/issues/1476 |
| EVI-082 | `bypass_multi_tools_limit` drops citations, breaks dependencies, hardcodes tool names. | COMMUNITY REPORT | https://github.com/google/adk-python/issues/7100 |
| EVI-083 | Updating `data_store_ids` in Terraform forces delete & recreate of engine. | COMMUNITY REPORT | https://github.com/hashicorp/terraform-provider-google/issues/20603 |
| EVI-084 | Ingesting ~1.4k files from Drive triggers opaque `"FC"` error due to API limits. | COMMUNITY REPORT | https://discuss.google.dev/t/attempt-to-create-corpus-fails-with-fc-error/191148 |
| EVI-085 | Identity Mapping Store caps at 500k identities per load; requires BigQuery CDC for scale. | COMMUNITY REPORT | https://medium.com/google-cloud/building-enterprise-scale-custom-connectors-for-vertex-ai-discovery-engine-gemini-enterprise-99a136f561e7 |
| EVI-086 | Drive connector surfaces overshared data; lacks folder micro-segmentation. | COMMUNITY REPORT | https://www.opsinsecurity.com/use-cases/gemini-security |
| EVI-087 | Local simulation confirms Custom MCP zero-trust extraction from Auth header prevents LLM prompt-injection routing. | FACT | Local Architecture Test (`demo/custom_mcp/server.py`) |
