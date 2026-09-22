# Gemini Enterprise Setup Runbook (PayCore Demo)

This runbook provisions a fresh Google Cloud project to support the Gemini Enterprise Custom MCP and Custom Ingestion demo. It explicitly honors the platform constraints documented in the research phase (e.g., `aclEnabled` immutability, Cloud Run `.run.app` requirement, and Org Policy blocks).

## PART 1 — ENVIRONMENT PREREQUISITES

| Requirement | Why needed | How to verify | Command |
| :--- | :--- | :--- | :--- |
| **GCP Project** | Resource boundary for Cloud Run and Discovery Engine. | Check active project. | `gcloud config get-value project` |
| **Billing Enabled** | Vertex AI and Cloud Run require an active billing account. | Check billing linkage. | `gcloud beta billing projects describe [PROJECT_ID]` |
| **Required APIs** | Discovery Engine (Gemini Enterprise), Cloud Run, Cloud Build. | Check enabled services. | `gcloud services list --enabled` |
| **IAM: Project Owner/Editor** | To deploy Cloud Run and provision Data Stores. | Check current user IAM. | `gcloud projects get-iam-policy [PROJECT_ID]` |
| **IAM: Org Policy Admin** | Required to override the MCP blocking constraint. | Check org-level IAM. | `gcloud organizations get-iam-policy [ORG_ID]` |
| **IAM: OAuth/IdP Admin** | Required to configure 3-legged OAuth in Entra/Workspace. | Console verification. | Access Workspace / Entra ID Admin Console |

