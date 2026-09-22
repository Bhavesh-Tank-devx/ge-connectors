from fastapi import FastAPI, Header, HTTPException

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
