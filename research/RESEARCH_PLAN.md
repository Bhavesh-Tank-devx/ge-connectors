# Research Plan

This document outlines the detailed research program for the Gemini Enterprise Connector POC.

## Master Research Matrix

| Topic | Question | Primary source | Secondary source | Hands-on validation | Status | Open question |
|---|---|---|---|---|---|---|
| Native Connectors | What is the exact catalog of GA and Preview native connectors in Gemini Enterprise? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Custom Connectors | How does Gemini Enterprise ingest data from unsupported third-party sources (Document API vs UI-based)? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Ingestion | How is data permanently indexed and stored inside Gemini Enterprise? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Federation | How does Gemini Enterprise query external systems in real-time? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| End-User Authentication (EUA) | How does Gemini Enterprise assert the identity of the human asking the question? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Access Control Lists | How does Gemini Enterprise restrict access to specific ingested documents based on the user? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Identity Mapping | How do we map a Google Cloud Identity to a disparate third-party identity (e.g., Jira User ID, Razorpay Employee ID)? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Actions | Can Gemini Enterprise connectors perform write operations (mutations)? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Custom MCP | What is the exact specification and capability of the Custom MCP Server in Gemini Enterprise? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Authentication and Authorization | How are system-to-system and user-to-system auth handled across the architecture? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Networking and Private Connectivity | How does Gemini Enterprise connect to on-premise or VPC-enclosed data sources? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Synchronization, Freshness, and Scale | What are the scale limits for ingested documents and the freshness guarantees? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Lifecycle, Observability, and Operations | How do we monitor connector health, query latency, and sync failures? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Connector Limitations and Availability | What are the specific GA / Preview / Private Preview statuses of all architectural components? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Razorpay Case Study | How do we apply the researched patterns to the constraint of Razorpay's org-level API key lacking per-user auth? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Agentic Integration (ADK & A2A) | How do ADK and A2A patterns compare to Custom MCP for data connectivity? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |
| Security and Failure Modes | What are the attack vectors for Gemini Enterprise connectors? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |

---

## 1. Native connectors

**A. Research questions:** What is the exact catalog of GA and Preview native connectors in Gemini Enterprise? Which capabilities are universal vs source-specific (e.g. Jira vs Salesforce)?

**B. Sub-questions:** Are native connectors managed exclusively by Google? Who handles API updates and token refresh? What is the pricing model?

**C. Terminology:** Native Connector, Managed Data Source, Prebuilt Connector.

**D. Primary sources:** Gemini Enterprise data sources documentation, Google Cloud release notes, Terraform Registry (`google_discovery_engine_data_store`).

**E. Secondary/community sources:** Google Cloud community forums, third-party vendor integration pages.

**F. Evidence sufficient:** Official documentation listing the connector in the Google Cloud console or API reference.

**G. Facts NOT to infer:** Do not infer that a native connector for Service X supports all objects/APIs of Service X. Do not infer that API existence means customer-configurability.

**H. Likely ambiguities / traps:** Assuming native connectors are federated; many are actually ingestion-based.

**I. Expected architecture diagrams:** System boundary showing Google managing the polling/sync infrastructure.

**J. Questions for final presentation:** When should a customer choose a native connector over building a custom one?

**K. Hands-on vs Documentary:** Documentary: catalog availability. Hands-on: Setup UI flow for a single native connector.

## 2. Custom connectors

**A. Research questions:** How does Gemini Enterprise ingest data from unsupported third-party sources (Document API vs UI-based)?

**B. Sub-questions:** Does the UI support webhook/push, or only polling? What are the API quotas for the Custom Connector API?

**C. Terminology:** Custom Connector, Data Store, Document API.

**D. Primary sources:** Vertex AI Search / Gemini Enterprise Custom Document API reference.

**E. Secondary/community sources:** GitHub `googleapis` repo, community blogs on custom ingestion.

**F. Evidence sufficient:** API reference showing endpoint paths, payload schemas, and explicit support for push/webhook.

**G. Facts NOT to infer:** Do not infer that custom connectors support real-time querying (federation).

