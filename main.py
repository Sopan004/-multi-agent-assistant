"""
main.py — Entry point for Multi-Agent Assistant

Run:
    python main.py

Then type any task at the prompt. Examples:
    > What are the top AI engineering skills to learn in 2026?
    > Calculate the compound interest on $10,000 at 7% over 10 years
    > Summarise the key differences between LangChain and LlamaIndex
    > Find the latest news about OpenAI and write a short brief
"""

import sys
from graph import build_graph, AgentState

BANNER = """
╔══════════════════════════════════════════════════════════╗
║          🤖  Multi-Agent Task Assistant  v1.0            ║
║  Agents: Researcher 🔍 | Coder 💻 | Writer ✍️            ║
║  Type your task below. Type 'exit' to quit.              ║
╚══════════════════════════════════════════════════════════╝
"""

def run_task(task: str) -> str:
    """Run a single task through the multi-agent graph and return the final answer."""
    graph = build_graph()

    initial_state: AgentState = {
        "task":         task,
        "messages":     [],
        "next_agent":   "",
        "final_answer": "",
    }

    final_state = graph.invoke(initial_state)
    return final_state.get("final_answer", "No answer generated.")


def main():
    print(BANNER)

    while True:
        try:
            task = input("\n📝 Your Task: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! 👋")
            sys.exit(0)

        if not task:
            continue
        if task.lower() in ("exit", "quit", "q"):
            print("Goodbye! 👋")
            break

        print("\n⏳ Processing...\n" + "─" * 60)
        answer = run_task(task)
        print("\n" + "═" * 60)
        print("✅ FINAL ANSWER\n")
        print(answer)
        print("═" * 60)


if __name__ == "__main__":
    main()
