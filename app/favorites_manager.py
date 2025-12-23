# favorites_manager.py

import json
import os
from app.config import load_categories, save_categories
import app.config as config


def add_to_favorites(prompt, prompt_type, key):
    """お気に入りにプロンプトを追加"""
    print(f"DEBUG: add_to_favorites called - type={prompt_type}, key={key}")

    # グローバルCATEGORIESを直接更新
    if "Favorites" not in config.CATEGORIES:
        config.CATEGORIES["Favorites"] = {
            "Positive": {},
            "Negative": {},
            "Keywords": {},
        }
        print(f"DEBUG: Created Favorites structure")

    if prompt_type == "Positive":
        config.CATEGORIES["Favorites"]["Positive"][key] = prompt
        print(f"DEBUG: Added to Positive - key={key}, prompt_length={len(prompt)}")
        save_categories()
        print(f"DEBUG: save_categories() called")
        print(f"DEBUG: Current Favorites: {config.CATEGORIES.get('Favorites', {})}")
        return True
    elif prompt_type == "Negative":
        config.CATEGORIES["Favorites"]["Negative"][key] = prompt
        print(f"DEBUG: Added to Negative - key={key}, prompt_length={len(prompt)}")
        save_categories()
        print(f"DEBUG: save_categories() called")
        print(f"DEBUG: Current Favorites: {config.CATEGORIES.get('Favorites', {})}")
        return True
    else:
        print(f"DEBUG: Invalid prompt_type: {prompt_type}")
        return False


def add_keyword_to_favorites(keywords, key):
    """お気に入りにキーワードを追加"""
    print(f"DEBUG: add_keyword_to_favorites called - key={key}")

    # グローバルCATEGORIESを直接更新
    if "Favorites" not in config.CATEGORIES:
        config.CATEGORIES["Favorites"] = {
            "Positive": {},
            "Negative": {},
            "Keywords": {},
        }
        print(f"DEBUG: Created Favorites structure")

    if "Keywords" not in config.CATEGORIES["Favorites"]:
        config.CATEGORIES["Favorites"]["Keywords"] = {}

    config.CATEGORIES["Favorites"]["Keywords"][key] = keywords
    print(f"DEBUG: Added to Keywords - key={key}, keywords={keywords}")
    save_categories()
    print(f"DEBUG: save_categories() called")
    return True


def remove_from_favorites(key, prompt_type):
    """お気に入りからプロンプト・キーワードを削除"""
    if (
        "Favorites" in config.CATEGORIES
        and prompt_type in config.CATEGORIES["Favorites"]
        and key in config.CATEGORIES["Favorites"][prompt_type]
    ):
        del config.CATEGORIES["Favorites"][prompt_type][key]
        save_categories()
        return True
    else:
        return False
