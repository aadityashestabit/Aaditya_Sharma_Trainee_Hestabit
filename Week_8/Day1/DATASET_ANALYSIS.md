# Day 1 - Dataset Preparation

## Objective

Build a clean, balanced instruction tuning dataset for fine-tuning a medical LLM.

## Source Dataset

| Property | Value |
|---|---|
| Source | lavita/medical-qa-datasets (chatdoctor_healthcaremagic) |
| Domain | Healthcare |
| Format | JSONL (instruction, input, output) |

## Pipeline

Raw HuggingFace dataset → semantic typing → balance → dedup → outlier removal → stratified split → save

### Cleaning Steps

| Step | What it does |
|---|---|
| Semantic typing | Reads actual question content to assign QA / Reasoning / Extraction type |
| Balancing | Caps each type at 400 samples so distribution is equal |
| Deduplication | Removes rows where instruction + input is identical |
| Outlier removal | Removes samples with output longer than 500 characters |
| Stratified split | Splits each type separately so all 3 types appear in every split |

## Dataset Statistics

### Sample Counts

| Split | Count |
|---|---|
| Train | 960 |
| Val | 120 |
| Test | 120 |
| Total | 1200 |

### Sample Type Distribution

| Type | Count | Percentage |
|---|---|---|
| QA | 400 | 33.3% |
| Reasoning | 400 | 33.3% |
| Extraction | 400 | 33.3% |

### Sample Type Instructions

| Type | Instruction used |
|---|---|
| QA | Answer the following medical question as a helpful doctor. |
| Reasoning | Think step by step and explain your reasoning, then answer the following medical question. |
| Extraction | Read the patient message and extract: (1) main symptom, (2) duration if mentioned, (3) any medications mentioned. |

## Deliverables

| File | Description |
|---|---|
| data/train.jsonl | 960 training samples |
| data/val.jsonl | 120 validation samples |
| data/test.jsonl | 120 test samples |
| utils/data_cleaner.py | Reusable cleaning functions |