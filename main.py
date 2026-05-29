from fastapi.responses import HTMLResponse
from fastapi import FastAPI
import redis
import uuid
import json

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.post("/jobs")
def create_job(payload: dict, priority: str = "normal"):
    job_id = str(uuid.uuid4())
    job_data = {
        "id": job_id,
        "status": "pending",
        "payload": payload,
        "retries": 0,
        "priority": priority
    }
    queue_name = f"job_queue_{priority}"
    r.lpush(queue_name, json.dumps(job_data))
    r.set(f"job:{job_id}", json.dumps(job_data))
    return {"job_id": job_id, "status": "pending", "priority": priority}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    data = r.get(f"job:{job_id}")
    if not data:
        return {"error": "not found"}
    return json.loads(data)
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("dashboard.html") as f:
        return f.read()
