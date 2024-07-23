# Covalent Blueprints (AI)

A collection of AI blueprints for Covalent, built using the `covalent-blueprints` library.

## Installation

```bash
pip install -U covalent-blueprints-ai
```

## Contents

This repository currently contains the following blueprints.

| name | description |
|----------|----------|
| `llama_chatbot` | Deploys a Llama-like chatbot service. |
| `sdxl_basic` | Deploys a stable-diffusion like image generator service. |
| `vllm_basic` | Deploys an LLM service using vLLM. |
| `lora_fine_tuning` | Fine-tunes and deploys a new LLM. |

## Example

### LoRA Fine-Tuning

```python
from covalent_blueprints_ai import lora_fine_tuning

# Generate blueprint
bp = lora_fine_tuning(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    num_train_epochs=2,
    data="./imdb_sample.json",  # local file
    split="train"
)

# Set/modify compute resources
bp.executors.service_executor = cc.CloudExecutor(
    gpu_type="v100",
    num_cpus=6,
    num_gpus=1,
    time_limit="01:00:00",
    memory="15GB"
)

# Run the blueprint's fine-tune and deploy workflow
fine_tuned_llm_client = bp.run()
print(fine_tuned_llm_client)
```

Output:
```
╭──────────────────────────────── Deployment Information ────────────────────────────────╮
│  Name          LoRA Fine-Tuned LLM                                                     │
│  Description   Serves a LoRA fine-tuned LLM for text generation.                       │
│  Function ID   66772d7fa1a393eb38302d77                                                │
│  Address       https://fn.prod.covalent.xyz/066772d7fa1a393eb38302d77                  │
│  Status        ACTIVE                                                                  │
│  Auth Enabled  Yes                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────── Endpoints ───────────────────────────────────────╮
│  Route        POST /generate                                                           │
│  Streaming    No                                                                       │
│  Description  Generate text from a prompt.                                             │
│                                                                                        │
│  Route        POST /stream                                                             │
│  Streaming    No                                                                       │
│  Description  Generate text from a prompt and stream the response.                     │
╰────────────────────────────────────────────────────────────────────────────────────────╯
Authorization token:
pusCwZfDngoFVfJmNsEZWz8ZJUzPPnTGmkO7_GQH0OUkch6wK6sFpbCSm_a6aXjWKJmUV6ICXMCkbwYF_qMRYQ
```

Use the service client for generation:

```python
response = fine_tuned_llm_client.generate(
    prompt="The Lord of The Rings movies are an amazing trilogy! --"
)
print(response)  # 0 - negative, 1 - positive
```
```
The Lord of The Rings movies are an amazing trilogy! -- 1
```

Tear down the service before its time limit:

```python
fine_tuned_llm_client.teardown()
```

See `examples/lora_fine_tuning.ipynb` for more details.