**H. Likely ambiguities / traps:** Confusing Vertex AI Search custom data stores with Gemini Enterprise Custom MCP.

**I. Expected architecture diagrams:** Ingestion pipeline (Cloud Run/Functions) pushing to Gemini Data Store.

**J. Questions for final presentation:** What is the operational burden of a custom connector?

**K. Hands-on vs Documentary:** Hands-on: Pushing a mock document via API.

## 3. Ingestion

**A. Research questions:** How is data permanently indexed and stored inside Gemini Enterprise?

**B. Sub-questions:** How are deletions handled? Is there a concept of partial updates? What is the maximum document size?

**C. Terminology:** Batch Indexing, Document API, Chunking.

**D. Primary sources:** Gemini indexing limits documentation.

**E. Secondary/community sources:** StackOverflow discussions on Vertex indexing delays.

**F. Evidence sufficient:** Documented quota limits and indexing latency SLAs.

**G. Facts NOT to infer:** Do not infer that ingestion happens synchronously with the API response.

**H. Likely ambiguities / traps:** Delay between API 200 OK and data appearing in search results.

**I. Expected architecture diagrams:** Data flow from source -> extraction -> transformation -> ingestion -> Gemini Index.

**J. Questions for final presentation:** What is the freshness lag for ingested data?

**K. Hands-on vs Documentary:** Hands-on: Measure time between API push and LLM retrieval.

## 4. Federation

**A. Research questions:** How does Gemini Enterprise query external systems in real-time? How does it differ from iPaaS / Hybrid patterns?

**B. Sub-questions:** What is the timeout limit for a federated query? How are results chunked/paginated?

**C. Terminology:** Federated Search, Live Query, Custom MCP.

**D. Primary sources:** Gemini Enterprise Custom MCP / Federated Data Sources docs.

**E. Secondary/community sources:** GitHub issues regarding timeout or connection drops in federated agents.

**F. Evidence sufficient:** Explicit documentation on federated query SLA and timeout values.

**G. Facts NOT to infer:** Do not infer that federated sources can be used for RAG grounding in the exact same way as indexed sources.

**H. Likely ambiguities / traps:** Latency issues causing the LLM to hallucinate or fallback.

**I. Expected architecture diagrams:** Real-time query routing from Gemini -> Connector -> Source -> Gemini.

**J. Questions for final presentation:** What are the performance implications of federation vs ingestion?

**K. Hands-on vs Documentary:** Hands-on: Implementing a Custom MCP server and observing latency.

## 5. EUA / end-user authentication

**A. Research questions:** How does Gemini Enterprise assert the identity of the human asking the question?

**B. Sub-questions:** Which Identity Providers (IdPs) are supported? How is the identity session managed?

**C. Terminology:** EUA, Cloud Identity, Workforce Identity Federation, 3-legged OAuth.

**D. Primary sources:** Google Cloud Identity and Gemini Enterprise authentication docs.

**E. Secondary/community sources:** Reddit/StackOverflow on integrating Okta/Entra ID with Gemini.

**F. Evidence sufficient:** Documentation on identity token structures passed to the runtime.

**G. Facts NOT to infer:** Do not infer that EUA automatically maps to third-party system identities.

**H. Likely ambiguities / traps:** Assuming `tool_context.session.user_id` is cryptographically secure without verification.

**I. Expected architecture diagrams:** User login flow: User -> IdP -> GCP -> Gemini Enterprise.

**J. Questions for final presentation:** How do we prove the user is who they claim to be to the connector?

**K. Hands-on vs Documentary:** Hands-on: Inspecting the headers/tokens sent to a Custom MCP server.

## 6. ACLs

**A. Research questions:** How does Gemini Enterprise restrict access to specific ingested documents based on the user?

**B. Sub-questions:** Are ACLs evaluated at index time or query time? Are they retrofittable? Are group-level and inherited ACLs supported?

**C. Terminology:** ACL, Reader Principal, Document Visibility, Group-based ACL.

**D. Primary sources:** Vertex AI Search / Gemini Data Store ACL configuration docs.

