# Day 4 - Inference Optimisation and Benchmarking

## Objective

Benchmark all model variants across four metrics — tokens per second, latency, VRAM usage and accuracy — to identify the best model for each deployment scenario.

## Models Tested

| Model | Description |
|---|---|
| Base (no FT) | TinyLlama 1.1B with no fine-tuning |
| Fine-tuned FP16 | Fine-tuned model at full float16 precision |
| Fine-tuned INT4 | Fine-tuned model quantised to 4-bit |
| GGUF q4_0 | Fine-tuned model in GGUF format, run on CPU |

## Benchmark Results

### Speed (tokens per second)

| Model | Tokens/sec |
|---|---|
| Base (no FT) | 10.66 |
| Fine-tuned FP16 | 40.16 |
| Fine-tuned INT4 | 16.16 |
| GGUF q4_0 (CPU) | 27.70 |

### Latency (seconds for 100 tokens)

| Model | Latency (sec) |
|---|---|
| Base (no FT) | 9.38 |
| Fine-tuned FP16 | 2.49 |
| Fine-tuned INT4 | 6.19 |
| GGUF q4_0 (CPU) | 3.61 |

### VRAM Usage

| Model | VRAM (GB) |
|---|---|
| Base (no FT) | 2.07 |
| Fine-tuned FP16 | 2.07 |
| Fine-tuned INT4 | 0.75 |
| GGUF q4_0 (CPU) | 0.00 |

### Accuracy vs Fine-tuned FP16

| Model | Similarity (%) |
|---|---|
| Base (no FT) | 9.0 |
| Fine-tuned FP16 | 100.0 |
| Fine-tuned INT4 | 37.5 |
| GGUF q4_0 (CPU) | 24.2 |

## Key Findings

| Finding | Detail |
|---|---|
| Fine-tuning impact | Fine-tuned FP16 is 3.76x faster than base and 9x more similar in response style |
| Best GPU model | Fine-tuned FP16 — fastest at 40.16 tok/s with 2.49s latency |
| Best VRAM efficiency | Fine-tuned INT4 — only 0.75 GB, fits on any GPU |
| Best CPU model | GGUF q4_0 — 27.70 tok/s on CPU with zero GPU requirement |
| Surprising result | GGUF on CPU (27.70) outperforms INT4 on GPU (16.16) due to llama.cpp CPU optimisations |

## Inference Features Tested

| Feature | Status |
|---|---|
| Single prompt inference | Done |
| Streaming output | Done |
| Batch / multi-prompt inference | Done (3 prompts) |
| KV caching | Enabled via use_cache=True |

## Deliverables

| File | Description |
|---|---|
| benchmarks/results.csv | All benchmark numbers in CSV format |
| benchmarks/benchmark_chart.png | 4-panel chart (speed, VRAM, latency, accuracy) |
| inference/test_inference.py | Standalone inference script |