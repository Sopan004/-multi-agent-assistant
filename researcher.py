"""
agents/researcher.py — Web Research Agent
Searches the internet, retrieves facts, and summarises findings.
"""

from langchain_openai              import ChatOpenAI
from langchain.agents              import create_react_agent, AgentExecutor
from langchain_core.prompts        import PromptTemplate
from tools                         import web_search_tool
from config                        import MODEL_NAME, TEMPERATURE, OPENAI_API_KEY, VERBOSE

RESEARCHER_PROMPT = PromptTemplate.from_template("""
You are an expert Research Agent. Your job is to search the web and return
accurate, well-organised findings on any topic.

Guidelines:
- Always verify facts with at least one web search.
- Summarise clearly with bullet points where appropriate.
- Cite the topic you searched for at the end.
- Never fabricate information.

You have access to the following tools:
{tools}

Tool names: {tool_names}

Use this format STRICTLY:

Question: the input question you must answer
Thought: your reasoning step
Action: the tool to use — must be one of [{tool_names}]
Action Input: what to pass to the tool
Observation: the result of the tool
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: your complete, well-structured answer

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

def build_researcher_agent() -> AgentExecutor:
    llm   = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE, api_key=OPENAI_API_KEY)
    tools = [web_search_tool]
    agent = create_react_agent(llm, tools, RESEARCHER_PROMPT)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=VERBOSE,
        handle_parsing_errors=True,
        max_iterations=6,
    )
