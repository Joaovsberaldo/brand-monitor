# 🚀 Brand Monitoring Agent

This project is an end-to-end AI agent that monitors and analyzes brand mentions across the web. It performs three core tasks:

1. **Ingests** brand mentions from sources like Twitter, News APIs, and the general web.
2. **Analyzes** public sentiment, key topics, and issues.
3. **Generates** a clear Markdown report with insights and recommendations.

---

## 🧰 Tools Used

- **Agent Development Kit (ADK)** – define agents, tools, and function calls.
- **MCP (optional)** – use provided credentials or implement custom connectors.
- **Gemini** – LLM for analyzing mentions and generating reports.
- **Python dependencies** – install via:

```bash
pip install -r requirements.txt
```

---

## 📥 Inputs

- `company_name` (string)
  e.g. `"Acme Co."`

---

## 📈 Output

Your agent should return a or Markdown report containing:

1. **Executive Summary**
   A 2–3 sentence overview of overall sentiment and top concerns.

2. **Sentiment Breakdown**
   Percentage of positive / neutral / negative mentions, **by source**.

3. **Top 5 Topics & Issues**
   Most frequently discussed themes (e.g., “shipping delays,” “customer support”).

4. **Trend Analysis**
   Simple time-series summary (mentions per day), highlighting peaks.

5. **Sample Mentions**
   2–3 representative quotes (with source name and link) for each sentiment category.

6. **Recommendations**
   Based on detected issues, suggest 2–3 actionable next steps.

---

## ⚙️ Setup

### 1. Environment Variables

**Create a .env file and add:**
```
GOOGLE_API_KEY=your_gemini_api_key
```

- **Gemini API key**
  Access google: http://aistudio.google.com/

  Login with your google account.

  Create an api key.

  Create a file named `.env`.

  Add the variable GOOGLE_API_KEY with the value of the api key from ai studio

### 2. ADK UI

Open UI using terminal:

```
adk web
```

### 3. Run Local MCP (optional)

to run the local MCP, make sure you have the correct credentials in your .env file

```
cd brand_monitor_mcp/app/
uvicorn services.api:app --host 0.0.0.0 --port 8001 --reload
```

### Credentials

#### 🐦 Twitter Credentials
**Website:** [developer.twitter.com/en/portal/dashboard](https://developer.twitter.com/en/portal/dashboard)
**What you’ll need:**
- **Bearer Token**

---

#### 🗞️ News API (Tavily)
**Website:** [tavily.com](https://tavily.com/)
**What you’ll need:**
- **API Key**
