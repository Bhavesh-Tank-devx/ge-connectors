import os

FILES = {}

FILES['docs/architecture_presentation.md'] = """# Gemini Enterprise Data Connectivity Architecture

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
            Auth_Middleware["JWT Auth Middleware\\n1. Validate Signature & Iss\\n2. Extract User Email"]
            Identity_Mapper["Deterministic Identity Store\\n(corp_email -> emp_id)"]
            Tool_Logic["Payroll Tool Logic\\n(Injects verified emp_id ONLY)"]
        end
        SM[("Google Secret Manager\\n(Org Master Key)")]
        VPC_Egress["Serverless VPC Access / Cloud NAT"]
    end

    subgraph Third_Party_Domain ["Third-Party Vendor Domain"]
        Mock_API["PayCore API\\n(Org Key Auth Only)"]
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
"""

FILES['demo/custom_connectors/paycore_mock.py'] = """from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="PayCore Mock API")
ORG_KEY = "sec_org_test_998124"

DB = {
    "EMP-001": {"base": 140000, "bonus": 15000, "dept": "Engineering"},
    "EMP-002": {"base": 95000, "bonus": 5000, "dept": "Sales"}
}

@app.get("/api/v1/employees/{emp_id}/payroll")
def get_payroll(emp_id: str, x_paycore_api_key: str = Header(None)):
    if x_paycore_api_key != ORG_KEY:
        raise HTTPException(status_code=403, detail="Invalid Org API Key")
    if emp_id not in DB:
        raise HTTPException(status_code=404, detail="Employee not found")
    return DB[emp_id]
"""

FILES['demo/custom_mcp/server.py'] = """from fastapi import FastAPI, Header, HTTPException
import httpx

app = FastAPI(title="Gemini Enterprise MCP Server")
IDENTITY_MAP = {"alice@demo.corp": "EMP-001", "bob@demo.corp": "EMP-002"}
PAYCORE_URL = "http://localhost:8000/api/v1/employees/{}/payroll"

def verify_and_map_jwt(auth_header: str) -> str:
    # MOCK: In production, verify JWT signature against GCP JWKS and extract email
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    email = auth_header.split(" ")[1] 
    if email not in IDENTITY_MAP:
        raise HTTPException(403, f"Token principal {email} not authorized")
    return IDENTITY_MAP[email]

@app.post("/mcp/tools/get_my_payroll_status")
def get_payroll_status(authorization: str = Header(None)):
    # 1. Zero-Trust Identity Mapping
    emp_id = verify_and_map_jwt(authorization)
    
    # 2. Secure Backend Call (Never pass LLM parameters as the emp_id)
    headers = {"X-PayCore-Api-Key": "sec_org_test_998124"}
    resp = httpx.get(PAYCORE_URL.format(emp_id), headers=headers)
    return resp.json()
"""

os.makedirs('docs', exist_ok=True)
os.makedirs('demo/custom_connectors', exist_ok=True)
os.makedirs('demo/custom_mcp', exist_ok=True)
os.makedirs('demo/ingestion_scripts', exist_ok=True)

for path, content in FILES.items():
    with open(path, 'w') as f:
        f.write(content)

print("Final presentation and demo codebase successfully generated.")
