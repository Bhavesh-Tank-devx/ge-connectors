import os

custom_connectors_content = """# Custom Connectors & Ingestion Architecture

## 1. What is a Data Store?
**FACT**: A Data Store in Gemini Enterprise (Discovery Engine) is the foundational storage and indexing unit containing ingested chunks, metadata, embeddings, and ACLs. Once created, foundational configurations—such as `aclEnabled` and data store type—are immutable.
*Scope: Platform* | *Source: https://cloud.google.com/generative-ai-app-builder/docs/create-data-store*

## 2. What is Ingestion?
**FACT**: Ingestion is the asynchronous, server-side data pipeline process of transferring raw data from external sources into a Data Store, converting it into structured or unstructured `Document` resources, parsing the content, splitting text into semantic chunks (100–500 tokens), generating dense vector embeddings, and indexing the content.

## 3. Custom Ingestion Pipelines (Dual-Path Hybrid)
For enterprise custom connectors, a dual-path hybrid architecture is recommended:
1. **Fast Path (Real-time Streaming)**: Pub/Sub -> Cloud Run worker -> Direct Upsert (`CreateDocument`/`PatchDocument`). Freshness in minutes.
2. **Slow Path (Nightly Reconciliation)**: Batch extraction to GCS `.jsonl` -> `ImportDocuments(reconciliationMode = FULL)`. Automatically purges deleted items and corrects index drift with zero downtime.

## 4. What does the public customer-authoring experience actually allow?
**FACT**: Customers can author custom ingestion pipelines using the Discovery Engine Document API (REST/gRPC). They can push JSON or unstructured files into a Data Store.

## 5. Which API capabilities are not necessarily customer-configurable?
**INFERENCE**: The API exposes a `THIRD_PARTY_FEDERATED` connector type, but there is no public UI or self-serve SDK for customers to register an arbitrary REST endpoint as a standard federated connector. Genuine federation is limited to pre-built native search platforms.
*Scope: Platform Config* | *Source: https://googleapis.dev/nodejs/discoveryengine/latest/google.cloud.discoveryengine.v1.html*
"""

scale_sync_content = """# Scale & Operations

## 1. Sync Reliability and Ingestion Quotas
**FACT**: When building custom connectors, the following hard quotas define the synchronization architecture:
- **GCS Batch Import Limits**: Up to 200 MB per file, max 100,000 files per import job.
- **Async Import Quota**: 5 requests per minute per project.
- **Batch Inline/Purge Quota**: 100 requests per minute per project.
*Source: https://cloud.google.com/generative-ai-app-builder/docs/quotas*

## 2. What happens when source data changes or is deleted?
**FACT**: In an ingestion architecture, a delta sync or explicit delete API call must be made to `projects/{project}/locations/global/collections/default_collection/dataStores/{datastore_id}/branches/0/documents/{doc_id}`.
**FACT**: Using `ImportDocuments(reconciliationMode = FULL)` automatically deletes documents that exist in the Data Store but are absent from the import source, providing a reliable cleanup mechanism.

## 3. What happens when a source API is unavailable?
**INFERENCE**:
- **Ingestion**: Gemini Enterprise falls back to the last known good index (Stale but highly available).
- **Federation / MCP**: Gemini Enterprise fails to retrieve context and the LLM must gracefully fallback.

## 4. Indexing Latency
**FACT**: Realtime direct upsert (`PatchDocument`) returns a synchronous API response, but the document enters a managed pipeline. Official documentation states indexing takes "seconds to hours."
*Source: https://cloud.google.com/generative-ai-app-builder/docs/prepare-data*
"""

with open('research/custom_connectors.md', 'w') as f:
    f.write(custom_connectors_content)

with open('research/scale_sync_strategies.md', 'w') as f:
    f.write(scale_sync_content)

print("Ingestion details successfully integrated.")
