import re

with open('demo/README.md', 'r') as f:
    content = f.read()

# Add validation section
validation_section = """
## Live Environment Validation Results (Sept 2026)
**STATUS:** PARTIALLY VERIFIED LOCALLY. GCP ENVIRONMENT NOT AVAILABLE.

The following elements have been tested in the local architecture:
1. **PayCore Security Test (Custom MCP Middleware)**: **VERIFIED**. Simulated Alice and Bob requests confirm that the authorization decision is deterministic and made entirely by the server-side middleware extracting the identity from the `Authorization` header. A simulated malicious LLM payload (attempting to request Bob's data while authenticated as Alice) securely returns Alice's data because the LLM is physically incapable of injecting an employee ID into the retrieval layer.

The following elements are **DOCUMENTED BUT NOT HANDS-ON VERIFIED** due to a lack of provisioned Gemini Enterprise environment access:
1. **Custom MCP Authentication Path End-to-End**: Cannot verify the exact structure of the `Authorization` and `X-Serverless-Authorization` tokens as sent by a live Gemini Agent.
2. **Custom MCP Prerequisites**: Cannot live-test the Org Policy override (`disableCustomMcpServerConnector`), Cloud Run IAM `roles/run.invoker`, or StreamableHTTP over public CA TLS.
3. **Ingestion Path (Server-Side ACLs)**: Cannot test the actual Google Cloud `documents.patch` or `documents.import` with `aclInfo` readers to verify chunk-level LLM filtering.

**Exact Blockers:**
- No provisioned Google Cloud Project.
- No Vertex AI Agent Builder / Discovery Engine billing API enabled.
- `gcloud` requires password reauthentication.

**Exact Steps Required for the Live Presentation:**
1. Authenticate `gcloud` and enable the Discovery Engine API.
2. An Org Admin must apply the Org Policy override for `disableCustomMcpServerConnector`.
3. Deploy `paycore_mock.py` and `server.py` to Cloud Run (must use `.run.app` default URLs).
4. Register the Custom MCP data store in the Vertex AI Search console, providing the Cloud Run URL and configuring the OAuth Client ID.
5. Provide the Discovery Engine Service Agent the `roles/run.invoker` role on the `server.py` Cloud Run deployment.
6. Create an Ingestion Data Store with `aclEnabled: true` and an Identity Mapping Store, then run the python sync script (to be built) to import the mock payroll chunks.
"""

with open('demo/README.md', 'a') as f:
    f.write("\n" + validation_section)
print("Updated demo/README.md")
