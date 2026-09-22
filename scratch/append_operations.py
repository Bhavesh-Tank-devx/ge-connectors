import os

operations_updates = """
## 5. Connector Lifecycle and Observability
**FACT**: Connector syncs are managed by `ConnectorRun` jobs which transition through specific states: `PENDING` -> `RUNNING` -> `SUCCEEDED` / `FAILED` / `WARNING` / `SKIPPED` / `CANCELLED`.
**FACT**: If a scheduled run overlaps with an ongoing run (due to upstream rate limits causing backoff), the subsequent run is marked as `SKIPPED`.
**FACT**: All Discovery Engine operations push logs under `discoveryengine.googleapis.com`. Operations teams should configure Cloud Monitoring alerts for `severity>=ERROR`.

## 6. Failure Resilience
**FACT**: If the source API becomes permanently unavailable during an ingestion run, the `ConnectorRun` transitions to `FAILED`. However, the existing search index is **not** taken offline. Ongoing user queries continue to be served from the last known good index state (Zero-Downtime Query Serving).

## 7. Disaster Recovery (DR) and Backups
**FACT**: Data Stores do not provide automated 1-click snapshot-and-restore. DR relies on the Source of Truth pattern: triggering a full backfill (`ReconciliationMode = FULL`) from the primary source.
"""

with open('research/scale_sync_strategies.md', 'a') as f:
    f.write(operations_updates)

new_evidence = """| EVI-012 | Default 3P incremental sync is 3 hours (30m-7d); ACL refresh default is 30 mins (30m-7d). | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-013 | Initial connector crawl triggers approximately 1 hour after connector provisioning. | FACT | https://cloud.google.com/agent-builder/docs/about-third-party-data-sources |
| EVI-014 | `ReconciliationMode.INCREMENTAL` upserts by ID; `ReconciliationMode.FULL` purges missing documents with zero downtime. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1alpha/projects.locations.collections.dataStores.branches.documents/import#ReconciliationMode |
| EVI-015 | `ConnectorRun` lifecycle includes PENDING, RUNNING, SUCCEEDED, FAILED, WARNING, SKIPPED, CANCELLED. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1alpha/projects.locations.collections.dataConnector.connectorRuns#State |
| EVI-016 | Overlapping scheduled runs enter SKIPPED state if prior run is still ongoing. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1alpha/projects.locations.collections.dataConnector.connectorRuns |
| EVI-017 | Document write quota is 12,000 requests/minute/project; max data stores and engines are 500 per project. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/quotas |
| EVI-019 | Audit logs generated under `protoPayload.serviceName="discoveryengine.googleapis.com"`. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/audit-logging |
| EVI-021 | Data residency confined to `us` or `eu` multi-regions, including ML inference and tuning. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/locations |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("Scale & Operations Evidence and File Updates completed successfully.")