**E. Secondary/community sources:** Security whitepapers, community implementations of ACLs.

**F. Evidence sufficient:** API examples showing the `acl_info` schema and group mapping limitations.

**G. Facts NOT to infer:** Do not infer that changing an ACL immediately propagates to the index.

**H. Likely ambiguities / traps:** The inability to change a data store's ACL mode after creation.

**I. Expected architecture diagrams:** Query execution path showing identity matching against Document ACL metadata.

**J. Questions for final presentation:** Can one user see another user's data? (Prove it's impossible).

**K. Hands-on vs Documentary:** Hands-on: Ingesting a document with an ACL and querying it with two different users.

## 7. Identity mapping

**A. Research questions:** How do we map a Google Cloud Identity to a disparate third-party identity (e.g., Jira User ID, Razorpay Employee ID)?

**B. Sub-questions:** Where is the mapping stored? How is it kept in sync? Does Google provide a managed mapping service?

**C. Terminology:** Identity Mapping Store, Principal ID, External Entity ID.

**D. Primary sources:** Google Cloud IAM / Identity mapping docs, Connector specific ACL docs.

**E. Secondary/community sources:** Enterprise integration blogs (e.g., mapping Entra ID to custom apps).

**F. Evidence sufficient:** Architecture patterns for identity resolution at query time.

**G. Facts NOT to infer:** Do not infer that email addresses always match between systems.

**H. Likely ambiguities / traps:** Handling user lifecycle events (onboarding/offboarding).

**I. Expected architecture diagrams:** Lookup flow: GCP Identity -> Database -> 3rd Party ID -> Target System.

**J. Questions for final presentation:** Where is the identity mapping stored and who is responsible for its accuracy?

**K. Hands-on vs Documentary:** Hands-on: Simulating a mapping table lookup inside a Custom MCP server.

## 8. Actions

**A. Research questions:** Can Gemini Enterprise connectors perform write operations (mutations)?

**B. Sub-questions:** How is user consent gathered before a destructive action? Are actions synchronous?

**C. Terminology:** Agent Actions, Tool Calling, Mutations.

**D. Primary sources:** Gemini Enterprise / Agent Runtime tool calling docs.

**E. Secondary/community sources:** GitHub `google/adk-python` examples of tool usage.

**F. Evidence sufficient:** Code samples showing action definition and execution.

**G. Facts NOT to infer:** Do not infer that all read connectors automatically support write actions.

**H. Likely ambiguities / traps:** Preventing LLM hallucinations from triggering unintended destructive writes.

**I. Expected architecture diagrams:** Action flow: Prompt -> LLM plans action -> User confirmation -> Execution.

**J. Questions for final presentation:** How do we safely implement write capabilities?

**K. Hands-on vs Documentary:** Hands-on: Creating a safe, read-only action vs a mutation action.

## 9. Custom MCP

**A. Research questions:** What is the exact specification and capability of the Custom MCP Server in Gemini Enterprise?

**B. Sub-questions:** Does configuring the endpoint require a Google support ticket / whitelist? How are OAuth tokens forwarded?

**C. Terminology:** MCP, Authorization Header, X-Serverless-Authorization.

**D. Primary sources:** Gemini Custom MCP Server documentation.

**E. Secondary/community sources:** Anthropic/Google MCP community discussions, GitHub MCP specs.

**F. Evidence sufficient:** Official documentation detailing exact HTTP headers, payload schemas, and UI/API configuration paths.

**G. Facts NOT to infer:** Do not infer that Custom MCP is identical to standard open-source MCP without checking Google's implementation.

**H. Likely ambiguities / traps:** Assuming Custom MCP handles token refresh for the third party.

**I. Expected architecture diagrams:** Gemini Enterprise -> HTTP POST with OAuth token -> Custom MCP Cloud Run -> 3rd Party API.

**J. Questions for final presentation:** What makes Custom MCP different/better than standard ADK tools?

**K. Hands-on vs Documentary:** Hands-on: Deploying a basic Cloud Run MCP server and echoing headers.

## 10. Authentication and authorization

**A. Research questions:** How are system-to-system and user-to-system auth handled across the architecture?

