# Scale & Operations

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

## 5. Connector Lifecycle and Observability
**FACT**: Connector syncs are managed by `ConnectorRun` jobs which transition through specific states: `PENDING` -> `RUNNING` -> `SUCCEEDED` / `FAILED` / `WARNING` / `SKIPPED` / `CANCELLED`.
**FACT**: If a scheduled run overlaps with an ongoing run (due to upstream rate limits causing backoff), the subsequent run is marked as `SKIPPED`.
**FACT**: All Discovery Engine operations push logs under `discoveryengine.googleapis.com`. Operations teams should configure Cloud Monitoring alerts for `severity>=ERROR`.

## 6. Failure Resilience
**FACT**: If the source API becomes permanently unavailable during an ingestion run, the `ConnectorRun` transitions to `FAILED`. However, the existing search index is **not** taken offline. Ongoing user queries continue to be served from the last known good index state (Zero-Downtime Query Serving).

## 7. Disaster Recovery (DR) and Backups
**FACT**: Data Stores do not provide automated 1-click snapshot-and-restore. DR relies on the Source of Truth pattern: triggering a full backfill (`ReconciliationMode = FULL`) from the primary source.
