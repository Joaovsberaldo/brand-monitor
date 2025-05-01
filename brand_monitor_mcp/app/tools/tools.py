import requests
import xml.etree.ElementTree as ET
import os
from tavily import TavilyClient
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def search_twitter(company_name: str) -> str:
    """
    Search for recent tweets related to the search term.
    In case of error, returns a default message without interrupting the execution of other agents.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    headers = {"Authorization": f"Bearer {bearer}"}
    querystring = {"max_results": "10", "query": company_name}

    try:
        resp = requests.get(url, headers=headers, params=querystring)
        resp.raise_for_status()  # Capture HTTP errors (400, 500)
        return resp.text
    except Exception as e:
        print(f"⚠️ Error searching Twitter for '{company_name}': {e}")
        return "Unable to fetch tweets at the moment."  
    

def search_google(company_name: str) -> str:
    """
    Searches the top 5 news headlines corresponding to the company_name on Google News RSS.

    Constructs a Google News RSS feed URL based on the company_name, fetches
    the feed, parses the XML, and extracts titles and links of the top 5
    news items.

    Args:
        company_name: The search term used to find news headlines (str).

    Returns:
        A string containing up to 5 headlines, each formatted as
        "- Title — Link" and separated by line breaks. Returns an empty string
        if no items are found or if the RSS feed structure is unexpected.

    Raises:
        requests.exceptions.HTTPError: If the request to the Google News RSS feed
            fails (e.g., network issue, server error).
        xml.etree.ElementTree.ParseError: If the received feed content
            is not valid XML.
    """
    # URL encode the company_name to handle special characters safely
    encoded_company_name = requests.utils.quote(company_name)
    url = f"https://news.google.com/rss/search?q={encoded_company_name}&hl=en-US&gl=US&ceid=US:en"
    resp = requests.get(url)
    resp.raise_for_status() # Raises HTTPError for bad responses
    # Raises ParseError if resp.content is not valid XML
    root = ET.fromstring(resp.content)
    # Find item elements within the channel
    items = root.findall(".//item")[:10] # Limit to top 5
    result = []
    for item in items:
        # Use .findtext() with default to handle potentially missing elements gracefully
        title = item.findtext("title", default="[No Title]")
        link  = item.findtext("link", default="#")
        result.append(f"- {title} — {link}")
    return "\n".join(result)


def search_tavily(company_name: str) -> str:
    """
    Collects top 10 news about the internet search interest.

    Arguments: 
    - 'company_name': The search term to find news (str)

    Returns:
        A text containing top 10 news about the search term.
        This text contains the topics: title, url and text.
    """
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query=company_name, max_results=5, topic="general")
    results = response.get("results")
    results_formatted = []
    for item in results:
        title = item.get("title")
        url = item.get("url")
        content = item.get("content")
        results_formatted.append(f"Title: {title} - URL: {url} - Text: {content}") 
    # string with title, url, content.
    return "\n".join(results_formatted)   
