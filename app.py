# app.py
# Compatible with Python 3.7 + FastAPI (<0.100) + Pydantic (<2)
# Exposes:
#   GET  /healthz
#   POST /patients  { "name": "...", "dob": "YYYY-MM-DD", "conditions": ["..."] }
#   GET  /patients/{pid}
#   GET  /metrics   (Prometheus format)
#   GET  /          -> redirects to /docs
#   GET  /favicon.ico -> 204 No Content

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Dict
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest
import time
import threading

app = FastAPI(title="Mini EMR (Py3.7 Compatible)")

# ----- Models -----
class Patient(BaseModel):
    name: str
    dob: str                   # ISO date string in demo (YYYY-MM-DD)
    conditions: List[str] = []

# ----- In-memory "DB" (demo only!) -----
DB_LOCK = threading.Lock()
DB: Dict[int, Patient] = {}
NEXT_ID = 1

# ----- Metrics -----
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds"
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)

    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start

    try:
        REQUEST_LATENCY.observe(elapsed)
        REQUEST_COUNT.labels(
            method=request.method,
            path=request.url.path,
            status=str(response.status_code)
        ).inc()
    except Exception:
        pass

    return response

# ----- Endpoints -----
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/patients")
def create_patient(p: Patient):
    global NEXT_ID
    with DB_LOCK:
        pid = NEXT_ID
        DB[pid] = p
        NEXT_ID += 1
    return {"id": pid, **p.dict()}

@app.get("/patients/{pid}")
def get_patient(pid: int):
    with DB_LOCK:
        patient = DB.get(pid)
    if not patient:
        raise HTTPException(status_code=404, detail="not found")
    return {"id": pid, **patient.dict()}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# ----- Friendly root & favicon -----
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)
