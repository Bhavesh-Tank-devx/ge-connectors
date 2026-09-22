import os

identity_mapping_updates = """
## 4. ACL Enforcement Mechanics (Server-Side)
**FACT**: Document authorization is enforced **server-side** inside the Google Cloud Discovery Engine retrieval infrastructure at query time. It is never enforced on the client, and never left to the generative LLM prompt. The generative model is physically unable to access documents that do not pass the reader filter.
**FACT**: Administrative APIs (`DocumentService.GetDocument`, `DocumentService.ListDocuments`) and the Google Cloud Console "Data > Documents" browser are completely blocked/disabled for `aclEnabled` data stores to prevent administrator data leakage.

## 5. Schema and Immutability
**FACT**: ACLs are represented in document metadata via the `acl_info` object, containing a repeated list of `readers` (`AccessRestriction`). Each `Principal` is a protobuf `oneof` containing `user_id`, `group_id`, or `external_entity_id` (hard length limit: 100 characters).
**FACT**: Both `aclEnabled` and `identityMappingStore` bindings are strictly immutable at data store creation.
"""

with open('research/identity_mapping.md', 'a') as f:
    f.write(identity_mapping_updates)

new_evidence = """| EVI-068 | `acl_info` schema uses `readers` containing `principals` (`user_id`, `group_id`, `external_entity_id`) and `idp_wide`. | FACT | https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.DiscoveryEngine.V1/latest/Google.Cloud.DiscoveryEngine.V1.Document.Types.AclInfo |
| EVI-069 | `Principal` is a protobuf oneof supporting `UserId`, `GroupId`, and `ExternalEntityId` (max 100 chars). | FACT | https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.DiscoveryEngine.V1/latest/Google.Cloud.DiscoveryEngine.V1.Principal |
| EVI-070 | DataStore `aclEnabled` and `identityMappingStore` fields are immutable and can only be set at creation time. | FACT | https://docs.cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/projects.locations.collections.dataStores |
| EVI-071 | Maximum limit of 3,000 readers per document; Data > Documents console tab is disabled for ACL-enabled data stores. | FACT | https://docs.cloud.google.com/generative-ai-app-builder/docs/data-source-access-control |
| EVI-072 | `DocumentService.GetDocument` and `ListDocuments` are disabled when `aclEnabled: true`. | FACT | https://docs.cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/projects.locations.collections.dataStores |
| EVI-073 | `IdentityMappingStore` stores `IdentityMappingEntry` linking `external_identity` to `user_id` or `group_id`. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/identity-mapping |
| EVI-075 | `importIdentityMappings` supports up to 500,000 entries per import operation and file sizes up to 2 GB. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/identity-mapping |
| EVI-077 | Authorization is evaluated server-side at query time; the generative LLM only receives documents passing the reader filter. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/identity-mapping |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("ACLs and Identity Mapping evidence updated successfully.")
