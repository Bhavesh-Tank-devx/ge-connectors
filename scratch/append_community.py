import os

community_updates = """
## 3. Community-Reported Friction Points & Bugs (As of Sept 2026)
**COMMUNITY REPORT**: **Terraform Provider Danger**: Modifying the `data_store_ids` list in `google_discovery_engine_chat_engine` or `google_discovery_engine_search_engine` in Terraform marks the resource as `forces replacement`, dangerously destroying and recreating the engine rather than patching it.
**COMMUNITY REPORT**: **ADK Tool Limits**: The `VertexAiSearchTool` in the Python ADK runs exclusively under the service account and has no built-in mechanism to pass or trigger an end-user OAuth 2.0 flow for query-time ACL filtering. Setting `bypass_multi_tools_limit=True` introduces breaking module dependencies and strips grounding citations.
**COMMUNITY REPORT**: **Google Drive Scope Creep**: The native Google Drive connector lacks fine-grained folder-level exclusion controls, leading to "permission creep" where broadly shared internal documents are unexpectedly surfaced by the AI.
**COMMUNITY REPORT**: **Identity Mapping Ceilings**: The Discovery Engine `IdentityMappingStore` has a hard batch import limit of 500,000 identities, requiring complex SQL-based Change Data Capture (CDC) pipelines for massive enterprises.
"""

with open('research/open_questions.md', 'a') as f:
    f.write(community_updates)

new_evidence = """| EVI-080 | `VertexAiSearchTool` cannot pass user OAuth credentials for query-time ACL filtering. | COMMUNITY REPORT | https://github.com/google/adk-python/issues/897 |
| EVI-081 | Hidden Agent Engine SA (`service-...@gcp-sa-aiplatform-cc...`) triggers `403 PERMISSION_DENIED`. | COMMUNITY REPORT | https://github.com/google/adk-python/issues/1476 |
| EVI-082 | `bypass_multi_tools_limit` drops citations, breaks dependencies, hardcodes tool names. | COMMUNITY REPORT | https://github.com/google/adk-python/issues/7100 |
| EVI-083 | Updating `data_store_ids` in Terraform forces delete & recreate of engine. | COMMUNITY REPORT | https://github.com/hashicorp/terraform-provider-google/issues/20603 |
| EVI-084 | Ingesting ~1.4k files from Drive triggers opaque `"FC"` error due to API limits. | COMMUNITY REPORT | https://discuss.google.dev/t/attempt-to-create-corpus-fails-with-fc-error/191148 |
| EVI-085 | Identity Mapping Store caps at 500k identities per load; requires BigQuery CDC for scale. | COMMUNITY REPORT | https://medium.com/google-cloud/building-enterprise-scale-custom-connectors-for-vertex-ai-discovery-engine-gemini-enterprise-99a136f561e7 |
| EVI-086 | Drive connector surfaces overshared data; lacks folder micro-segmentation. | COMMUNITY REPORT | https://www.opsinsecurity.com/use-cases/gemini-security |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("Community Evidence updated successfully.")
