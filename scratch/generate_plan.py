import os

TRACKS_DATA = [
    {
        "title": "1. Native connectors",
        "topic": "Native Connectors",
        "A": "What is the exact catalog of GA and Preview native connectors in Gemini Enterprise? Which capabilities are universal vs source-specific (e.g. Jira vs Salesforce)?",
        "B": "Are native connectors managed exclusively by Google? Who handles API updates and token refresh? What is the pricing model?",
        "C": "Native Connector, Managed Data Source, Prebuilt Connector.",
        "D": "Gemini Enterprise data sources documentation, Google Cloud release notes, Terraform Registry (`google_discovery_engine_data_store`).",
        "E": "Google Cloud community forums, third-party vendor integration pages.",
        "F": "Official documentation listing the connector in the Google Cloud console or API reference.",
        "G": "Do not infer that a native connector for Service X supports all objects/APIs of Service X. Do not infer that API existence means customer-configurability.",
        "H": "Assuming native connectors are federated; many are actually ingestion-based.",
        "I": "System boundary showing Google managing the polling/sync infrastructure.",
        "J": "When should a customer choose a native connector over building a custom one?",
        "K": "Documentary: catalog availability. Hands-on: Setup UI flow for a single native connector."
    },
    {
        "title": "2. Custom connectors",
        "topic": "Custom Connectors",
        "A": "How does Gemini Enterprise ingest data from unsupported third-party sources (Document API vs UI-based)?",
        "B": "Does the UI support webhook/push, or only polling? What are the API quotas for the Custom Connector API?",
        "C": "Custom Connector, Data Store, Document API.",
        "D": "Vertex AI Search / Gemini Enterprise Custom Document API reference.",
        "E": "GitHub `googleapis` repo, community blogs on custom ingestion.",
        "F": "API reference showing endpoint paths, payload schemas, and explicit support for push/webhook.",
        "G": "Do not infer that custom connectors support real-time querying (federation).",
        "H": "Confusing Vertex AI Search custom data stores with Gemini Enterprise Custom MCP.",
        "I": "Ingestion pipeline (Cloud Run/Functions) pushing to Gemini Data Store.",
        "J": "What is the operational burden of a custom connector?",
        "K": "Hands-on: Pushing a mock document via API."
    },
    {
        "title": "3. Ingestion",
        "topic": "Ingestion",
        "A": "How is data permanently indexed and stored inside Gemini Enterprise?",
        "B": "How are deletions handled? Is there a concept of partial updates? What is the maximum document size?",
        "C": "Batch Indexing, Document API, Chunking.",
        "D": "Gemini indexing limits documentation.",
        "E": "StackOverflow discussions on Vertex indexing delays.",
        "F": "Documented quota limits and indexing latency SLAs.",
        "G": "Do not infer that ingestion happens synchronously with the API response.",
        "H": "Delay between API 200 OK and data appearing in search results.",
        "I": "Data flow from source -> extraction -> transformation -> ingestion -> Gemini Index.",
        "J": "What is the freshness lag for ingested data?",
        "K": "Hands-on: Measure time between API push and LLM retrieval."
    },
    {
        "title": "4. Federation",
        "topic": "Federation",
        "A": "How does Gemini Enterprise query external systems in real-time? How does it differ from iPaaS / Hybrid patterns?",
        "B": "What is the timeout limit for a federated query? How are results chunked/paginated?",
        "C": "Federated Search, Live Query, Custom MCP.",
        "D": "Gemini Enterprise Custom MCP / Federated Data Sources docs.",
        "E": "GitHub issues regarding timeout or connection drops in federated agents.",
        "F": "Explicit documentation on federated query SLA and timeout values.",
        "G": "Do not infer that federated sources can be used for RAG grounding in the exact same way as indexed sources.",
        "H": "Latency issues causing the LLM to hallucinate or fallback.",
        "I": "Real-time query routing from Gemini -> Connector -> Source -> Gemini.",
        "J": "What are the performance implications of federation vs ingestion?",
        "K": "Hands-on: Implementing a Custom MCP server and observing latency."
    },
    {
        "title": "5. EUA / end-user authentication",
        "topic": "End-User Authentication (EUA)",
        "A": "How does Gemini Enterprise assert the identity of the human asking the question?",
        "B": "Which Identity Providers (IdPs) are supported? How is the identity session managed?",
        "C": "EUA, Cloud Identity, Workforce Identity Federation, 3-legged OAuth.",
        "D": "Google Cloud Identity and Gemini Enterprise authentication docs.",
        "E": "Reddit/StackOverflow on integrating Okta/Entra ID with Gemini.",
        "F": "Documentation on identity token structures passed to the runtime.",
        "G": "Do not infer that EUA automatically maps to third-party system identities.",
        "H": "Assuming `tool_context.session.user_id` is cryptographically secure without verification.",
        "I": "User login flow: User -> IdP -> GCP -> Gemini Enterprise.",
        "J": "How do we prove the user is who they claim to be to the connector?",
        "K": "Hands-on: Inspecting the headers/tokens sent to a Custom MCP server."
    },
    {
        "title": "6. ACLs",
        "topic": "Access Control Lists",
        "A": "How does Gemini Enterprise restrict access to specific ingested documents based on the user?",
        "B": "Are ACLs evaluated at index time or query time? Are they retrofittable? Are group-level and inherited ACLs supported?",
        "C": "ACL, Reader Principal, Document Visibility, Group-based ACL.",
        "D": "Vertex AI Search / Gemini Data Store ACL configuration docs.",
        "E": "Security whitepapers, community implementations of ACLs.",
        "F": "API examples showing the `acl_info` schema and group mapping limitations.",
        "G": "Do not infer that changing an ACL immediately propagates to the index.",
        "H": "The inability to change a data store's ACL mode after creation.",
        "I": "Query execution path showing identity matching against Document ACL metadata.",
        "J": "Can one user see another user's data? (Prove it's impossible).",
        "K": "Hands-on: Ingesting a document with an ACL and querying it with two different users."
    },
    {
        "title": "7. Identity mapping",
        "topic": "Identity Mapping",
        "A": "How do we map a Google Cloud Identity to a disparate third-party identity (e.g., Jira User ID, Razorpay Employee ID)?",
        "B": "Where is the mapping stored? How is it kept in sync? Does Google provide a managed mapping service?",
        "C": "Identity Mapping Store, Principal ID, External Entity ID.",
        "D": "Google Cloud IAM / Identity mapping docs, Connector specific ACL docs.",
        "E": "Enterprise integration blogs (e.g., mapping Entra ID to custom apps).",
        "F": "Architecture patterns for identity resolution at query time.",
        "G": "Do not infer that email addresses always match between systems.",
        "H": "Handling user lifecycle events (onboarding/offboarding).",
        "I": "Lookup flow: GCP Identity -> Database -> 3rd Party ID -> Target System.",
        "J": "Where is the identity mapping stored and who is responsible for its accuracy?",
        "K": "Hands-on: Simulating a mapping table lookup inside a Custom MCP server."
    },
    {
        "title": "8. Actions",
        "topic": "Actions",
        "A": "Can Gemini Enterprise connectors perform write operations (mutations)?",
        "B": "How is user consent gathered before a destructive action? Are actions synchronous?",
        "C": "Agent Actions, Tool Calling, Mutations.",
        "D": "Gemini Enterprise / Agent Runtime tool calling docs.",
        "E": "GitHub `google/adk-python` examples of tool usage.",
        "F": "Code samples showing action definition and execution.",
        "G": "Do not infer that all read connectors automatically support write actions.",
        "H": "Preventing LLM hallucinations from triggering unintended destructive writes.",
        "I": "Action flow: Prompt -> LLM plans action -> User confirmation -> Execution.",
        "J": "How do we safely implement write capabilities?",
        "K": "Hands-on: Creating a safe, read-only action vs a mutation action."
    },
    {
        "title": "9. Custom MCP",
        "topic": "Custom MCP",
        "A": "What is the exact specification and capability of the Custom MCP Server in Gemini Enterprise?",
        "B": "Does configuring the endpoint require a Google support ticket / whitelist? How are OAuth tokens forwarded?",
        "C": "MCP, Authorization Header, X-Serverless-Authorization.",
        "D": "Gemini Custom MCP Server documentation.",
        "E": "Anthropic/Google MCP community discussions, GitHub MCP specs.",
        "F": "Official documentation detailing exact HTTP headers, payload schemas, and UI/API configuration paths.",
        "G": "Do not infer that Custom MCP is identical to standard open-source MCP without checking Google's implementation.",
        "H": "Assuming Custom MCP handles token refresh for the third party.",
        "I": "Gemini Enterprise -> HTTP POST with OAuth token -> Custom MCP Cloud Run -> 3rd Party API.",
        "J": "What makes Custom MCP different/better than standard ADK tools?",
        "K": "Hands-on: Deploying a basic Cloud Run MCP server and echoing headers."
    },
    {
        "title": "10. Authentication and authorization",
        "topic": "Authentication and Authorization",
        "A": "How are system-to-system and user-to-system auth handled across the architecture?",
        "B": "What are the roles of Service Accounts vs User Identity Delegation? How is the Agent Engine authenticated?",
        "C": "Service Agent, 3-legged OAuth, Delegation, OIDC.",
        "D": "Google Cloud IAM, Agent Identity OAuth docs.",
        "E": "Security audits, GCP IAM blogs.",
        "F": "IAM policy configurations and token validation logic.",
        "G": "Do not conflate the identity of the Agent with the identity of the User.",
        "H": "Misunderstanding when to use a Service Account vs passing the user's token.",
        "I": "Complete Auth Flow diagram distinguishing system boundaries.",
        "J": "How is the zero-trust boundary maintained between components?",
        "K": "Documentary: Validate IAM roles. Hands-on: Token validation in code."
    },
    {
        "title": "11. Networking / private connectivity",
        "topic": "Networking and Private Connectivity",
        "A": "How does Gemini Enterprise connect to on-premise or VPC-enclosed data sources?",
        "B": "Does it support egress controls via VPC Service Controls (VPC-SC) or Private Service Connect (PSC)?",
        "C": "VPC-SC, PSC egress, Serverless VPC Access.",
        "D": "Google Cloud VPC, Gemini Enterprise networking docs.",
        "E": "Network engineering blogs, GCP Reddit.",
        "F": "Supported network topologies explicitly documented for Gemini Enterprise egress.",
        "G": "Do not infer that public APIs support VPC-SC automatically.",
        "H": "Agent Runtime IP ranges changing dynamically and breaking firewall rules.",
        "I": "Network topology map showing private routing from Gemini to the data source.",
        "J": "How do we secure data in transit for private sources?",
        "K": "Documentary: Map out the required PSC endpoints and firewall rules."
    },
    {
        "title": "12. Synchronization / freshness / scale",
        "topic": "Synchronization, Freshness, and Scale",
        "A": "What are the scale limits for ingested documents and the freshness guarantees?",
        "B": "What is the max QPS? How do we handle millions of documents? How are delta syncs performed?",
        "C": "Delta Sync, Full Sync, QPS, Quota vs Hard Limit.",
        "D": "Quotas and Limits documentation for Gemini Enterprise.",
        "E": "Enterprise architecture case studies.",
        "F": "Hard quota numbers from GCP console/docs.",
        "G": "Do not infer that a connector handles delta syncs natively unless documented.",
        "H": "API rate limits on the third-party source breaking the sync pipeline.",
        "I": "Data pipeline architecture for high-throughput ingestion.",
        "J": "How will this scale to 100,000 employees?",
        "K": "Documentary: Calculate theoretical max throughput based on quotas."
    },
    {
        "title": "13. Connector lifecycle / observability / operations",
        "topic": "Lifecycle, Observability, and Operations",
        "A": "How do we monitor connector health, query latency, and sync failures?",
        "B": "What logs are pushed to Cloud Logging? Does it support Cloud Trace? How are alerts configured?",
        "C": "Cloud Logging, Cloud Trace, Error Reporting.",
        "D": "Google Cloud operations suite docs for Gemini Enterprise.",
        "E": "SRE best practices for agent observability.",
        "F": "Documented log payload structures.",
        "G": "Do not infer that prompt-response logs contain PII by default.",
        "H": "Missing failed queries due to lack of alerting on MCP timeouts.",
        "I": "Observability architecture showing metrics/logs flow.",
        "J": "How does the operations team know if the connector is broken?",
        "K": "Hands-on: Triggering a failure and checking Cloud Logging."
    },
    {
        "title": "14. Connector-specific limitations and product availability",
        "topic": "Connector Limitations and Availability",
        "A": "What are the specific GA / Preview / Private Preview statuses of all architectural components?",
        "B": "Are there regional restrictions? What is customer-configurable vs partner/provider-only?",
        "C": "Pre-GA, Private Preview, Org Policy Override.",
        "D": "Google Cloud Release Notes, Pre-GA terms, Admin console.",
        "E": "Community whispers on release timelines.",
        "F": "Explicit status badges in official docs.",
        "G": "Do not infer global availability if a feature is only in us-central1.",
        "H": "Building a production design on a Private Preview feature.",
        "I": "N/A - Table of feature availability.",
        "J": "Is this architecture ready for production today?",
        "K": "Documentary: Verify statuses in console."
    },
    {
        "title": "15. Razorpay case study",
        "topic": "Razorpay Case Study",
        "A": "How do we apply the researched patterns to the constraint of Razorpay's org-level API key lacking per-user auth?",
        "B": "How do we securely simulate the org-key isolation? Does Custom MCP securely isolate cross-user queries?",
        "C": "Org-level API Key, Case Study.",
        "D": "Razorpay API docs, compiled Gemini Enterprise research.",
        "E": "None (synthesis of primary research).",
        "F": "Successful execution of POC demo scenarios without data leakage.",
        "G": "Do not infer Razorpay's rate limits from Google's quotas.",
        "H": "Razorpay API changes or unhandled edge cases in employee IDs.",
        "I": "Final POC Architecture diagram (Custom MCP vs Ingestion).",
        "J": "Does the POC successfully prove the security model to the audience?",
        "K": "Hands-on: Execute cross-user impersonation tests to ensure isolation."
    },
    {
        "title": "16. Agentic Integration (ADK & A2A)",
        "topic": "Agentic Integration (ADK & A2A)",
        "A": "How do ADK and A2A patterns compare to Custom MCP for data connectivity?",
        "B": "Can an agent (ADK/A2A) act as a viable 'connector'? How does its auth boundary differ from Custom MCP?",
        "C": "A2A, Agent-to-Agent, ADK, Agent Engine.",
        "D": "ADK documentation, Agent Registry docs.",
        "E": "GitHub `google/adk-python` discussions.",
        "F": "Clear architectural comparison of invocation paths and auth forwarding.",
        "G": "Do not infer that ADK agents automatically receive verified user identities.",
        "H": "Assuming A2A is GA or ready for production without checking terms.",
        "I": "A2A routing vs Custom MCP routing diagrams.",
        "J": "Why choose a Custom MCP server over building a standalone ADK agent?",
        "K": "Hands-on: Test user identity injection in an ADK tool."
    },
    {
        "title": "17. Security and Failure Modes",
        "topic": "Security and Failure Modes",
        "A": "What are the attack vectors for Gemini Enterprise connectors?",
        "B": "What are the risks of Prompt Injection bypassing connector filtering? Can a Custom MCP suffer from SSRF?",
        "C": "Prompt Injection, SSRF, Token Exfiltration.",
        "D": "Google Cloud security whitepapers.",
        "E": "OWASP for LLMs, community security writeups.",
        "F": "Documented mitigations or acknowledged risks.",
        "G": "Do not infer that the LLM automatically filters unauthorized data returned by the connector.",
        "H": "Trusting the LLM to apply ACLs rather than enforcing them at the data layer.",
        "I": "Threat model diagram.",
        "J": "How do we defend against a malicious user attempting to extract another's payslip via Prompt Injection?",
        "K": "Hands-on: Attempt prompt injection to bypass Razorpay filters."
    }
]

