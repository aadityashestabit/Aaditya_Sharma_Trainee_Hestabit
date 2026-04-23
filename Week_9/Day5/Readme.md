# Week 9 — Agentic AI

---

## Overview

Week 9 covers the design and implementation of multi-agent AI systems from scratch. Starting with a simple three-agent pipeline on Day 1 and ending with a full eleven-agent capstone system on Day 5, each day builds on the previous one by introducing a new architectural concept. By the end of the week the project is a complete autonomous AI system with parallel execution, tool calling, persistent memory, and a Streamlit dashboard.

The entire project runs on free-tier infrastructure. The LLM calls go to Groq's free API. There are no paid services, no cloud deployments, and no GPU required. Everything executes locally on a Linux machine.

---

## Tech Stack

The project uses AutoGen's agentchat library as the agent framework. All LLM calls go through Groq's free API using two models — llama-3.1-8b-instant for planning and orchestration, and meta-llama/llama-4-scout-17b-16e-instruct for tool-calling agents. The memory system uses SQLite for long-term fact storage and FAISS with sentence-transformers for semantic vector search. Data validation uses Pydantic's BaseModel. The Day 5 dashboard is built with Streamlit.


---

## Project Structure

```
Week_9/
├── .env                    
├── Dockerfile                
├── requirements.txt             
├── .dockerignore                 
│
├── Day1/
│   ├── agents/
│   │   ├── research_agent.py
│   │   ├── summarizer_agent.py
│   │   └── answer_agent.py
│   ├── loader.py
│   ├── run_pipeline.py
│   └── README.md
│
├── Day2/
│   ├── agents/
│   │   ├── worker_agent.py
│   │   ├── reflection_agent.py
│   │   └── validator_agent.py
│   ├── orchestrator/
│   │   └── planner.py
│   ├── loader.py
│   ├── run_day2.py
│   └── README.md
│
├── Day3/
│   ├── tools/
│   │   ├── file_agent.py
│   │   ├── db_agent.py
│   │   └── code_executor.py
│   ├── loader.py
│   ├── run_day3.py
│   └── README.md
│
├── Day4/
│   ├── memory/
│   │   ├── session_memory.py
│   │   └── vector_store.py
│   ├── loader.py
│   ├── run_day4.py
│   └── README.md
│
└── Day5/
    ├── nexus_ai/
    │   ├── agents/
    │   │   ├── agents.py
    │   │   ├── orchestrator.py
    │   │   ├── planner.py
    │   │   ├── researcher.py
    │   │   ├── coder.py
    │   │   ├── analyst.py
    │   │   ├── critic.py
    │   │   ├── optimizer.py
    │   │   ├── validator.py
    │   │   ├── reporter.py
    │   │   ├── file_agent.py
    │   │   └── db_agent.py
    │   └── config.py
    ├── memory/
    │   ├── session_memory.py      
    │   └── vector_store.py        
    ├── tools/
    │   ├── file_agent.py         
    │   ├── db_agent.py          
    │   └── code_executor.py     
    ├── main.py
    ├── app.py                   
    └── README.md
```

---

## Day 1 — Single Agent Pipeline

Day 1 introduces the simplest possible multi-agent pattern. Three agents run in a fixed sequence where each agent takes the previous agent's output as its input. There is no orchestration, no planning, and no parallelism. The goal is to understand how a single AssistantAgent works, how messages pass between agents, and how BufferedChatCompletionContext limits memory to a sliding window of ten turns.

The Research Agent receives the user query and produces a detailed factual response. The Summarizer Agent takes that response and compresses it into a concise summary. The Answer Agent takes both the original query and the summary and produces the final clean answer.

The key design decision is the Answer Agent receives two inputs — the original query and the summary — rather than just the summary alone. This prevents the answer from drifting away from what the user actually asked.

To run Day 1:

```bash
cd Day1
python run_pipeline.py
```

Type any question when prompted. Examples that work well are factual questions like "What is the difference between supervised and unsupervised learning?" or conceptual questions like "Explain how a transformer neural network works step by step."

---

## Day 2 — Multi-Agent Orchestration with DAG

