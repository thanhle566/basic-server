from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter()

OPENSEARCH_BASE_URL = "http://your-opensearch-host:9200"

@router.get("/opensearch/search")
async def search_opensearch(index: str = Query(...), q: str = Query("*")):
    url = f"{OPENSEARCH_BASE_URL}/{index}/_search"
    query = {
        "query": {
            "query_string": {
                "query": q
            }
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=query)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
