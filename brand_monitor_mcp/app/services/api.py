from requests.exceptions import HTTPError
from fastapi import FastAPI, Query, HTTPException
from fastapi_mcp import FastApiMCP
from ..tools.tools import search_google, search_tavily, search_twitter 

app = FastAPI()

@app.get("/get_twitter_mentions", operation_id="get_twitter_mentions" )
async def get_twitter_mentions(query: str = Query(..., description="Company name (e.g. Nubank)")):
    try:
        return search_twitter(query)
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/get_tavily_results", operation_id="get_tavily" )
async def get_tavily_results(query: str = Query(..., description="Company name (e.g. Nubank)")):
    try:
        return search_tavily(query)
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.get("/get_google_news", operation_id="get_google_news" )
async def get_google_news(query: str = Query(..., description="Company name (e.g. Nubank)")):
    try:
        return search_google(query)
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

mcp = FastApiMCP(
    app,
    name="Get Twitter Mentions, Tavily and Google News.",
    description="This MCP server creates functions for Getting the Twitter Mentions and News about a Brand.",
    # base_url="http://localhost:8001",
)
mcp.mount()