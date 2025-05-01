import requests
import xml.etree.ElementTree as ET
import os
from tavily import TavilyClient
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def fetch_news(query: str) -> str:
    """Fetch top 5 news headlines matching the query from Google News RSS.

    Constructs a Google News RSS feed URL based on the query, fetches the
    feed, parses the XML, and extracts the titles and links of the top 5
    news items.

    Args:
        query: The search term to use for finding news headlines (str).

    Returns:
        A string containing up to 5 news headlines, each formatted as
        "- Title — Link" and separated by newlines. Returns an empty
        string if no items are found or if the RSS feed structure is
        unexpected.

    Raises:
        requests.exceptions.HTTPError: If the request to the Google News RSS
            feed fails (e.g., network issue, server error).
        xml.etree.ElementTree.ParseError: If the content received from the
            RSS feed is not valid XML.
    """
    # URL encode the query to handle special characters safely
    encoded_query = requests.utils.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
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

def fetch_twitter(query: str) -> str:
    """
    Busca tweets recentes relacionados ao termo de busca.
    Em caso de erro, retorna uma mensagem padrão sem interromper a execução dos outros agentes.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    headers = {"Authorization": f"Bearer {bearer}"}
    querystring = {"max_results": "10", "query": query}

    try:
        resp = requests.get(url, headers=headers, params=querystring)
        resp.raise_for_status()  # Captura erros HTTP (400, 500)
        return resp.text
    except Exception as e:
        print(f"⚠️ Erro ao buscar no Twitter para '{query}': {e}")
        return "Não foi possível buscar tweets no momento."    
        
def fetch_tavily(query: str) -> str:
    """
    Colete 10 notícias principais sobre o interesse de busca na internet.
    
    Argumentos: 
    - 'query': O termo de busca para encontrar notícias (str)
    
    Retorna:
        Um texto contendo 10 notícias principais sobre o termo de busca.
        Esse texto contém os tópicos: title, url e text.
    """
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query=query, max_results=5, topic="general")
    results = response.get("results")
    results_formated = []
    for item in results:
        title = item.get("title")
        url = item.get("url")
        content = item.get("content")
        results_formated.append(f"Title: {title} - URL: {url} - Text: {content}") 
    # string com title, url, content.
    return "\n".join(results_formated)
    
def fetch_reddit(query: str) -> str:
    """
    """        
    url = f""
    resp = requests.get(url)
    resp.raise_for_status()
    # Retorna posts/comentários mencionando a marca