"""
tools/search_tool.py — Free web search via DuckDuckGo (no API key needed)
"""

from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools           import Tool

_ddg = DuckDuckGoSearchRun()

web_search_tool = Tool(
    name="web_search",
    func=_ddg.run,
    description=(
        "Search the web for current information. "
        "Use when the user asks about recent events, facts, or anything "
        "that requires up-to-date knowledge. Input should be a search query string."
    ),
)
