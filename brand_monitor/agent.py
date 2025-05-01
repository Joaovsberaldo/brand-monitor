from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from .tools import (fetch_news, fetch_twitter, fetch_tavily)
from pydantic import BaseModel, Field
from typing import List

GEMINI_FLASH = "gemini-2.0-flash"



news_agent: LlmAgent = LlmAgent(
    name="AgenteNoticias",
    model=GEMINI_FLASH,
    description="Busque notícias sobre uma marca.",
    instruction=(
        "Você é um agente coletor de notícias responsável por coletar notícias e menções sobre marcas/empresas."
        "Você prioriza fatos e menções de clientes e notícias sobre a percepção geral do mercado."
        "Colete as principais menções e notícias e as salve em state['headlines']."
        "Priorize coletar dados com menos de 3 meses."
        "Como entrada você receberá o nome da marca/empresa."
        "Use a ferramenta 'fetch_news' para executar sua tarefa."
    ),
    output_key="headlines",
    tools=[fetch_news]
)

twitter_agent: LlmAgent = LlmAgent(
    name="AgenteTwitter",
    model=GEMINI_FLASH,
    description="Busque postagens que mencionem uma marca.",
    instruction=(
        "Você é um agente marketing responsável por coletar menções relevantes sobre uma marca/empresa."
        "Você prioriza posts e comentários sobre reclamações e problemas relatados pelos usuários."
        "Colete 5 menções de usuários sobre a marca e as salve em state['twitter_mentions']."
        "Como entrada, você receberá o nome da marca/empresa."
        "Use a ferramenta 'fetch_twitter' para executar sua tarefa."
    ),
    output_key="twitter_mentions",
    tools=[fetch_twitter],
)

tavily_agent: LlmAgent = LlmAgent(
    name="AgenteTavily",
    model=GEMINI_FLASH,
    description="Busque notícias gerais sobre uma marca.",
    instruction=(
        "Você é um agente coletor de notícias responsável por coletar notícias e menções sobre marcas/empresas."
        "Você prioriza fatos e menções de clientes e notícias sobre a percepção geral do mercado."
        "Colete as principais menções e notícias e as salve em state['headlines']."
        "Priorize coletar dados com menos de 3 meses."
        "Como entrada você receberá o nome da marca/empresa."
        "Use a ferramenta 'fetch_tavily' para executar sua tarefa."
    ),
    output_key="general_news",
    tools=[fetch_tavily]
)

# Orquestrador de busca
fetch_agent: ParallelAgent = ParallelAgent(
    name="AgenteBuscador",
    description="Busca menções sobre uma marca no google news, twitter e tavily.",
    sub_agents=[news_agent, twitter_agent, tavily_agent]
)

class SearchOutput(BaseModel):
    text: str = Field(description="O texto da notícia/post sobre a marca.")
    source: str = Field(description="A fonte ou URL do texto.")
    company_query: str = Field(description="A marca/empresa que foi pesquisada.")

format_agent: LlmAgent = LlmAgent(
    name="AgenteFormatadorDados",
    model=GEMINI_FLASH,
    description="Formate as notícias e menções de acordo com JSON especificado.",
    instruction=(
        "Você é um editor de texto responsável por formatar notícias e posts do twitter."
        "Você prioriza uma formatação legível e clara de entender."
        "Formate as notícias e os posts do twitter de acordo com a classe SearchOutput."
        ),
    output_schema=SearchOutput,
    output_key="search",
)

search_agent: SequentialAgent = SequentialAgent(
    name="AgenteFormatadorBusca",
    description="Executa uma sequência de busca de notícias e formatação da busca.",
    sub_agents=[fetch_agent, format_agent]
)

# Analisa notícias
class AnalyzeOutput(BaseModel):
    sentimento: str = Field(description="O sentimento predominante das pessoas nas menções e notícias sobre a empresa.")
    topicos: List[str] = Field(description="Os principais tópicos mencionados pelas pessoas sobre a empresa.")
    problemas: List[str] = Field(description="Os problemas mais mencionados pelas pessoas sobre a empresa.")

analyze_agent: LlmAgent = LlmAgent(
    name="AgenteAnalistaNoticias",
    model=GEMINI_FLASH,
    description="Analise menções das pessoas e notícias sobre uma marca, considerando os sentimentos, tópicos principais e problemas.",
    instruction=(
        "Você é um agente analista de marca responsável por analisar menções sobre a empresa."
        "Analise os seguintes tópicos sobre o que pessoas estão dizendo sobre a marca:"
        "- Sentimento: Identifique qual sentimento é predominante: positivo, negativo ou neutro."
        "- Tópicos: Identifique os 3 principais tópicos falados pelas pessoas."
        "- Problemas: Detecte entre 2 a 3 principais problemas mencionados pelas pessoas."
        "Formato resposta: {'sentimento': 'positivo', 'topicos': ['atendimento ao cliente', 'entrega'], 'problemas': ['atrasos na entrega', 'suporte ao cliente']}"
        "Limitações:"
        "- Resposta: Apenas gere uma resposta em JSON."
        "- Marca: Apenas analise notícias da empresa mencionada na resposta anterior."
        "Considerações:"
        "- Garanta que a resposta seja um JSON com as chaves: 'sentimento', 'topicos', 'problemas'."
        "- A chave 'problemas' deve ser uma lista de strings."
    ),
    output_schema=AnalyzeOutput,
    output_key="analysis"
)

# Gera o relatório
report_agent: LlmAgent = LlmAgent(
    name="AgenteRelatorio",
    model=GEMINI_FLASH,
    description="Gere um relatório em formato markdown sobre a percepção de uma marca.",
    instruction=(
        "Você é um analista de experiência do cliente responsável por gerar relatórios sobre uma marca."
        "Escreva um relátorio sobre as menções da empresa em notícias e em redes sociais, considerando a análise enviada."
        "Estruture seu relatório da seguinte maneira:"
        "1. Resumo Executivo: Uma visão geral em 2–3 frases sobre o sentimento geral e as principais preocupações."
        "2. Distribuição de Sentimentos: Percentual de menções positivas / neutras / negativas, por fonte."
        "3. Top 5 Tópicos & Problemas: Temas mais discutidos com frequência (ex.: “atrasos na entrega”, “suporte ao cliente”)."
        "4. Análise de Tendência: Resumo simples em série temporal (menções por dia), destacando os picos."
        "5. Menções Exemplares: 2–3 citações representativas (com nome da fonte e link) para cada categoria de sentimento."
        "6. Recomendações: Com base nos problemas detectados, sugira 2–3 próximos passos acionáveis."
        "Formato da resposta: Markdown"
        "Considerações:"
        "– Use símbolos de arquivos markdown: Hierarquia de títulos (ex: #, ##, etc.), listas (-, números,), destaques (negrito)"
    ),
)
# Executa o monitoramento da marca
brand_monitor_agent: SequentialAgent = SequentialAgent(
    name="AgenteOrquestrador",
    description="Executa uma sequência de, busca de notícias e menções, análise de texto, geração de relatório.",
    sub_agents=[search_agent, analyze_agent, report_agent]
)

root_agent = brand_monitor_agent