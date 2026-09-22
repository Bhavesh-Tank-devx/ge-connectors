import os

custom_mcp_updates = """
## 5. Critical Deployment Constraints (As of Aug 2026)
**FACT**: **The `.run.app` Requirement**: Gemini Enterprise only injects the `X-Serverless-Authorization` token if the target URL uses the default Cloud Run `*.run.app` domain. If mapped to a custom domain, the token is not sent, breaking Cloud Run IAM.
**FACT**: **User Confirmation Prompts**: By default, Gemini treats all MCP actions as potentially destructive and prompts the user for confirmation. To bypass this for read-only queries (like checking a payslip), developers must explicitly annotate the MCP tool with `readOnlyHint: True` and `destructiveHint: False`.
**FACT**: **Action Limits & TLS**: A single Custom MCP data store is hard-limited to 100 enabled actions. The endpoint must use a publicly trusted TLS certificate (internal/private CAs are rejected).
"""

with open('research/custom_mcp.md', 'a') as f:
    f.write(custom_mcp_updates)

new_evidence = """| EVI-MCP-01 | In MCP spec, capabilities are "tools"; in Gemini Enterprise data stores, they are "actions" (interchangeable). | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-02 | StreamableHTTP transport is exclusively supported; SSE transport is not supported. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-03 | Public and private MCP servers must have TLS signed by a publicly trusted CA. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-04 | Requests send user OAuth token in `Authorization` and Discovery Engine service agent ID token in `X-Serverless-Authorization`. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-05 | `X-Serverless-Authorization` is only automatically sent to default `.run.app` URLs, not custom domains. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-06 | Service agent requires `roles/run.invoker` (`service-<NUM>@gcp-sa-discoveryengine.iam.gserviceaccount.com`). | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-08 | Maximum of 100 enabled actions per custom MCP server data store. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-09 | Actions require user confirmation by default; bypassed with `readOnlyHint: True` and `destructiveHint: False`. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server |
| EVI-MCP-10 | Creation blocked by `constraints/discoveryengine.managed.disableCustomMcpServerConnector`. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/override-constraint-for-custom-mcp-data-stores |
| EVI-MCP-12 | Custom MCP server data store released in Public Preview on April 28, 2026. | FACT | https://docs.cloud.google.com/gemini/enterprise/docs/release-notes |
"""

with open('research/EVIDENCE_INDEX.md', 'a') as f:
    f.write(new_evidence)

print("Custom MCP Evidence and deployment constraints updated successfully.")
