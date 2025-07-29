import os
import l2c


def test_core_prompt_creation(tmp_path, monkeypatch):
    path = tmp_path / "core_prompt.txt"
    monkeypatch.setattr(l2c, "CORE_PROMPT_FILE", str(path), raising=False)
    # ensure it does not exist
    if path.exists():
        path.unlink()
    prompt = l2c.load_core_prompt(str(path))
    assert path.exists()
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    assert data == prompt
    assert data.startswith("You are L\u00c9.")
