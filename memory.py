import json
from pathlib import Path

MEMORY_FILE = Path("memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"posts": [], "failures": []}

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))