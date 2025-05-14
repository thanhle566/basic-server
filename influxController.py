from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter()

INFLUX_BASE_URL = "http://your-influxdb-host:8086"
INFLUX_TOKEN = "YOUR_INFLUX_TOKEN"
INFLUX_ORG = "your-org"

HEADERS = {
    "Authorization": f"Token {INFLUX_TOKEN}",
    "Content-Type": "application/vnd.flux"
}

@router.post("/influx/query")
async def query_influxdb(query: str = Query(..., description="Flux query to execute")):
    url = f"{INFLUX_BASE_URL}/api/v2/query?org={INFLUX_ORG}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HEADERS, content=query)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