*Reference: [Vertex AI Search Access Control](https://cloud.google.com/generative-ai-app-builder/docs/access-control)*

---

## PART 2 — GOOGLE CLOUD CLI SETUP

Execute these commands to prepare your local CLI. Replace placeholders `[PROJECT_ID]`, `[REGION]`, and `[USER_EMAIL]` with your environment specifics.

```bash
# 1. Authenticate gcloud (Log in to GCP)
gcloud auth login

# 2. Select project
gcloud config set project [PROJECT_ID]

# 3. Set region (e.g., us-central1)
gcloud config set compute/region [REGION]
gcloud config set run/region [REGION]

# 4. Verify active account
gcloud auth list

# 5. Verify project
gcloud config get-value project

# 6. Enable required APIs
gcloud services enable discoveryengine.googleapis.com run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com

# 7. Retrieve Project Number (Needed for Service Agent IAM)
PROJECT_NUMBER=$(gcloud projects describe [PROJECT_ID] --format="value(projectNumber)")
echo "Project Number: $PROJECT_NUMBER"
```

*Common Failure:* `403 Permission Denied` during API enablement. 
*Fix:* Ensure your account has the `roles/serviceusage.serviceUsageAdmin` or `roles/editor` role.

---

## PART 3 — ORGANIZATION POLICY

By default, Custom MCP servers are blocked globally. You must override `constraints/discoveryengine.managed.disableCustomMcpServerConnector`.
*Requirement:* `roles/orgpolicy.policyAdmin` at the Organization or Folder level. A Project Owner alone is **insufficient** if the org enforces it globally.

**1. Inspect the policy:**
```bash
gcloud org-policies describe constraints/discoveryengine.managed.disableCustomMcpServerConnector --project=[PROJECT_ID]
```

**2. Override the policy (Set enforce to false):**
```bash
cat <<EOF > mcp-policy.yaml
name: projects/[PROJECT_ID]/policies/discoveryengine.managed.disableCustomMcpServerConnector
spec:
  rules:
  - enforce: false
EOF

gcloud org-policies set-policy mcp-policy.yaml
```

*Reference: [Override constraint for custom MCP data stores](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/override-constraint-for-custom-mcp-data-stores)*

---

## PART 4 — CUSTOM MCP + CLOUD RUN

Deploy the FastMCP middleware to Cloud Run. It must retain the default `.run.app` URL for `X-Serverless-Authorization` to function.

```bash
# 1. Deploy directly from source using Buildpacks (No Dockerfile needed)
gcloud run deploy paycore-mcp \
  --source demo/custom_mcp/ \
  --region [REGION] \
  --allow-unauthenticated=false

# 2. Grant the Discovery Engine Service Agent Invoker permissions
# The service agent pattern is: service-[PROJECT_NUMBER]@gcp-sa-discoveryengine.iam.gserviceaccount.com
gcloud run services add-iam-policy-binding paycore-mcp \
  --region=[REGION] \
  --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-discoveryengine.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

# 3. Obtain the deployed URL
MCP_URL=$(gcloud run services describe paycore-mcp --platform managed --region [REGION] --format 'value(status.url)')
echo "MCP URL: $MCP_URL"
```

---

## PART 5 — CUSTOM MCP REGISTRATION IN GEMINI ENTERPRISE

**CONSOLE-ONLY STEP**
Currently, the Custom MCP Server data store registration flow requires the Google Cloud Console due to the 3-legged OAuth callback UI setup.

1. Navigate to **Agent Builder > Data Stores > Create Data Store**.
2. Select **Custom MCP Server** (If disabled, verify Part 3 Org Policy).
3. **Data Store Name**: `PayCore-Live`
4. **MCP Server URL**: Paste the `$MCP_URL` obtained in Part 4 (Must end in `.run.app/mcp`).
5. **Authentication**: Select `OAuth 2.0`.
   - Configure your IdP (e.g., Google Workspace) with the Redirect URI provided in the UI (`https://vertexaisearch.cloud.google.com/oauth-redirect`).
   - Enter `Client ID`, `Client Secret`, and `Authorization URL`.
6. Click **Create**.
7. Navigate to the **Actions** tab of the new Data Store and click **Reload custom actions** to invoke `tools/list`. Enable the `get_my_payroll_status` action.

---

## PART 6 — MCP AUTHENTICATION VERIFICATION

To verify the Gemini Enterprise identity propagation, capture the headers in Cloud Run logs:

```bash
# Query Cloud Run logs for the specific Custom MCP invocation
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="paycore-mcp" AND textPayload:"Authorization"' --limit 10
```

**Verification Checklist for Headers:**
- `X-Serverless-Authorization`: A Google-signed OIDC JWT. The `iss` will be `https://accounts.google.com` and the `aud` will be your Cloud Run URL. This authenticates the **Gemini Enterprise service agent**.
- `Authorization`: The OAuth Bearer token. The `iss` will be your enterprise IdP (e.g., Entra ID or Workspace). The payload will contain the **End User's identity** (e.g., `email: alice@demo.corp`).

---

## PART 7 — CUSTOM INGESTION + ACL

To contrast the Custom MCP with standard RAG ingestion, configure an ACL-enabled data store. 
*Note: `aclEnabled` and `identityMappingStore` are immutable at creation.*

```bash
# 1. Create Identity Mapping Store
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: [PROJECT_ID]" \
  "https://discoveryengine.googleapis.com/v1/projects/[PROJECT_ID]/locations/global/identityMappingStores?identityMappingStoreId=paycore-id-store" \
  -d '{}'

# 2. Create Data Store with ACL enabled
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: [PROJECT_ID]" \
  "https://discoveryengine.googleapis.com/v1/projects/[PROJECT_ID]/locations/global/collections/default_collection/dataStores?dataStoreId=paycore-ingestion-store" \
  -d '{
    "displayName": "PayCore Ingestion",
    "industryVertical": "GENERIC",
    "solutionTypes": ["SOLUTION_TYPE_SEARCH"],
    "aclEnabled": true,
    "identityMappingStore": "projects/[PROJECT_ID]/locations/global/identityMappingStores/paycore-id-store"
  }'
```

*Reference: [Data Source Access Control](https://cloud.google.com/generative-ai-app-builder/docs/access-control)*

---

## PART 8 — END-TO-END DEMO CHECKLIST

- [ ] GCP authenticated
- [ ] Project selected
- [ ] APIs enabled
- [ ] Org policy verified (`disableCustomMcpServerConnector` is false)
- [ ] MCP server deployed to Cloud Run
- [ ] Cloud Run IAM configured (`roles/run.invoker`)
- [ ] OAuth client configured in IdP
- [ ] MCP data store created in Console
- [ ] MCP connection healthy (`tools/list` succeeded)
- [ ] Alice authenticated in Gemini Chat
- [ ] Alice → Alice data works (Federated Live)
- [ ] Alice → Bob data rejected (Zero-trust middleware drop)
- [ ] Bob → Bob data works (Federated Live)
- [ ] Ingestion data store created (`aclEnabled: true`)
- [ ] Alice/Bob ACL test passed (Server-side document filtering)
- [ ] Freshness comparison demonstrated (Live vs Ingested lag)
- [ ] Cloud Run logs visible confirming headers

---

## PART 9 — TROUBLESHOOTING

| Error / Symptom | Likely cause | Diagnostic command | Fix |
| :--- | :--- | :--- | :--- |
| **gcloud auth fails** | Missing credentials or expired session | `gcloud auth list` | Run `gcloud auth login` |
| **API not enabled** | Billing not linked or permissions missing | `gcloud services list` | Link billing; run `gcloud services enable` |
| **Org policy blocked** | Missing Org Admin privileges | `gcloud org-policies describe...` | Request Org Admin to apply override |
| **Cloud Run 401/403** | Missing IAM or Custom Domain Drop | `gcloud run services get-iam-policy paycore-mcp` | Ensure `.run.app` URL is used; verify `run.invoker` role |
| **MCP tool registration fails** | StreamableHTTP/TLS failure | View Agent Builder console errors | Ensure Cloud Run endpoint is healthy and returns valid JSON-RPC |
| **Data Store creation fails** | Invalid JSON or disabled API | `curl -v ...` | Check JSON syntax; verify Discovery Engine API is active |
| **Ingestion exposes data** | `aclEnabled` is false or Identity Map broken | `curl .../dataStores/paycore-ingestion-store` | Recreate Data Store (cannot be patched); check identity entries |

---

## PART 10 — COST / CLEANUP

**Resources created:** Cloud Run service, Discovery Engine Data Stores, Identity Mapping Store, Artifact Registry Docker images.
**Charges:** Cloud Run incurs charges per request. Vertex AI Search / Discovery Engine incurs charges for indexing and querying.

**Cleanup commands:**
```bash
# Delete Cloud Run Service
gcloud run services delete paycore-mcp --region [REGION] --quiet

# Delete Data Store (API)
curl -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://discoveryengine.googleapis.com/v1/projects/[PROJECT_ID]/locations/global/collections/default_collection/dataStores/paycore-ingestion-store"

# Note: Custom MCP data stores should be deleted via the Google Cloud Console.
```
