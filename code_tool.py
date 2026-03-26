"""
tools/code_tool.py — Safe Python REPL for executing generated code
"""

from langchain_experimental.tools import PythonREPLTool
from langchain.tools               import Tool

_repl = PythonREPLTool()

python_repl_tool = Tool(
    name="python_repl",
    func=_repl.run,
    description=(
        "Execute Python code and return the output. "
        "Use for: data analysis, math calculations, generating charts, "
        "sorting/filtering data, string manipulation, or any task "
        "that benefits from running actual code. "
        "Input must be valid Python code as a string."
    ),
)
