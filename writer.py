"""
agents/writer.py — Writer / Summariser Agent
Synthesises inputs into clean, structured written output.
"""

from langchain_openai       import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config                 import MODEL_NAME, TEMPERATURE, OPENAI_API_KEY

WRITER_SYSTEM = """
You are an expert Writer Agent. Your job is to take raw research,
code outputs, or notes and transform them into polished, clear,
well-structured written content.

Guidelines:
- Use headings, bullet points, and code blocks where appropriate.
- Be concise — remove filler and redundancy.
- Adapt tone to the context (technical, casual, formal).
- Always end with a 1-sentence "Summary" line.
"""

def build_writer_agent():
    """Returns a simple LCEL chain (no tools needed for writing)."""
    llm    = ChatOpenAI(model=MODEL_NAME, temperature=0.3, api_key=OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_messages([
        ("system", WRITER_SYSTEM),
        ("human", "{input}"),
    ])
    return prompt | llm | StrOutputParser()
