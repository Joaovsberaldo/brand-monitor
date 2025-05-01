import pytest
from ..app.agents.search import (
    news_agent, 
    twitter_agent, 
    tavily_agent, 
    fetch_data_agent, 
    format_search_agent, 
    search_agent)
from ..app.agents.analytics import analyze_agent
from ..app.agents.report import report_agent

@pytest.mark.asyncio
async def test_news_agent_properties():
    assert news_agent.name == "NewsAgent"
    assert news_agent.output_key == "headlines"
    assert news_agent.tools, "The agent must have associated tools."

@pytest.mark.asyncio
async def test_twitter_agent_properties():
    assert twitter_agent.name == "TwitterAgent"
    assert twitter_agent.output_key == "twitter_mentions"
    assert twitter_agent.tools, "The agent must have associated tools."

@pytest.mark.asyncio
async def test_tavily_agent_properties():
    assert tavily_agent.name == "TavilyAgent"
    assert tavily_agent.output_key == "general_news"
    assert tavily_agent.tools, "The agent must have associated tools."

@pytest.mark.asyncio
async def test_fetch_data_agent_sub_agents():
    sub_agent_names = [agent.name for agent in fetch_data_agent.sub_agents]
    expected_names = {"NewsAgent", "TwitterAgent", "TavilyAgent"}
    assert set(sub_agent_names) == expected_names

@pytest.mark.asyncio
async def test_format_search_agent_properties():
    assert format_search_agent.name == "FormatAgent"
    assert format_search_agent.output_key == "search"
    assert format_search_agent.output_schema is not None

@pytest.mark.asyncio
async def test_search_agent_sub_agents():
    sub_agent_names = [agent.name for agent in search_agent.sub_agents]
    expected_names = {"SearchAgent", "FormatAgent"}
    assert set(sub_agent_names) == expected_names

@pytest.mark.asyncio
async def test_analyze_agent_properties():
    assert analyze_agent.name == "NewsAnalysisAgent"
    assert analyze_agent.output_key == "analysis"
    assert analyze_agent.output_schema is not None

@pytest.mark.asyncio
async def test_report_agent_properties():
    assert report_agent.name == "ReportAgent"
    assert report_agent.model == "gemini-2.0-flash"
    assert "Markdown" in report_agent.instruction