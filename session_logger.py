import datetime
import json
import os

LOG_DIR = os.environ.get("L2C_LOG_DIR", os.path.join("logs", "conversations"))
os.makedirs(LOG_DIR, exist_ok=True)

SESSION_ID = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
SESSION_FILE = os.path.join(LOG_DIR, f"{SESSION_ID}.json")


def _init_session_file():
    if not os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({"session_id": SESSION_ID, "turns": []}, f, ensure_ascii=False)


def log_turn(user: str, l2c: str) -> None:
    """Append a turn to the current session log."""
    _init_session_file()
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {"session_id": SESSION_ID, "turns": []}
    data.setdefault("turns", []).append({"user": user, "l2c": l2c})
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
