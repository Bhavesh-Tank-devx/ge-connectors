# Identity Mapping

## 1. When is identity mapping required?
**FACT**: Identity mapping is required whenever the identity used to log into Gemini Enterprise (e.g., Google Workspace email) differs from the identity format expected by the source system's ACLs (e.g., an internal Employee ID or Salesforce ID).
*Source: https://cloud.google.com/generative-ai-app-builder/docs/about-access-control*

## 2. Architecture
**FACT**: Gemini Enterprise uses an `IdentityMappingStore` (a native resource) to map third-party identities to Google Cloud identities.
**FACT**: The mapping store must be continuously synchronized with the source of truth (e.g., HRIS or Entra ID).

## 4. ACL Enforcement Mechanics (Server-Side)
**FACT**: Document authorization is enforced **server-side** inside the Google Cloud Discovery Engine retrieval infrastructure at query time. It is never enforced on the client, and never left to the generative LLM prompt. The generative model is physically unable to access documents that do not pass the reader filter.
**FACT**: Administrative APIs (`DocumentService.GetDocument`, `DocumentService.ListDocuments`) and the Google Cloud Console "Data > Documents" browser are completely blocked/disabled for `aclEnabled` data stores to prevent administrator data leakage.

## 5. Schema and Immutability
**FACT**: ACLs are represented in document metadata via the `acl_info` object, containing a repeated list of `readers` (`AccessRestriction`). Each `Principal` is a protobuf `oneof` containing `user_id`, `group_id`, or `external_entity_id` (hard length limit: 100 characters).
**FACT**: Both `aclEnabled` and `identityMappingStore` bindings are strictly immutable at data store creation.
