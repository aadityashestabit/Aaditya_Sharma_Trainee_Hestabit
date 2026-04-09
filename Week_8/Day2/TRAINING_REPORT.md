# Day 2 - QLoRA Fine-Tuning

## Objective

Fine-tune TinyLlama 1.1B on the healthcare dataset using QLoRA — a parameter efficient method that trains only a small fraction of the model weights.

## Model

| Property | Value |
|---|---|
| Base model | TinyLlama/TinyLlama-1.1B-Chat-v1.0 |
| Total parameters | 1.1 Billion |
| Fine-tuning method | QLoRA (Quantised LoRA) |
| Hardware | T4 GPU (15 GB VRAM) |

## QLoRA Configuration

| Parameter | Value |
|---|---|
| Quantisation | 4-bit (nf4) |
| LoRA rank (r) | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Target modules | q_proj, k_proj, v_proj, o_proj |

## Training Configuration

| Parameter | Value |
|---|---|
| Epochs | 3 |
| Learning rate | 2e-4 |
| Batch size | 4 |
| Gradient accumulation steps | 4 |
| Effective batch size | 16 |
| Max sequence length | 512 |
| Optimizer | paged_adamw_8bit |
| Mixed precision | fp16 |
| Gradient checkpointing | True |

## Parameter Efficiency

| Metric | Value |
|---|---|
| Total parameters | 616,593,408 |
| Trainable parameters | 4,505,600 |
| Frozen parameters | 612,087,808 |
| Trainable percentage | 0.73% |

## Training Results

| Metric | Value |
|---|---|
| Starting train loss | 2.71 |
| Final train loss | 2.14 |
| Final val loss | 2.16 |
| Loss reduction | 0.57 |

## Prompt Template

```
<|system|>
You are a helpful medical assistant.
<|user|>
{instruction}
{input}
<|assistant|>
{output}
```

## Deliverables

| File | Description |
|---|---|
| adapters/adapter_model.safetensors | Trained LoRA weights (~17 MB) |
| adapters/adapter_config.json | LoRA configuration |
| adapters/tokenizer.json | Tokenizer |
| adapters/loss_curve.png | Training and validation loss curve |