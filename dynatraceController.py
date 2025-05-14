from fastapi import APIRouter, HTTPException, Request
import httpx
import os
from datetime import datetime
import json

router = APIRouter()

# Load from env or config in production
DYNATRACE_API_TOKEN = os.getenv("DYNATRACE_API_TOKEN", "YOUR_DYNATRACE_API_TOKEN")
DYNATRACE_BASE_URL = "https://{your-environment-id}.live.dynatrace.com"
OUTPUT_FILE = "dynatrace_output.json"

HEADERS = {
    "Authorization": f"Api-Token {DYNATRACE_API_TOKEN}"
}

def save_to_file(data: dict, prefix: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = f"{prefix}_{timestamp}_{OUTPUT_FILE}"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def build_url(base: str, path: str, query_params: dict) -> str:
    if query_params:
        query_string = "&".join(f"{key}={value}" for key, value in query_params.items())
        return f"{base}{path}?{query_string}"
    return f"{base}{path}"


@router.get("/dynatrace/metrics")
async def get_metrics(request: Request):
    url = build_url(DYNATRACE_BASE_URL, "/api/v2/metrics", dict(request.query_params))

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    file_path = save_to_file(data, "metrics")

    return {
        "message": "Metrics data retrieved and saved",
        "file": file_path,
        "record_count": len(data.get("metrics", []))
    }


@router.get("/dynatrace/problems")
async def get_problems(request: Request):
    url = build_url(DYNATRACE_BASE_URL, "/api/v2/problems", dict(request.query_params))

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    file_path = save_to_file(data, "problems")

    return {
        "message": "Problems data retrieved and saved",
        "file": file_path,
        "record_count": len(data.get("problems", []))
    }


@router.get("/dynatrace/events")
async def get_events(request: Request):
    url = build_url(DYNATRACE_BASE_URL, "/api/v2/events", dict(request.query_params))

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    file_path = save_to_file(data, "events")

    return {
        "message": "Events data retrieved and saved",
        "file": file_path,
        "record_count": len(data.get("events", []))
    }


@router.get("/dynatrace/topology")
async def get_topology(request: Request):
    url = build_url(DYNATRACE_BASE_URL, "/api/v2/entities", dict(request.query_params))

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    file_path = save_to_file(data, "topology")

    return {
        "message": "Topology data retrieved and saved",
        "file": file_path,
        "record_count": len(data.get("entities", []))
    }