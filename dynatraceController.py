from fastapi import APIRouter, HTTPException
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

# Utility: Save data to file with timestamp and prefix
def save_to_file(data: dict, prefix: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = f"{prefix}_{timestamp}_{OUTPUT_FILE}"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dynatrace/metrics")
async def get_and_save_metrics():
    url = f"{DYNATRACE_BASE_URL}/api/v2/metrics"

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
async def get_and_save_problems():
    url = f"{DYNATRACE_BASE_URL}/api/v2/problems"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    file_path = save_to_file(data, "problems")

    return {
        "message": "Problems data retrieved and saved",
        "file": file_path,
        "record_count": len(data.get("problems", []))  # Adjust if needed
    }

@router.get("/dynatrace/events")
async def get_and_save_events():
    url = f"{DYNATRACE_BASE_URL}/api/v2/events"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    file_path = save_to_file(data, "events")

    return {
        "message": "Events data retrieved and saved",
        "file": file_path,
        "record_count": len(data.get("events", []))  # Adjust if needed
    }

@router.get("/dynatrace/topology")
async def get_and_save_topology():
    url = f"{DYNATRACE_BASE_URL}/api/v2/entities"

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