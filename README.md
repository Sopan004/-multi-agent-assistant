# 🤖 Multi-Agent Task Assistant

A production-grade **LangGraph multi-agent system** where a Supervisor orchestrates three specialised agents — Researcher, Coder, and Writer — to solve any general-purpose task autonomously.

Built to demonstrate core **AI Engineering** skills for 2026: agent orchestration, tool use, LangGraph state machines, and modular agent design.

---

## 🏗️ Architecture

```
User Task
    │
    ▼
┌─────────────┐
│  Supervisor │  ← decides which agent acts next
└──────┬──────┘
       │
   ┌───┴────────────────┐
   │                    │
   ▼                    ▼                    ▼
┌──────────┐    ┌───────────┐    ┌───────────────┐
│Researcher│    │  Coder    │    │    Writer     │
│🔍 Search │    │💻 Python  │    │✍️  Synthesise │
│  Web     │    │   REPL    │    │   & Format    │
└──────────┘    └───────────┘    └───────────────┘
       │                │                │
       └────────────────┴────────────────┘
                        │
                        ▼
                 Final Answer ✅
```

### Agents

| Agent | Tools | Responsibility |
|-------|-------|----------------|
| **Supervisor** | None (LLM routing) | Decides which agent acts next; routes to END when done |
| **Researcher** | `web_search` (DuckDuckGo) | Searches the internet for facts and current information |
| **Coder** | `python_repl` | Writes and executes Python code for calculations/data tasks |
| **Writer** | None (LLM chain) | Polishes raw outputs into clean, structured final answers |

### Tech Stack

- **LangGraph** — state machine orchestration
- **LangChain** — agent/tool abstractions
- **OpenAI GPT-4o-mini** — LLM backbone (cheap & fast)
- **DuckDuckGo Search** — free web search (no API key needed)
- **Python REPL** — sandboxed code execution

---

## 📁 Project Structure

```
multi-agent-assistant/
├── agents/
│   ├── __init__.py
│   ├── researcher.py    # ReAct agent with web search
│   ├── coder.py         # ReAct agent with Python REPL
│   └── writer.py        # LCEL chain for formatting
├── tools/
│   ├── __init__.py
│   ├── search_tool.py   # DuckDuckGo wrapper
│   └── code_tool.py     # Python REPL wrapper
├── graph/
│   ├── __init__.py
│   └── workflow.py      # LangGraph state machine
├── main.py              # CLI entry point
├── config.py            # Centralised config via .env
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚡ Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-assistant.git
cd multi-agent-assistant
```

### 2. Create virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> Get your key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 5. Run

```bash
python main.py
```

---

## 💬 Example Tasks

```
📝 Your Task: What are the top AI engineering skills to learn in 2026?

📝 Your Task: Calculate compound interest on $5000 at 8% over 15 years

📝 Your Task: Find the latest news about Anthropic and write a short brief

📝 Your Task: What is the difference between RAG and fine-tuning? Write a comparison.

📝 Your Task: Write and run a Python function to generate the first 20 Fibonacci numbers
```

---

## 🔧 Configuration

Edit `.env` to customise behaviour:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | **Required.** Your OpenAI key |
| `MODEL_NAME` | `gpt-4o-mini` | Swap to `gpt-4o` for better reasoning |
| `TEMPERATURE` | `0` | `0` = deterministic, `0.7` = creative |
| `MAX_ITERATIONS` | `10` | Max agent loop steps before stopping |
| `VERBOSE` | `true` | Show step-by-step agent thinking |

---

## 🧩 Extending the Project

### Add a new agent

1. Create `agents/your_agent.py` following the same pattern as `researcher.py`
2. Export it in `agents/__init__.py`
3. Add a node in `graph/workflow.py` and wire it into the routing logic

### Swap the LLM

Change `MODEL_NAME` in `.env`. Compatible options:
- `gpt-4o-mini` (default, cheapest)
- `gpt-4o` (best reasoning)
- Use `langchain-groq` + Groq API for near-free inference with Llama 3

### Add memory

Import `langgraph.checkpoint.memory.MemorySaver` and pass it to `graph.compile(checkpointer=...)` for persistent conversation history.

---

## 📊 Key Concepts Demonstrated

- **LangGraph StateGraph** — typed state, conditional edges, cyclical graphs
- **ReAct Agent Pattern** — Reason + Act loop with tool use
- **LCEL Chains** — composable LangChain Expression Language
- **Supervisor Pattern** — central router coordinating specialised sub-agents
- **Tool Abstraction** — clean separation of tools from agent logic
- **Environment Config** — dotenv-based config management

---

## 📄 License

MIT — free to use, modify, and share.

---

## 🙋 Author

Built by [Your Name](https://github.com/YOUR_USERNAME) as an AI Engineering portfolio project.
