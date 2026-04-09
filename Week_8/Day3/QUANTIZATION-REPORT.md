# Day 3 - Quantisation

## Objective

Convert the fine-tuned model into multiple quantised formats to reduce size and enable deployment on different hardware.

## What is Quantisation

Quantisation reduces the precision of model weights from 32/16-bit floating point numbers to lower bit integers. This makes the model smaller and faster at the cost of a small quality loss.

## Pipeline

```
Fine-tuned adapters + Base model
        |
   Merge into FP16 model
        |
   -------------------------
   |           |           |
  INT8        INT4       GGUF
  (8-bit)    (4-bit)   (q4_0)
```

## Quantisation Results

| Format | Size (GB) | Quality vs FP16 | Runs on |
|---|---|---|---|
| FP16 | 2.05 | 100% (baseline) | GPU |
| INT8 | 1.15 | 64.0% | GPU |
| INT4 | 0.70 | 62.7% | GPU |
| GGUF q4_0 | 0.59 | ~similar to INT4 | CPU |

## Size Reduction

| Format | Size (GB) | Reduction vs FP16 |
|---|---|---|
| FP16 | 2.05 | baseline |
| INT8 | 1.15 | 1.78x smaller |
| INT4 | 0.70 | 2.93x smaller |
| GGUF q4_0 | 0.59 | 3.47x smaller |

## Quality Note

Quality is measured as text similarity between each format's response and the FP16 baseline response using SequenceMatcher. Low similarity scores do not mean wrong answers — they mean different wording. All formats produced medically correct responses to the same question.

## Tools Used

| Tool | Purpose |
|---|---|
| bitsandbytes | INT8 and INT4 quantisation |
| llama.cpp | GGUF conversion and q4_0 quantisation |
| convert_hf_to_gguf.py | Convert HuggingFace model to GGUF format |
| llama-quantize | Quantise GGUF f16 to q4_0 |

## Deliverables

| File | Description |
|---|---|
| quantized/model-fp16/ | Full precision merged model |
| quantized/model-int8/ | 8-bit quantised model |
| quantized/model-int4/ | 4-bit quantised model |
| quantized/model.gguf | GGUF q4_0 model for CPU inference |