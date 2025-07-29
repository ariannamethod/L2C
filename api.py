import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
import uvicorn
import l2c
import os

app = FastAPI()

logger = logging.getLogger(__name__)


@app.post("/chat", response_class=ORJSONResponse)
async def chat(data: dict):
    prompt = data.get("prompt", "") if isinstance(data, dict) else ""
    logger.info("/chat called length=%d", len(prompt))
    try:
        text = l2c.generate(prompt)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("generation failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"response": text}


@app.get("/health", response_class=ORJSONResponse)
async def health():
    metrics = l2c.health()
    entries = l2c._load_train_log()  # type: ignore[attr-defined]
    return {
        "online": metrics.get("available", False),
        "logs_read": bool(entries),
        "unique_datapoints": len(entries),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
