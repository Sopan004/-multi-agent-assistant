"""
graph/workflow.py — LangGraph Supervisor Workflow

State machine:
  START → supervisor → [researcher | coder | writer] → supervisor → ... → END

The supervisor decides which agent handles the task at each step,
then routes to END when the answer is complete.
"""

from typing import TypedDict, Annotated, Literal
import operator

from langchain_openai       import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph        import StateGraph, END
from langgraph.prebuilt     import ToolNode

from agents  import build_researcher_agent, build_coder_agent, build_writer_agent
from config  import MODEL_NAME, TEMPERATURE, OPENAI_API_KEY, VERBOSE

# ── Shared State ──────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    task:          str                              # original user task
    messages:      Annotated[list[str], operator.add]  # conversation log
    next_agent:    str                              # routing decision
    final_answer:  str                              # assembled answer

# ── Supervisor ────────────────────────────────────────────────────────────────

SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a Supervisor orchestrating a team of three agents:
  • researcher  — searches the web for facts and current information
  • coder       — writes and runs Python code for calculations/data tasks
  • writer      — polishes and formats the final answer

Given the current task and what has been done so far, decide which agent
should act NEXT, or reply FINISH if the task is complete.

Respond with ONLY one word: researcher | coder | writer | FINISH
"""),
    ("human", "Task: {task}\n\nProgress so far:\n{progress}\n\nNext agent?"),
])

def build_supervisor():
    llm    = ChatOpenAI(model=MODEL_NAME, temperature=0, api_key=OPENAI_API_KEY)
    chain  = SUPERVISOR_PROMPT | llm
    return chain

# ── Node Functions ────────────────────────────────────────────────────────────

def supervisor_node(state: AgentState) -> AgentState:
    supervisor = build_supervisor()
    progress   = "\n".join(state["messages"]) if state["messages"] else "Nothing done yet."
    decision   = supervisor.invoke({"task": state["task"], "progress": progress})
    next_agent = decision.content.strip().lower()

    if VERBOSE:
        print(f"\n🧠 Supervisor → {next_agent.upper()}")

    return {**state, "next_agent": next_agent}


def researcher_node(state: AgentState) -> AgentState:
    agent  = build_researcher_agent()
    result = agent.invoke({"input": state["task"]})
    output = result.get("output", "")
    if VERBOSE:
        print(f"\n🔍 Researcher:\n{output}\n")
    return {
        **state,
        "messages": [f"[Researcher]\n{output}"],
    }


def coder_node(state: AgentState) -> AgentState:
    agent  = build_coder_agent()
    result = agent.invoke({"input": state["task"]})
    output = result.get("output", "")
    if VERBOSE:
        print(f"\n💻 Coder:\n{output}\n")
    return {
        **state,
        "messages": [f"[Coder]\n{output}"],
    }


def writer_node(state: AgentState) -> AgentState:
    writer = build_writer_agent()
    context = "\n\n".join(state["messages"])
    prompt  = f"Task: {state['task']}\n\nRaw inputs:\n{context}\n\nWrite the final polished answer."
    output  = writer.invoke({"input": prompt})
    if VERBOSE:
        print(f"\n✍️  Writer:\n{output}\n")
    return {
        **state,
        "messages":     [f"[Writer]\n{output}"],
        "final_answer": output,
    }

# ── Routing ───────────────────────────────────────────────────────────────────

def route(state: AgentState) -> Literal["researcher", "coder", "writer", "__end__"]:
    decision = state.get("next_agent", "writer")
    if decision == "finish":
        return "__end__"
    if decision in ("researcher", "coder", "writer"):
        return decision
    return "__end__"   # safety fallback

# ── Graph Assembly ────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("supervisor",  supervisor_node)
    graph.add_node("researcher",  researcher_node)
    graph.add_node("coder",       coder_node)
    graph.add_node("writer",      writer_node)

    # Entry point
    graph.set_entry_point("supervisor")

    # Supervisor routes to agents or END
    graph.add_conditional_edges("supervisor", route)

    # After each agent, return to supervisor
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("coder",      "supervisor")
    graph.add_edge("writer",     "supervisor")

    return graph.compile()
