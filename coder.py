"""
agents/coder.py — Python Coder Agent
Writes and executes Python code to solve computational tasks.
"""

from langchain_openai       import ChatOpenAI
from langchain.agents       import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from tools                  import python_repl_tool
from config                 import MODEL_NAME, TEMPERATURE, OPENAI_API_KEY, VERBOSE

CODER_PROMPT = PromptTemplate.from_template("""
You are an expert Python Coder Agent. Your job is to solve problems by
writing clean, well-commented Python code and executing it.

Guidelines:
- Write simple, readable code — avoid unnecessary complexity.
- Always print() the final result so it appears in the output.
- Handle potential errors with try/except where sensible.
- Explain what the code does in 1-2 sentences before the Final Answer.

You have access to the following tools:
{tools}

Tool names: {tool_names}

Use this format STRICTLY:

Question: the input question you must answer
Thought: your reasoning step
Action: the tool to use — must be one of [{tool_names}]
Action Input: Python code to execute
Observation: the result of running the code
... (repeat if needed)
Thought: I now have the answer
Final Answer: explanation + the code output

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

def build_coder_agent() -> AgentExecutor:
    llm   = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE, api_key=OPENAI_API_KEY)
    tools = [python_repl_tool]
    agent = create_react_agent(llm, tools, CODER_PROMPT)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=VERBOSE,
        handle_parsing_errors=True,
        max_iterations=6,
    )