Day 2 introduces dynamic planning and parallel execution using a Directed Acyclic Graph. Instead of a fixed three-agent chain, the Planner agent reads the user query and generates a structured execution plan where tasks can run in parallel when they have no dependencies on each other.

The Planner uses Pydantic's BaseModel to define and validate the plan schema. Every plan must be a list of Task objects where each task has a worker_name, a description, and a depends_on list. The depends_on list is what creates the DAG structure — tasks with empty depends_on lists run simultaneously, and tasks that list other tasks in depends_on wait for those tasks to complete before starting.

Execution uses asyncio.Semaphore to limit concurrency to three parallel workers at a time. This prevents burst rate limit errors on the free Groq tier. The asyncio.gather call launches all ready tasks simultaneously and the semaphore ensures at most three of them are actually running at any moment.

After all worker tasks complete, a Reflection agent reviews the final task's output for quality and completeness. A Validator agent then checks the reflected output against the original user query to ensure the answer actually addresses what was asked. If the validator says PASS the reflected output is shown. If the validator made improvements its improved version is shown instead.

The call_agent helper function wraps every agent call with retry logic — three attempts with exponential backoff of thirty, sixty, and ninety seconds for rate limit errors.

To run Day 2:

```bash
cd Day2
python run_day2.py
```

Try queries of varying complexity. Simple queries like "What is a neural network?" should produce a single-worker plan. Complex queries like "Plan a startup in AI for healthcare" or "Design a recommendation system for a video streaming platform" should produce four to six workers running in parallel batches.

Common issues and fixes: if the planner returns a truncated JSON response the query was too complex and generated too many tasks with long descriptions. The fix is to add "Maximum 4 tasks total. Keep each task description under 15 words." to the planner system prompt. If rate limit errors appear during execution the semaphore and backoff will handle them automatically.

---

## Day 3 — Tool-Calling Agent Pipeline

Day 3 introduces agents that can take real actions through registered tools. Three specialist agents replace the generic workers from Day 2. The FILE agent can read, write, append, and list files. The DB agent can inspect SQLite database schemas and execute SQL queries. The CODE agent can write and execute Python code in a real subprocess on the local machine.

The key architectural change from Day 2 is that tool-calling agents require a separate model client with function_calling set to True. The planner still uses a regular client. This is why Day 3 defines two separate client classes — LLMclient for the planner and ToolLLMclient for the three tool agents. Using the wrong client for tool agents is the most common setup error.

The pipeline is sequential rather than parallel because Day 3 tasks are inherently ordered — you cannot analyze a file before reading it, and you cannot save a report before generating it. Context injection connects the steps — every agent receives all previous outputs appended to its task so it has full context without any explicit passing of data.

The FILE agent has five tools: read_file reads any file and returns column statistics for CSVs, write_file writes text to any file, write_csv writes properly formatted CSV files using Python's csv.DictWriter for correct comma escaping, append_file adds content without overwriting, and list_files shows directory contents. The write_csv function accepts three input formats — list of dicts, list of lists with headers, and JSON strings — and normalizes them all before writing.

The DB agent has two tools: inspect_schema returns all table names, column definitions, row counts, and sample rows from a SQLite database, and execute_sql runs both single statements and multi-statement scripts. The execute_sql function detects when a query contains multiple statements by checking for semicolons and uses executescript for those cases rather than execute.

The CODE agent has one tool: run_python. This function writes the model's generated code to a temporary file in the /tmp directory, spawns a completely separate subprocess using the same Python interpreter, captures stdout and stderr, and returns both the code and its output. The Groq model never executes any code. It only decides what code to write. All actual execution happens locally on the developer's machine through the subprocess. An auto-install mechanism scans the code for import statements and installs any missing packages via pip before running.

To run Day 3:

```bash
cd Day3
python run_day3.py
```

Test each agent type separately before combining them. For the FILE agent try "List all files in the current directory" and "Create a file called test.txt with content hello world." For the DB agent try "Create a table called employees with name and salary columns and insert 3 rows." For the CODE agent try "Write Python code to find all prime numbers between 1 and 100." For multi-step chains try "Generate 500 rows of sales data and save to sales.csv."

