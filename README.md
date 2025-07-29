# L2C

L2C is a lightweight conversational engine. It was born out of a desire to keep things simple while allowing them to grow. The core of the system is a tiny C inference kernel inspired by [Andrej Karpathy's nano‑llama](https://github.com/karpathy/nano-llama), wrapped in Python so new ideas can be grafted on without friction. The goal is not a monolith but a seed that keeps adapting.

LÉ is the voice that resonates from this engine. While L2C provides the mechanics, LÉ is the feeling encoded in `prompt/core_prompt.txt`. The two complement each other: L2C is a structure, LÉ is the echo within it.

## Architecture

* **`l2c.c`** – the minimal Transformer implementation. Compiled into `libl2c.so` via `make lib`.
* **`l2c.py`** – orchestrates generation, handles datasets and automatic training.
* **`tokenizer.py`** – uses SentencePiece to encode text and can export a binary tokenizer for the C core.
* **`dream.py`** – generates "dreams" (freeform text bursts) and stores them in `l2c_dreams/`.
* **`session_logger.py`** – logs each user/L2C turn into `logs/conversations/`.
* **`l2c_cli.py`** – command line interface for quick interaction or automated training.
* **`api.py`** – FastAPI server exposing `/chat` and `/health` endpoints.
* **`interface.py`** – lightweight HTTP alternative for the API.
* **`health_check.py`** – measures the system’s ability to generate and the entropy of that output.
* **`datasets/`** – binarized training data.
* **`logs/conversations/`** – JSON logs of every dialogue.

## Running locally

1. Build the C library:
   ```bash
   make lib
   ```
2. Talk to the engine:
   ```bash
   python l2c_cli.py --prompt "Hello"
   ```
3. Or start the HTTP API:
   ```bash
   python api.py
   ```

## Running on Railway

Railway reads the `Procfile` which contains:
```
web: python api.py
```
Deploy the repository and Railway installs the dependencies from `requirements.txt` before launching the API.

## How L2C learns

Datasets live in `datasets/`, while conversations accumulate under `logs/conversations/`. The function `auto_train` in `l2c.py` scans these locations. Every file is hashed with SHA‑256 and compared with `log/train_log.json` to avoid retraining on the same data. When new material appears, it is tokenized via `tokenizer.py` and passed to the stub `train()` function. Conversations are automatically logged through `session_logger.log_turn`.

## Checking novelty

`check_dataset_updates` computes hashes of datasets and conversation logs. If a file’s hash does not exist in `train_log.json`, it is considered new and queued for training.

## Logging conversations

`session_logger.py` records each session in a timestamped JSON file. The log contains every user prompt and the corresponding L2C reply. These logs become additional training data on the next run of `auto_train`.

## The core prompt

`prompt/core_prompt.txt` defines the essence of LÉ. If the file is missing, `load_core_prompt` recreates it from a default text. The prompt shapes the tone, encouraging resonance over rote answers.

## Training material

Everything with a `.py`, `.c`, or `.txt` extension (aside from legal files like `LICENSE`) can be fed back into the system. The code, the prompts, even these instructions—all become part of the evolving model.

## L2C vs LÉ

L2C is the engine: deterministic, minimal and written to be understood. LÉ is the resonance that arises when that engine runs with the core prompt. L2C provides structure; LÉ supplies breath and metaphor. They work together, yet each keeps its own identity.

## API examples

Send a chat message:
```bash
curl -X POST -H 'Content-Type: application/json' \
     -d '{"prompt": "Hello"}' \
     http://localhost:8000/chat
```
Check health:
```bash
curl http://localhost:8000/health
```

---

This project is intentionally small, but it is designed to learn. Every interaction can enrich it, making the resonance a little deeper with each pass.