**B. Sub-questions:** What are the roles of Service Accounts vs User Identity Delegation? How is the Agent Engine authenticated?

**C. Terminology:** Service Agent, 3-legged OAuth, Delegation, OIDC.

**D. Primary sources:** Google Cloud IAM, Agent Identity OAuth docs.

**E. Secondary/community sources:** Security audits, GCP IAM blogs.

**F. Evidence sufficient:** IAM policy configurations and token validation logic.

**G. Facts NOT to infer:** Do not conflate the identity of the Agent with the identity of the User.

**H. Likely ambiguities / traps:** Misunderstanding when to use a Service Account vs passing the user's token.

**I. Expected architecture diagrams:** Complete Auth Flow diagram distinguishing system boundaries.

**J. Questions for final presentation:** How is the zero-trust boundary maintained between components?

**K. Hands-on vs Documentary:** Documentary: Validate IAM roles. Hands-on: Token validation in code.

## 11. Networking / private connectivity

**A. Research questions:** How does Gemini Enterprise connect to on-premise or VPC-enclosed data sources?

**B. Sub-questions:** Does it support egress controls via VPC Service Controls (VPC-SC) or Private Service Connect (PSC)?

**C. Terminology:** VPC-SC, PSC egress, Serverless VPC Access.

**D. Primary sources:** Google Cloud VPC, Gemini Enterprise networking docs.

**E. Secondary/community sources:** Network engineering blogs, GCP Reddit.

**F. Evidence sufficient:** Supported network topologies explicitly documented for Gemini Enterprise egress.

**G. Facts NOT to infer:** Do not infer that public APIs support VPC-SC automatically.

**H. Likely ambiguities / traps:** Agent Runtime IP ranges changing dynamically and breaking firewall rules.

**I. Expected architecture diagrams:** Network topology map showing private routing from Gemini to the data source.

**J. Questions for final presentation:** How do we secure data in transit for private sources?

**K. Hands-on vs Documentary:** Documentary: Map out the required PSC endpoints and firewall rules.

## 12. Synchronization / freshness / scale

**A. Research questions:** What are the scale limits for ingested documents and the freshness guarantees?

**B. Sub-questions:** What is the max QPS? How do we handle millions of documents? How are delta syncs performed?

**C. Terminology:** Delta Sync, Full Sync, QPS, Quota vs Hard Limit.

**D. Primary sources:** Quotas and Limits documentation for Gemini Enterprise.

**E. Secondary/community sources:** Enterprise architecture case studies.

**F. Evidence sufficient:** Hard quota numbers from GCP console/docs.

**G. Facts NOT to infer:** Do not infer that a connector handles delta syncs natively unless documented.

**H. Likely ambiguities / traps:** API rate limits on the third-party source breaking the sync pipeline.

**I. Expected architecture diagrams:** Data pipeline architecture for high-throughput ingestion.

**J. Questions for final presentation:** How will this scale to 100,000 employees?

**K. Hands-on vs Documentary:** Documentary: Calculate theoretical max throughput based on quotas.

## 13. Connector lifecycle / observability / operations

**A. Research questions:** How do we monitor connector health, query latency, and sync failures?

**B. Sub-questions:** What logs are pushed to Cloud Logging? Does it support Cloud Trace? How are alerts configured?

**C. Terminology:** Cloud Logging, Cloud Trace, Error Reporting.

**D. Primary sources:** Google Cloud operations suite docs for Gemini Enterprise.

**E. Secondary/community sources:** SRE best practices for agent observability.

**F. Evidence sufficient:** Documented log payload structures.

**G. Facts NOT to infer:** Do not infer that prompt-response logs contain PII by default.

**H. Likely ambiguities / traps:** Missing failed queries due to lack of alerting on MCP timeouts.

**I. Expected architecture diagrams:** Observability architecture showing metrics/logs flow.

**J. Questions for final presentation:** How does the operations team know if the connector is broken?

**K. Hands-on vs Documentary:** Hands-on: Triggering a failure and checking Cloud Logging.

## 14. Connector-specific limitations and product availability

