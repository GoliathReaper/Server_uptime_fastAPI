from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

app = FastAPI()

uptime_logs: Dict[str, List[dict]] = {}

class UptimeLog(BaseModel):
    server_id: str
    timestamp: datetime
    status: bool

@app.post("/log_uptime")
async def log_uptime(log: UptimeLog):
    if log.server_id not in uptime_logs:
        uptime_logs[log.server_id] = []
    uptime_logs[log.server_id].append(log.dict())
    return {"message": "Log added successfully"}

@app.get("/uptime/{server_id}")
async def get_uptime(server_id: str):
    if server_id not in uptime_logs:
        raise HTTPException(status_code=404, detail="Server not found")

    logs = uptime_logs[server_id]
    total_checks = len(logs)
    successful_checks = len([log for log in logs if log["status"]])
    uptime_percentage = (successful_checks / total_checks) * 100 if total_checks > 0 else 0
    return {
        "server_id": server_id,
        "total_checks": total_checks,
        "successful_checks": successful_checks,
        "uptime_percentage": uptime_percentage,
        "logs": logs
    }

@app.get("/uptime")
async def get_all_uptime():
    results = []
    for server_id, logs in uptime_logs.items():
        total_checks = len(logs)
        successful_checks = len([log for log in logs if log["status"]])
        uptime_percentage = (successful_checks / total_checks) * 100 if total_checks > 0 else 0
        results.append({
            "server_id": server_id,
            "total_checks": total_checks,
            "successful_checks": successful_checks,
            "uptime_percentage": uptime_percentage,
            "logs": logs
        })
    return results
