# Gemini Enterprise Data Connectivity Architecture

## 1. The Architectural Paradigm Shift
A frequent failure in enterprise LLM adoption is treating **Ingestion**, **Federation**, and **Custom MCP** as interchangeable "connectors". They operate in fundamentally different execution planes and carry distinct security trust models.

* **Ingestion**: Storage & Index Plane (Discovery Engine). Best for static/historical knowledge. Server-side ACLs.
* **Federation**: Distributed Query Proxy. Best for remote search engines (Drive, Jira). Zero duplication.
* **Custom MCP (Tooling)**: Agent Reasoning & Execution Plane. Best for transactional APIs, mutations, and zero-trust proxying.

## 2. Common Architectural Fallacies
- **Fallacy**: "Native connectors default to federation." 
  **Reality**: Native connectors (Jira, Salesforce, Confluence) strictly default to Ingestion (batch crawling).
- **Fallacy**: "The LLM will enforce data authorization based on system prompt."
  **Reality**: Security MUST NOT rely on LLM obedience. Authorization must be enforced deterministically at the data or middleware layer.
- **Fallacy**: "Custom MCP is fully GA."
  **Reality**: Custom MCP Server data stores are in Public Preview (July 2026).

## 3. The Target Architecture (Razorpay / PayCore Pattern)
For systems that use a single Org-level API key without per-user OAuth scoping (e.g., legacy ERPs, payroll systems), **Custom MCP** is the required architecture to ensure data isolation.

### Deterministic Multi-Boundary Isolation
```mermaid
flowchart TD
    subgraph Client_Domain ["Client Trust Domain"]
        User["Authenticated User (alice@demo.corp)"]
    end

    subgraph Google_Managed_Plane ["Google Cloud - Managed Gemini Enterprise"]
        GE_UI["Gemini Enterprise Portal / App"]
        GE_Engine["Gemini Reasoning Engine"]
    end

    subgraph Customer_GCP_Project ["Customer GCP Project (Isolated Boundary)"]
        subgraph Cloud_Run_Service ["Custom MCP Server (Cloud Run)"]
            Auth_Middleware["JWT Auth Middleware\n1. Validate Signature & Iss\n2. Extract User Email"]
            Identity_Mapper["Deterministic Identity Store\n(corp_email -> emp_id)"]
            Tool_Logic["Payroll Tool Logic\n(Injects verified emp_id ONLY)"]
        end
        SM[("Google Secret Manager\n(Org Master Key)")]
        VPC_Egress["Serverless VPC Access / Cloud NAT"]
    end

    subgraph Third_Party_Domain ["Third-Party Vendor Domain"]
        Mock_API["PayCore API\n(Org Key Auth Only)"]
    end

    User -->|1. Session| GE_UI
    GE_UI -->|2. Forward User OIDC Token| GE_Engine
    GE_Engine -->|3. POST /mcp with Auth| Auth_Middleware
    Auth_Middleware -->|4. Verified Email| Identity_Mapper
    Identity_Mapper -->|5. Resolved emp_id| Tool_Logic
    SM -.->|Fetch Key| Tool_Logic
    Tool_Logic -->|6. Call API with emp_id & Org Key| VPC_Egress
    VPC_Egress -->|7. TLS Outbound| Mock_API
    Mock_API -->|8. Filtered JSON| Tool_Logic
    Tool_Logic -->|9. Structured Result| GE_Engine
    GE_Engine -->|10. Answer| User
```

## 4. Architecture Decision Framework
1. **Require Real-Time Freshness?** -> Custom MCP
2. **Require Zero Data Duplication?** -> Custom MCP or Native Federation (if supported)
3. **Require Semantic RAG over Millions of Docs?** -> Ingestion
4. **Require Write Actions?** -> Custom MCP