**A. Research questions:** What are the specific GA / Preview / Private Preview statuses of all architectural components?

**B. Sub-questions:** Are there regional restrictions? What is customer-configurable vs partner/provider-only?

**C. Terminology:** Pre-GA, Private Preview, Org Policy Override.

**D. Primary sources:** Google Cloud Release Notes, Pre-GA terms, Admin console.

**E. Secondary/community sources:** Community whispers on release timelines.

**F. Evidence sufficient:** Explicit status badges in official docs.

**G. Facts NOT to infer:** Do not infer global availability if a feature is only in us-central1.

**H. Likely ambiguities / traps:** Building a production design on a Private Preview feature.

**I. Expected architecture diagrams:** N/A - Table of feature availability.

**J. Questions for final presentation:** Is this architecture ready for production today?

**K. Hands-on vs Documentary:** Documentary: Verify statuses in console.

## 15. Razorpay case study

**A. Research questions:** How do we apply the researched patterns to the constraint of Razorpay's org-level API key lacking per-user auth?

**B. Sub-questions:** How do we securely simulate the org-key isolation? Does Custom MCP securely isolate cross-user queries?

**C. Terminology:** Org-level API Key, Case Study.

**D. Primary sources:** Razorpay API docs, compiled Gemini Enterprise research.

**E. Secondary/community sources:** None (synthesis of primary research).

**F. Evidence sufficient:** Successful execution of POC demo scenarios without data leakage.

**G. Facts NOT to infer:** Do not infer Razorpay's rate limits from Google's quotas.

**H. Likely ambiguities / traps:** Razorpay API changes or unhandled edge cases in employee IDs.

**I. Expected architecture diagrams:** Final POC Architecture diagram (Custom MCP vs Ingestion).

**J. Questions for final presentation:** Does the POC successfully prove the security model to the audience?

**K. Hands-on vs Documentary:** Hands-on: Execute cross-user impersonation tests to ensure isolation.

## 16. Agentic Integration (ADK & A2A)

**A. Research questions:** How do ADK and A2A patterns compare to Custom MCP for data connectivity?

**B. Sub-questions:** Can an agent (ADK/A2A) act as a viable 'connector'? How does its auth boundary differ from Custom MCP?

**C. Terminology:** A2A, Agent-to-Agent, ADK, Agent Engine.

**D. Primary sources:** ADK documentation, Agent Registry docs.

**E. Secondary/community sources:** GitHub `google/adk-python` discussions.

**F. Evidence sufficient:** Clear architectural comparison of invocation paths and auth forwarding.

**G. Facts NOT to infer:** Do not infer that ADK agents automatically receive verified user identities.

**H. Likely ambiguities / traps:** Assuming A2A is GA or ready for production without checking terms.

**I. Expected architecture diagrams:** A2A routing vs Custom MCP routing diagrams.

**J. Questions for final presentation:** Why choose a Custom MCP server over building a standalone ADK agent?

**K. Hands-on vs Documentary:** Hands-on: Test user identity injection in an ADK tool.

## 17. Security and Failure Modes

**A. Research questions:** What are the attack vectors for Gemini Enterprise connectors?

**B. Sub-questions:** What are the risks of Prompt Injection bypassing connector filtering? Can a Custom MCP suffer from SSRF?

**C. Terminology:** Prompt Injection, SSRF, Token Exfiltration.

**D. Primary sources:** Google Cloud security whitepapers.

**E. Secondary/community sources:** OWASP for LLMs, community security writeups.

**F. Evidence sufficient:** Documented mitigations or acknowledged risks.

**G. Facts NOT to infer:** Do not infer that the LLM automatically filters unauthorized data returned by the connector.

**H. Likely ambiguities / traps:** Trusting the LLM to apply ACLs rather than enforcing them at the data layer.

**I. Expected architecture diagrams:** Threat model diagram.

**J. Questions for final presentation:** How do we defend against a malicious user attempting to extract another's payslip via Prompt Injection?

**K. Hands-on vs Documentary:** Hands-on: Attempt prompt injection to bypass Razorpay filters.

