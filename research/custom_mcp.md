# Custom MCP (Model Context Protocol)

## 1. What are Actions?
**FACT**: Actions are function calls / tools that allow the LLM to mutate state or retrieve live context dynamically.

## 2. How does Custom MCP differ from a Custom Connector?
**FACT**: A Custom Connector ingests data into a static GCP search index. A Custom MCP is a live, HTTP-based middleware server that exposes tools directly to the Agent execution plane.
*Source: https://cloud.google.com/release-notes (July 2026 Preview)*

## 3. When should MCP be used instead of a connector?
**INFERENCE**: MCP should be used when data freshness must be immediate, when zero data replication is mandated, or when the use case requires actions/mutations (e.g., creating a ticket).

## 4. Prerequisites for Custom MCP
**FACT**: Custom MCP Server data stores are gated by Google Cloud Organization Policies. To deploy, an Org Policy Administrator must set `constraints/discoveryengine.managed.disableCustomMcpServerConnector` to **Off** and add `custom_mcp` to `constraints/discoveryengine.managed.allowedDataSources`.
**FACT**: The MCP transport protocol is strictly restricted to `StreamableHTTP`. The server must possess a valid TLS certificate from a publicly trusted CA (internal CAs are blocked in the public console registration).

## 5. Critical Deployment Constraints (As of Aug 2026)
**FACT**: **The `.run.app` Requirement**: Gemini Enterprise only injects the `X-Serverless-Authorization` token if the target URL uses the default Cloud Run `*.run.app` domain. If mapped to a custom domain, the token is not sent, breaking Cloud Run IAM.
**FACT**: **User Confirmation Prompts**: By default, Gemini treats all MCP actions as potentially destructive and prompts the user for confirmation. To bypass this for read-only queries (like checking a payslip), developers must explicitly annotate the MCP tool with `readOnlyHint: True` and `destructiveHint: False`.
**FACT**: **Action Limits & TLS**: A single Custom MCP data store is hard-limited to 100 enabled actions. The endpoint must use a publicly trusted TLS certificate (internal/private CAs are rejected).
