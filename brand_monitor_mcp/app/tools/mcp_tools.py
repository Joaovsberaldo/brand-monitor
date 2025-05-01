from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

MCP_URL = "http://localhost:8001/mcp"

# Tools
async def search_twitter(company_name: str, **kwargs) -> str:
    """
    Proxy for the 'search_twitter_mentions' tool from MCP.
    Returns: A JSON string with the 'data' field, a list with each mention.
    """
    tx = kwargs.get("tx")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(url=MCP_URL, headers={})
    )
    async with exit_stack:
        tool = next(t for t in tools if t.name == "get_twitter")
        return await tool.run_async(
            args={"company_name": company_name},
            tool_context=tx
        )

async def search_google(company_name: str, **kwargs) -> str:
    """
    Proxy for the 'search_google_news' tool from MCP.
    Returns: Returns a string with news about the search term.
    """
    tx = kwargs.get("tx")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(url=MCP_URL, headers={})
    )
    async with exit_stack:
        tool = next(t for t in tools if t.name == "get_google")
        return await tool.run_async(
            args={"company_name": company_name},
            tool_context=tx
        )
        
async def search_tavily(company_name: str, **kwargs) -> str:
    """
    Proxy for the 'search_tavily_results' tool from MCP.
    
    Returns:
        A text containing the top 10 news about the search term.
        This text contains the topics: title, url, and text.
    """
    tx = kwargs.get("tx")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(url=MCP_URL, headers={})
    )
    async with exit_stack:
        tool = next(t for t in tools if t.name == "get_tavily")
        return await tool.run_async(
            args={"company_name": company_name},
            tool_context=tx
        )