def generate_research_plan():
    content = "# Research Plan\n\nThis document outlines the detailed research program for the Gemini Enterprise Connector POC.\n\n"
    content += "## Master Research Matrix\n\n"
    content += "| Topic | Question | Primary source | Secondary source | Hands-on validation | Status | Open question |\n"
    content += "|---|---|---|---|---|---|---|\n"
    for track in TRACKS_DATA:
        content += f"| {track['topic']} | {track['A'].split('?')[0]}? | Docs / APIs / TF | Blogs / Forums | TBD | NOT STARTED | None yet |\n"
    content += "\n---\n\n"
    for track in TRACKS_DATA:
        content += f"## {track['title']}\n\n"
        content += f"**A. Research questions:** {track['A']}\n\n"
        content += f"**B. Sub-questions:** {track['B']}\n\n"
        content += f"**C. Terminology:** {track['C']}\n\n"
        content += f"**D. Primary sources:** {track['D']}\n\n"
        content += f"**E. Secondary/community sources:** {track['E']}\n\n"
        content += f"**F. Evidence sufficient:** {track['F']}\n\n"
        content += f"**G. Facts NOT to infer:** {track['G']}\n\n"
        content += f"**H. Likely ambiguities / traps:** {track['H']}\n\n"
        content += f"**I. Expected architecture diagrams:** {track['I']}\n\n"
        content += f"**J. Questions for final presentation:** {track['J']}\n\n"
        content += f"**K. Hands-on vs Documentary:** {track['K']}\n\n"
    with open("research/RESEARCH_PLAN.md", "w") as f:
        f.write(content)

