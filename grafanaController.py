from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter()

GRAFANA_BASE_URL = "http://your-grafana-host:3000"
GRAFANA_API_KEY = "YOUR_GRAFANA_API_KEY"
HEADERS = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}"
}

@router.get("/grafana/search")
async def search_grafana_dashboards(query: str = Query("")):
    url = f"{GRAFANA_BASE_URL}/api/search?query={query}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
