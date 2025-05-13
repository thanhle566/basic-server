from fastapi import FastAPI, HTTPException
import httpx
import os
from datetime import datetime

app = FastAPI()

# Load from env or config in production
DYNATRACE_API_TOKEN = os.getenv("DYNATRACE_API_TOKEN", "YOUR_DYNATRACE_API_TOKEN")
DYNATRACE_BASE_URL = "https://{your-environment-id}.live.dynatrace.com"
OUTPUT_FILE = "dynatrace_output.json"

HEADERS = {
    "Authorization": f"Api-Token {DYNATRACE_API_TOKEN}"
}

@app.get("/dynatrace/metrics")
async def get_and_save_metrics():
    url = f"{DYNATRACE_BASE_URL}/api/v2/metrics"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    # Optional: timestamp the output file
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = f"{timestamp}_{OUTPUT_FILE}"

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Data retrieved and saved",
        "file": file_path,
        "record_count": len(data.get("metrics", []))  # if you're calling metrics API
    }