def generate_search_queries():
    content = "# Source Search Queries\n\nPrecise search queries for executing the research plan.\n\n"
    for track in TRACKS_DATA:
        topic = track['topic']
        content += f"## {track['title']}\n\n"
        content += f"- **Official Google Docs:** `site:cloud.google.com/docs/gemini \"{topic}\" (architecture OR configuration OR limits)`\n"
        content += f"- **Google API/Reference:** `site:cloud.google.com/docs/reference gemini \"{topic}\" (REST OR RPC OR payload)`\n"
        content += f"- **Google Release Notes:** `site:cloud.google.com/release-notes \"Gemini Enterprise\" \"{topic}\"`\n"
        content += f"- **Google Cloud Blogs:** `site:cloud.google.com/blog \"Gemini\" \"{topic}\" (connector OR integration)`\n"
        content += f"- **Vendor Documentation:** `\"{topic}\" integration \"Gemini Enterprise\" OR \"Agentspace\"`\n"
        content += f"- **GitHub:** `org:google repo:adk-python \"{topic}\" OR \"Gemini Enterprise\"`\n"
        content += f"- **Terraform Registry:** `site:registry.terraform.io/providers/hashicorp/google/latest/docs \"Gemini\" OR \"discovery_engine\" \"{topic}\"`\n"
        content += f"- **Reddit:** `site:reddit.com/r/googlecloud \"Gemini Enterprise\" \"{topic}\"`\n"
        content += f"- **X/Community:** `\"Gemini Enterprise\" \"{topic}\" (issue OR limitation OR howto)`\n\n"
    with open("research/SOURCE_SEARCH_QUERIES.md", "w") as f:
        f.write(content)

if __name__ == "__main__":
    generate_research_plan()
    generate_search_queries()
