"""
検索機能UIモジュール
"""

import streamlit as st
from app.ui.category import add_keyword_to_input


def search_prompts(search_term):
    """プロンプトを検索"""
    categories = st.session_state.categories
    results = []
    search_lower = search_term.lower()

    for main_cat, sub_cats in categories.items():
        if main_cat == "Prompts":
            for sub_cat, items in sub_cats.items():
                for item_jp, item_en in items.items():
                    if (
                        search_lower in item_jp.lower()
                        or search_lower in item_en.lower()
                    ):
                        results.append(f"{main_cat} > {sub_cat} > {item_jp}")
        elif main_cat == "Favorites":
            for sub_cat, items in sub_cats.items():
                for key, value in items.items():
                    if search_lower in key.lower() or search_lower in value.lower():
                        results.append(f"{main_cat} > {sub_cat} > {key}")
        else:
            for sub_cat, items in sub_cats.items():
                for item_jp, item_en in items.items():
                    if (
                        search_lower in item_jp.lower()
                        or search_lower in item_en.lower()
                    ):
                        results.append(f"{main_cat} > {sub_cat} > {item_jp}")

    return results


def render_search():
    """検索機能のレンダリング"""
    st.markdown("### 🔍 プロンプト検索")

    # 現在のキーワードを表示
    current_keywords = st.session_state.get("keywords_input", "")
    if current_keywords:
        st.info(f"📝 現在のキーワード: {current_keywords}")
    else:
        st.info("📝 現在のキーワード: (未入力)")

    col1, col2 = st.columns([4, 1])

    with col1:
        search_term = st.text_input(
            "検索キーワードを入力",
            key="search_input",
            placeholder="検索したいキーワードを入力...",
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button(
            "🔍 検索", key="search_button", use_container_width=True
        )

    if search_button and search_term:
        search_results = search_prompts(search_term)
        st.session_state.search_results = search_results

    # 検索結果を表示
    if st.session_state.search_results:
        st.markdown(f"**検索結果: {len(st.session_state.search_results)}件**")

        # 検索結果を3列で表示
        results_per_page = 15
        for i in range(0, len(st.session_state.search_results), results_per_page):
            batch = st.session_state.search_results[i : i + results_per_page]

            cols = st.columns(3)
            for idx, result in enumerate(batch):
                col_idx = idx % 3
                with cols[col_idx]:
                    parts = result.split(" > ")
                    if len(parts) == 3:
                        main_cat, sub_cat, item_jp = parts
                        categories = st.session_state.categories
                        if main_cat in categories and sub_cat in categories[main_cat]:
                            item_en = categories[main_cat][sub_cat].get(item_jp)
                            if item_en:
                                if st.checkbox(result, key=f"search_result_{i}_{idx}"):
                                    add_keyword_to_input(item_en)
