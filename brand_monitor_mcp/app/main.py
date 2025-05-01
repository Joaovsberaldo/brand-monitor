from google.adk.agents import SequentialAgent
from .agents.search import search_agent
from .agents.analytics import analyze_agent
from .agents.report import report_agent

# -------- Monitora a marca -------- #
brand_monitor_agent: SequentialAgent = SequentialAgent(
    name="OrchestratorAgent",
    description="Executes a sequence of: news and mentions search, text analysis, report generation.",
    sub_agents=[search_agent, analyze_agent, report_agent]
)

root_agent = brand_monitor_agent