import pytest
from brand_monitor_mcp.app.tools import tools
from unittest.mock import AsyncMock, patch, MagicMock
from brand_monitor_mcp.app.agents import agent

@pytest.mark.asyncio
@patch("brand_monitor_mcp.app.agents.agent.MCPToolset.from_server")
async def test_search_twitter_mcp(mock_from_server):
    mock_tool = AsyncMock()
    mock_tool.name = "get_twitter"
    mock_tool.run_async = AsyncMock(return_value="{'data': [{'text': 'Tweet mock'}]}")
    mock_from_server.return_value = ([mock_tool], AsyncMock())

    result = await agent.search_twitter("OpenAI")
    assert isinstance(result, str)
    assert "Tweet mock" in result


@pytest.mark.asyncio
@patch("brand_monitor_mcp.app.agents.agent.MCPToolset.from_server")
async def test_search_google_mcp(mock_from_server):
    mock_tool = AsyncMock()
    mock_tool.name = "get_google"
    mock_tool.run_async = AsyncMock(return_value="- News A — https://link.com")
    mock_from_server.return_value = ([mock_tool], AsyncMock())

    result = await agent.search_google("OpenAI")
    assert isinstance(result, str)
    assert "News A" in result


@pytest.mark.asyncio
@patch("brand_monitor_mcp.app.agents.agent.MCPToolset.from_server")
async def test_search_tavily_mcp(mock_from_server):
    mock_tool = AsyncMock()
    mock_tool.name = "get_tavily"
    mock_tool.run_async = AsyncMock(return_value="Title: News Tavily - URL: https://tavily - Text: content")
    mock_from_server.return_value = ([mock_tool], AsyncMock())

    result = await agent.search_tavily("OpenAI")
    assert isinstance(result, str)
    assert "News Tavily" in result
    assert "URL:" in result
    

@patch("brand_monitor_mcp.app.tools.requests.get")
def test_search_twitter(mock_get):
    mock_resp = MagicMock()
    mock_resp.text = '{"data": [{"text": "tweet 1"}]}'
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    result = tools.search_twitter("OpenAI")
    assert isinstance(result, str)
    assert "tweet 1" in result


@patch("brand_monitor_mcp.app.tools.requests.get")
def test_search_google(mock_get):
    mock_xml = """<?xml version="1.0"?>
        <rss>
          <channel>
            <item>
              <title>Google News 1</title>
              <link>https://link1.com</link>
            </item>
          </channel>
        </rss>"""
    mock_resp = MagicMock()
    mock_resp.content = mock_xml.encode("utf-8")
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    result = tools.search_google("OpenAI")
    assert isinstance(result, str)
    assert "Google News 1" in result


@patch("brand_monitor_mcp.app.tools.TavilyClient.search")
def test_search_tavily(mock_search):
    mock_search.return_value = {
        "results": [
            {
                "title": "Tavily Title",
                "url": "https://tavily.com",
                "content": "Important news"
            }
        ]
    }

    result = tools.search_tavily("OpenAI")
    assert isinstance(result, str)
    assert "Tavily Title" in result
    assert "URL:" in result