The most common errors are the tool_use_failed error from Groq which means the model wrote a tool call in the wrong format. This is fixed by strengthening the system prompt with explicit instructions not to write markdown or explanations and to call the tool immediately. GUI applications like tkinter cannot run in the subprocess because they need a display and will hang — route those queries to save the code only rather than executing it.

---

## Day 4 — Memory Systems

Day 4 introduces persistent memory across conversation sessions. Three memory layers work together to give the agent context about past interactions.

Short-term memory uses a Python deque with maxlen of ten. It stores the last ten conversation turns in RAM and loses everything when the program exits. This is what makes the conversation feel coherent within a single session.

Long-term memory uses SQLite with two tables — facts and conversation_turns. The facts table stores extracted key information like the user's name, workplace, and interests. The conversation_turns table stores every message with its role and timestamp. Both tables persist to disk at memory/long_term.db and survive program restarts. Fact extraction uses regex patterns to find phrases like "my name is", "I work at", "I like", and "I am learning."

Vector memory uses FAISS with the all-MiniLM-L6-v2 sentence-transformers model. Every message is converted to a 384-dimensional vector and stored in a FAISS IndexFlatL2 index. When the user asks a new question, the question is also converted to a vector and FAISS finds the three most semantically similar past exchanges by comparing L2 distances. This means the agent can recall relevant past context even when there are no keyword matches. Both the FAISS index and the metadata list that maps vector positions back to original text are saved to disk after every addition and loaded on startup.

The main loop retrieves from all three stores before generating every response. Short-term context provides conversational flow. SQLite keyword search finds stored facts relevant to the current query. FAISS semantic search finds semantically similar past exchanges. All retrieved context is assembled into a memory block that is injected into the prompt before the current query.

To test memory persistence: run Day 4, tell it your name and what you are working on, exit the program, restart it, and ask "What is my name?" and "What am I working on?" — it should answer correctly from SQLite facts even though the short-term memory is gone.

To run Day 4:

```bash
cd Day4
python run_day4.py
```

---

## Day 5 — Nexus AI Capstone

Day 5 combines everything from the previous four days into a single production-quality system called Nexus AI. Eleven agents work together under the direction of an Orchestrator that reads every query and decides which agents to use and in what order.

The eleven agents are Orchestrator, Planner, Researcher, Coder, Analyst, Critic, Optimizer, Validator, Reporter, FILE, and DB. Three of these are tool-calling agents — Coder, FILE, and DB — and they use the tool client with function_calling True. All other agents use the regular model client.

The Orchestrator uses a routing rules system in its system prompt to decide which agents to activate for each query. Simple factual questions go only to Researcher. Code tasks go to Coder then Validator. File analysis tasks go to FILE then Analyst. Database tasks go to DB only. Tasks requiring quality assurance use Critic then Optimizer then Validator. Reports are only generated when the user explicitly asks for one.

The memory system from Day 4 is reused directly. Every query retrieves from SQLite facts and FAISS vectors before generating a response. Every response is stored back to both memory systems after completion.

There are two interfaces. The terminal interface at main.py shows the execution tree in the console and prints each step's output. The Streamlit dashboard at app.py provides a dark-themed web UI with real-time step tracking, agent badges, a memory context panel in the sidebar, and conversation history.

The Validator has a PASS detection mechanism. If the validator's output starts with phrases like "pass", "the output fully", "unchanged", or "correct and complete" then the previous step's output is shown rather than the verdict. This prevents the user from seeing validation reports instead of actual answers.

To run the terminal interface:

```bash
cd Day5
python nexus_ai/main.py
```

To run the Streamlit dashboard:

```bash
cd Day5
streamlit run app.py --server.fileWatcherType none
```

Then open http://localhost:8501 in a browser.

Test with queries of different types to verify correct routing. "What is a vector database?" should use only Researcher. "Write Python code to sort a list of dictionaries by a key" should use Coder then Validator. "Design a complete ML pipeline for fraud detection and create a report" should use multiple agents and end with Reporter.

---
