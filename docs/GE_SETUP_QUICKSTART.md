# Gemini Enterprise Setup Quickstart

Minimum commands needed to provision the Gemini Enterprise environment for the PayCore demo. 

Replace placeholders before running.

```bash
# 1. Auth and Config
gcloud auth login
gcloud config set project [PROJECT_ID]
gcloud config set run/region [REGION]

# 2. Enable APIs
gcloud services enable discoveryengine.googleapis.com run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

# 3. Org Policy Override (Requires Org Admin)
cat <<EOF > mcp-policy.yaml
name: projects/[PROJECT_ID]/policies/discoveryengine.managed.disableCustomMcpServerConnector
spec:
  rules:
  - enforce: false
EOF
gcloud org-policies set-policy mcp-policy.yaml

# 4. Deploy Custom MCP to Cloud Run
gcloud run deploy paycore-mcp \
  --source demo/custom_mcp/ \
  --allow-unauthenticated=false

# 5. Grant IAM to Gemini Service Agent
PROJECT_NUMBER=$(gcloud projects describe [PROJECT_ID] --format="value(projectNumber)")

gcloud run services add-iam-policy-binding paycore-mcp \
  --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-discoveryengine.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

MCP_URL=$(gcloud run services describe paycore-mcp --platform managed --format 'value(status.url)')
echo "MCP URL to register in console: $MCP_URL"

# 6. Create Identity Mapping & Ingestion Store (For ACL Comparison)
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" "https://discoveryengine.googleapis.com/v1/projects/[PROJECT_ID]/locations/global/identityMappingStores?identityMappingStoreId=paycore-id-store" -d '{}'

curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" "https://discoveryengine.googleapis.com/v1/projects/[PROJECT_ID]/locations/global/collections/default_collection/dataStores?dataStoreId=paycore-ingestion-store" -d '{"displayName": "PayCore Ingestion", "industryVertical": "GENERIC", "solutionTypes": ["SOLUTION_TYPE_SEARCH"], "aclEnabled": true, "identityMappingStore": "projects/[PROJECT_ID]/locations/global/identityMappingStores/paycore-id-store"}'
```

**Next Steps:**
Go to the **Vertex AI Agent Builder Console** to register `$MCP_URL` as a Custom MCP Data Store. (Console-only step due to OAuth callback configuration).
