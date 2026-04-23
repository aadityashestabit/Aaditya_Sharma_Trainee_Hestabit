## What Tool Calling Actually Means

In Days 1 and 2 every agent only generated text. It could talk about running code, it could describe what a file contains, it could explain what SQL to write — but it could not actually do any of those things. The output was always just words.

Day 3 changes that completely. When an agent calls a tool, something real happens. A Python script executes in a subprocess on your machine and returns real output. A file gets written to your disk and you can open it. A SQL query runs against a real SQLite database and rows come back. The agent is no longer describing the world — it is acting on it.

This is a fundamental shift in what an agent can do.

---

## The Planner

Before any work happens, the Planner reads the user query and figures out which agents need to run and in what order. It has three agents available to it — FILE, DB, and CODE — and it assigns each step of the work to whichever one is most appropriate.

For a query like "read my CSV and save the analysis as a report", the Planner recognizes that reading is a file operation, analysis is a code operation, and saving is another file operation. It creates a three-step plan automatically. You do not have to tell it how to break the work down.

The Planner outputs a simple JSON list of steps. Each step says which agent should handle it and what that agent needs to do. Once the plan is ready, execution begins.

---

## Sequential Chaining

Unlike Day 2 where tasks could run in parallel, Day 3 runs everything one step at a time. This is because the steps depend on each other in ways that make parallelism impossible.

You cannot analyze a file before reading it. You cannot save a report before generating it. You cannot insert into a database table before creating it. Each step produces output that the next step needs.

The way this works is straightforward. After each step completes, its output gets added to a running list. When the next step starts, that entire list gets passed to it as context. So when the CODE agent runs, it automatically has access to whatever the FILE agent read. When the FILE agent runs to write the report, it automatically has the analysis that the CODE agent produced. Nothing needs to be explicitly connected — it all flows through the shared context.

---

## The FILE Agent

The FILE agent is responsible for everything that touches the filesystem. It can read files, write files, append to existing files, and list the contents of directories.

Reading a CSV is treated differently from reading a plain text file. When you read a CSV the agent does not just return the raw content — it also calculates statistics for each column. For numeric columns you get the minimum, maximum, mean, and standard deviation. For text columns you get the count of unique values. This gives the CODE agent much richer context when it receives the data.

Writing CSVs is also handled separately from writing other files. CSVs need proper escaping — if a field contains a comma, a plain text write would break the file format. The write_csv tool uses Python's csv library to handle this correctly. Using write_file for a CSV is a mistake that produces broken output.

---

## The DB Agent

The DB agent works with SQLite databases. SQLite is a file-based database — the entire database lives in a single `.db` file on your disk, no server needed. This makes it ideal for local agent work.

The first thing the DB agent always does before any query is inspect the schema. It looks at what tables exist, what columns they have, how many rows they contain, and shows a few sample rows. An empty database is not a problem — it just means the agent needs to create the tables first, and it does.

For inserting data the agent always combines the CREATE TABLE and INSERT statements into a single script. This prevents the common failure where it tries to insert into a table that does not exist yet.

For large amounts of data — anything over 50 rows — the DB agent defers to the CODE agent. Generating 1000 INSERT statements in SQL is unreliable. Generating them in a Python loop is not.

---

## The CODE Agent

The CODE agent writes Python and executes it. Every piece of code it generates runs as a real subprocess on your machine and the output comes back.

The most useful feature is auto-install. Before executing any code, the agent scans all the import statements and tries to import each package. If a package is missing it installs it automatically using pip. The install happens silently and the code then runs normally. This means the agent can use any library — matplotlib, pandas, seaborn, numpy — without you having to pre-install anything.

Some package names are different from their import names. sklearn is the import name but scikit-learn is the pip package. PIL is the import name but Pillow is the pip package. The agent knows these mappings and handles them correctly.

---

## Two Different Models

The Planner and the tool agents use different models. This is not an accident — it reflects a real difference in what each one needs to do.

The Planner just needs to read a query and output a JSON list. A small, fast model does this perfectly well. Using a large model for this would be wasteful.

The tool agents need to actually call functions. They receive a task, decide which tool to use, and generate a structured function call that the framework executes. This requires a model that reliably generates correct JSON function calls. Not all models do this well. Using the wrong model here results in malformed tool calls that fail at execution.

So the Planner uses llama-3.1-8b-instant — fast and good at JSON. The tool agents use llama-4-scout-17b-16e-instruct — larger and reliable at function calling.

---

## Example: Three Steps Working Together

When you ask "read sales.csv, find the top products by revenue, and save the report":

The Planner creates three steps. The FILE agent reads the CSV and returns not just the raw rows but also statistics showing which columns are numeric and what their ranges are. The CODE agent receives that data, writes Python to sort by the revenue column and extract the top entries, executes it, and returns the result. The FILE agent receives that result and writes it to a text file on disk.

At no point does any agent need to be told what the previous agent did. Every agent automatically receives everything that came before it. The pipeline is self-connecting.

---

## Execution Flow Diagram

```
User: "Read sales.csv, find top 3 products by revenue, save to report.txt"
    |
    v
[Planner]
  ├── Step 1: FILE  → Read sales.csv
  ├── Step 2: CODE  → Analyze data, find top 3 by revenue
  └── Step 3: FILE  → Write results to report.txt
    |
    v
[Step 1 — FILE Agent]
  calls read_file("sales.csv")
  returns: raw CSV rows + column statistics
    |
    v  (output passed to next step as context)
    |
[Step 2 — CODE Agent]
  receives: CSV content from Step 1
  writes Python → executes → returns analysis output
    |
    v  (output passed to next step as context)
    |
[Step 3 — FILE Agent]
  receives: analysis from Step 2
  calls write_file("report.txt", analysis)
  returns: [OK] Written to report.txt
    |
    v
[Pipeline Complete]
    |
    v
report.txt exists on disk with the analysis inside
```

---

## File Structure

```
Day3/
├── tools/
│   ├── file_agent.py       
│   ├── db_agent.py         
│   └── code_executor.py  
├── loader.py               
├── run_day3.py             
└── TOOL-CHAIN.md          
```

---