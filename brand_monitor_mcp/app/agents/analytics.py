from google.adk.agents import LlmAgent
from ..schemas import AnalyzeOutput

GEMINI_FLASH = "gemini-2.0-flash"

analyze_agent: LlmAgent = LlmAgent(
    name="NewsAnalysisAgent",
    model=GEMINI_FLASH,
    description="Analyze people's mentions and news about a brand, considering sentiments, main topics, and problems.",
    instruction=(
        "You are a brand analysis agent responsible for analyzing mentions about the company."
        "Analyze the following topics about what people are saying about the brand:"
        "- Sentiment: Identify the predominant sentiment: positive, negative, or neutral."
        "- Topics: Identify the top 3 topics talked about by people."
        "- Problems: Detect between 2 to 3 main problems mentioned by people."
        "Response format: {'sentiment': 'positive', 'topics': ['customer service', 'delivery'], 'problems': ['delivery delays', 'customer support']}"
        "Limitations:"
        "- Response: Only generate a JSON response."
        "- Brand: Only analyze news of the company mentioned in the previous response."
        "Considerations:"
        "- Ensure the response is a JSON with keys: 'sentiment', 'topics', 'problems'."
        "- The 'problems' key must be a list of strings."
    ),
    output_schema=AnalyzeOutput,
    output_key="analysis"
)
