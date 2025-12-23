# history_manager.py
"""
プロンプト履歴を管理するモジュール
"""

import json
import os
from datetime import datetime

HISTORY_FILE = "prompt_history.json"
MAX_HISTORY_SIZE = 100


def load_history():
    """履歴をロード"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    return []


def save_history(history):
    """履歴を保存"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def add_to_history(keywords, positive_prompt, negative_prompt, lora="None"):
    """履歴に追加"""
    history = load_history()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "keywords": keywords,
        "positive_prompt": positive_prompt,
        "negative_prompt": negative_prompt,
        "lora": lora,
    }

    # 先頭に追加
    history.insert(0, entry)

    # 最大サイズを超えたら古いものを削除
    if len(history) > MAX_HISTORY_SIZE:
        history = history[:MAX_HISTORY_SIZE]

    save_history(history)
    return True


def clear_history():
    """履歴をクリア"""
    save_history([])
    return True


def delete_history_item(index):
    """特定の履歴項目を削除"""
    history = load_history()
    if 0 <= index < len(history):
        del history[index]
        save_history(history)
        return True
    return False
