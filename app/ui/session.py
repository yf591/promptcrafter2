"""
セッション状態管理モジュール
"""

import streamlit as st
from app.config import load_categories
from app.history_manager import load_history


def initialize_session_state():
    """セッション状態の初期化"""
    if "keywords" not in st.session_state:
        st.session_state.keywords = ""
    if "keywords_input" not in st.session_state:
        st.session_state.keywords_input = ""
    if "keyword_to_add" not in st.session_state:
        st.session_state.keyword_to_add = None
    if "keyword_added_info" not in st.session_state:
        st.session_state.keyword_added_info = None
    if "clear_keywords_flag" not in st.session_state:
        st.session_state.clear_keywords_flag = False
    if "clear_positive_flag" not in st.session_state:
        st.session_state.clear_positive_flag = False
    if "clear_negative_flag" not in st.session_state:
        st.session_state.clear_negative_flag = False
    if "positive_prompt" not in st.session_state:
        st.session_state.positive_prompt = ""
    if "negative_prompt" not in st.session_state:
        st.session_state.negative_prompt = ""
    if "selected_lora" not in st.session_state:
        st.session_state.selected_lora = "None"
    if "categories" not in st.session_state:
        st.session_state.categories = load_categories()
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    if "prompt_history" not in st.session_state:
        st.session_state.prompt_history = load_history()

    # キーワードクリアの処理（ウィジェット生成前に実行）
    if st.session_state.get("clear_keywords_flag", False):
        st.session_state.keywords = ""
        st.session_state.keywords_input = ""
        st.session_state.clear_keywords_flag = False

    # Positiveプロンプトクリアの処理（ウィジェット生成前に実行）
    if st.session_state.get("clear_positive_flag", False):
        st.session_state.positive_prompt = ""
        st.session_state.clear_positive_flag = False

    # Negativeプロンプトクリアの処理（ウィジェット生成前に実行）
    if st.session_state.get("clear_negative_flag", False):
        st.session_state.negative_prompt = ""
        st.session_state.clear_negative_flag = False

    # キーワード追加の処理（ウィジェット生成前に実行）
    if st.session_state.keyword_to_add:
        current_keywords = st.session_state.keywords_input.strip()
        keyword = st.session_state.keyword_to_add
        if current_keywords:
            if keyword not in current_keywords:
                st.session_state.keywords_input = f"{current_keywords}, {keyword}"
        else:
            st.session_state.keywords_input = keyword
        st.session_state.keyword_to_add = None
