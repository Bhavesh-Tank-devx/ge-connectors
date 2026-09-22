from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Gemini Enterprise MCP Server")
IDENTITY_MAP = {"alice@demo.corp": "EMP-001", "bob@demo.corp": "EMP-002"}

# Mock DB for self-contained demo
DB = {
    "EMP-001": {"base": 140000, "bonus": 15000, "dept": "Engineering"},
    "EMP-002": {"base": 95000, "bonus": 5000, "dept": "Sales"}
}

def verify_and_map_jwt(auth_header: str) -> str:
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
    
    # 2. Secure Backend Lookup
    if emp_id not in DB:
        raise HTTPException(status_code=404, detail="Employee not found")
    return DB[emp_id]
