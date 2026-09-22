import os

new_evidence = """| EVI-001 | Custom MCP Server receives the end user's OAuth token in `Authorization` and the Gemini service agent ID token in `X-Serverless-Authorization`. | FACT | https://cloud.google.com/run/docs/authenticating/service-to-service |
| EVI-002 | Gemini Enterprise Custom MCP requires `StreamableHTTP` transport; SSE is unsupported. Requires CA-signed TLS. | FACT | https://cloud.google.com/gemini/docs/enterprise/ |
| EVI-003 | Custom MCP Server data store is currently in **Public Preview** (as of mid-2026) and requires an Org Policy override. | FACT | https://cloud.google.com/gemini/docs/enterprise/ |
| EVI-004 | Discovery Engine `DataStore.aclEnabled` is **immutable** and must be specified at data store creation time. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/projects.locations.collections.dataStores |
| EVI-005 | Identity Mapping Stores map Google Cloud / corporate identities to 3P identifiers via `externalEntityId`. | FACT | https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1/projects.locations.identityMappingStores |
| EVI-008 | A2A (Agent-to-Agent) agent registration in Gemini Enterprise is subject to Pre-GA Offerings Terms. | FACT | https://cloud.google.com/vertex-ai/docs/agent-builder/a2a |
| EVI-009 | ADK `tool_context.session.user_id` is caller-supplied and not cryptographically verifiable by agent tools. | COMMUNITY REPORT / FACT | https://github.com/google/adk-python |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("Razorpay Case Study Evidence appended successfully.")
