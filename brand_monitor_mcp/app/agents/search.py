from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from ..schemas import SearchOutput
from ..tools.mcp_tools import search_twitter, search_tavily, search_google

GEMINI_FLASH = "gemini-2.0-flash"

news_agent: LlmAgent = LlmAgent(
    name="NewsAgent",
    model=GEMINI_FLASH,
    description="Search for news about a brand.",
    instruction=(
        "You are a news collecting agent responsible for gathering news and mentions about brands/companies."
        "You prioritize facts and customer mentions and news about the general market perception."
        "Collect the main mentions and news and save them in state['headlines']."
        "Prioritize collecting data less than 3 months old."
        "As input, you will receive the brand/company name."
        "Use the 'fetch_news' tool to perform your task."
    ),
    output_key="headlines",
    tools=[search_tavily]
)

twitter_agent: LlmAgent = LlmAgent(
    name="TwitterAgent",
    model=GEMINI_FLASH,
    description="Search for posts mentioning a brand.",
    instruction=(
        "You are a marketing agent responsible for collecting relevant mentions about a brand/company."
        "You prioritize posts and comments about complaints and problems reported by users."
        "Collect 5 user mentions about the brand and save them in state['twitter_mentions']."
        "As input, you will receive the brand/company name."
        "Use the 'fetch_twitter' tool to perform your task."
    ),
    output_key="twitter_mentions",
    tools=[search_twitter],
)

tavily_agent: LlmAgent = LlmAgent(
    name="TavilyAgent",
    model=GEMINI_FLASH,
    description="Search for general news about a brand.",
    instruction=(
        "You are a news collecting agent responsible for gathering news and mentions about brands/companies."
        "You prioritize facts and customer mentions and news about the general market perception."
        "Collect the main mentions and news and save them in state['headlines']."
        "Prioritize collecting data less than 3 months old."
        "As input, you will receive the brand/company name."
        "Use the 'fetch_tavily' tool to perform your task."
    ),
    output_key="general_news",
    tools=[search_google]
)


fetch_data_agent: ParallelAgent = ParallelAgent(
    name="SearchAgent",
    description="Search for mentions about a brand in google news, twitter, and tavily.",
    sub_agents=[news_agent, twitter_agent, tavily_agent]
)

format_search_agent: LlmAgent = LlmAgent(
    name="FormatAgent",
    model=GEMINI_FLASH,
    description="Format the news and mentions according to the specified JSON.",
    instruction=(
        "You are a text editor responsible for formatting news and twitter posts."
        "You prioritize readable and clear formatting."
        "Format the news and twitter posts according to the SearchOutput class."
        ),
    output_schema=SearchOutput,
    output_key="search",
)

# -------- Search -------- #
search_agent: SequentialAgent = SequentialAgent(
    name="SearchFormatAgent",
    description="Execute a sequence of news search and search formatting.",
    sub_agents=[fetch_data_agent, format_search_agent]
)