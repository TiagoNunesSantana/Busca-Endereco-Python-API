import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("historico_ceps.json")

def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def add_history(item: dict) -> None:
    hist = load_history()
    item = dict(item)
    item["timestamp"] = datetime.now().isoformat(timespec="seconds")
    hist.insert(0, item)
    hist = hist[:200]
    HISTORY_FILE.write_text(
        json.dumps(hist, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )