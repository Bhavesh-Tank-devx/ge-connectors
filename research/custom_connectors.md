# Custom Connectors & Ingestion Architecture

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
