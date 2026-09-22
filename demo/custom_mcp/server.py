from fastapi import FastAPI, Header, HTTPException
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
