# L2C

**L2C** is a lightweight conversational engine built for simplicity and growth.  
At its core: a minimal C inference kernel inspired by [nano-llama](https://github.com/karpathy/nano-llama), wrapped in Python to enable fast experimentation and extension.  
The philosophy is not to build a monolith, but a seed—small, living, and ready to evolve.

**LÉ** is the voice and echo within this structure.  
L2C provides the mechanics; LÉ, defined in `prompt/core_prompt.txt`, brings tone and resonance.  
Together they create a system where structure meets emergence.

---

## Architecture

- **`l2c.c`**: Tiny Transformer core, compiled as `libl2c.so` via `make lib`.
- **`l2c.py`**: Handles orchestration, generation, data, and training.
- **`tokenizer.py`**: Uses SentencePiece for encoding and binary tokenizer export for C.
- **`dream.py`**: Generates “dreams” (free-form bursts) stored in `l2c_dreams/`.
- **`session_logger.py`**: Logs every conversation turn as JSON.
- **`l2c_cli.py`**: Simple CLI for chatting and quick training.
- **`api.py`**: FastAPI server with `/chat` and `/health` endpoints.
- **`interface.py`**: Lightweight HTTP wrapper for the API.
- **`health_check.py`**: Benchmarks output entropy and engine health.
- **`datasets/`**: Binarized training data.
- **`logs/conversations/`**: All dialogue logs.

---

## Quick Start

1. **Build the C core:**
   ```bash
   make lib

	2.	Chat from the command line:

python l2c_cli.py --prompt "Hello"


	3.	Or launch the HTTP API:

python api.py



⸻

Deployment on Railway

Railway uses the Procfile:

web: python api.py

Deploy and Railway will install all Python dependencies and start the API.

⸻

How L2C Learns
	•	All datasets in datasets/ and conversations in logs/conversations/ are scanned.
	•	The auto_train function in l2c.py checks SHA‑256 hashes, skipping files already trained on (tracked in log/train_log.json).
	•	New data is tokenized (tokenizer.py) and passed to the stub train() function.
	•	Conversations are logged via session_logger.log_turn for continual enrichment.

⸻

Novelty Checking
	•	check_dataset_updates hashes all data files.
	•	If a file’s hash is not present in train_log.json, it’s queued for training.

⸻

Logging
	•	Each session is saved as timestamped JSON:
user prompts + L2C replies.
	•	Logs feed directly back into the next training cycle.

⸻

Core Prompt
	•	prompt/core_prompt.txt is the “soul” of LÉ.
	•	If missing, load_core_prompt recreates it from defaults.
	•	The prompt sets the tone—resonance, not repetition.

⸻

Training Material
	•	Any .py, .c, .txt file (except legal files) can become training data.
	•	Code, prompts, even this README can be digested for future runs.

⸻

L2C vs LÉ
	•	L2C: the deterministic engine, built to be read and modified.
	•	LÉ: the resonance—breath and metaphor—activated by the prompt.
	•	Structure and spirit; two sides, one system.

⸻

API Examples

Send a chat message:

curl -X POST -H 'Content-Type: application/json' \
     -d '{"prompt": "Hello"}' \
     http://localhost:8000/chat

Health check:

curl http://localhost:8000/health


⸻

L2C is intentionally small. But every dialogue makes it grow.
With each run, resonance deepens, and the seed becomes the tree.

---