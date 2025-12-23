"""
お気に入り管理UIモジュール
"""

import streamlit as st
import pyperclip
from app.config import load_categories
from app.favorites_manager import remove_from_favorites


def render_favorites_manager():
    """お気に入り管理画面のレンダリング"""
    st.markdown("### ⭐ お気に入り管理")

    categories = st.session_state.categories

    if "Favorites" not in categories or not categories["Favorites"]:
        st.info("お気に入りがまだありません。プロンプト生成画面から追加してください。")
        return

    favorites = categories["Favorites"]

    # Positive/Negative/Keywordsのタブ
    fav_tabs = st.tabs(["➕ Positive", "➖ Negative", "🔑 Keywords"])

    # Positiveお気に入り
    with fav_tabs[0]:
        if "Positive" in favorites and favorites["Positive"]:
            st.markdown(f"**登録数: {len(favorites['Positive'])}件**")

            for i, (key, prompt) in enumerate(favorites["Positive"].items()):
                with st.expander(f"🌟 {key}"):
                    st.text_area(
                        "プロンプト内容",
                        value=prompt,
                        height=100,
                        key=f"fav_pos_{i}",
                        disabled=True,
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "📋 コピー",
                            key=f"copy_fav_pos_{i}",
                            use_container_width=True,
                        ):
                            pyperclip.copy(prompt)
                            st.success("✅ コピーしました！")

                    with col2:
                        if st.button(
                            "🗑️ 削除", key=f"del_fav_pos_{i}", use_container_width=True
                        ):
                            if remove_from_favorites(key, "Positive"):
                                st.session_state.categories = load_categories()
                                st.success(f"✅ '{key}' を削除しました！")
                                st.rerun()
        else:
            st.info("Positiveお気に入りがまだありません。")

    # Negativeお気に入り
    with fav_tabs[1]:
        if "Negative" in favorites and favorites["Negative"]:
            st.markdown(f"**登録数: {len(favorites['Negative'])}件**")

            for i, (key, prompt) in enumerate(favorites["Negative"].items()):
                with st.expander(f"🌟 {key}"):
                    st.text_area(
                        "プロンプト内容",
                        value=prompt,
                        height=100,
                        key=f"fav_neg_{i}",
                        disabled=True,
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "📋 コピー",
                            key=f"copy_fav_neg_{i}",
                            use_container_width=True,
                        ):
                            pyperclip.copy(prompt)
                            st.success("✅ コピーしました！")

                    with col2:
                        if st.button(
                            "🗑️ 削除", key=f"del_fav_neg_{i}", use_container_width=True
                        ):
                            if remove_from_favorites(key, "Negative"):
                                st.session_state.categories = load_categories()
                                st.success(f"✅ '{key}' を削除しました！")
                                st.rerun()
        else:
            st.info("Negativeお気に入りがまだありません。")

    # Keywordsお気に入り
    with fav_tabs[2]:
        if "Keywords" in favorites and favorites["Keywords"]:
            st.markdown(f"**登録数: {len(favorites['Keywords'])}件**")

            for i, (key, keywords) in enumerate(favorites["Keywords"].items()):
                with st.expander(f"🌟 {key}"):
                    st.text_area(
                        "キーワード内容",
                        value=keywords,
                        height=100,
                        key=f"fav_kwd_{i}",
                        disabled=True,
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "📋 コピー",
                            key=f"copy_fav_kwd_{i}",
                            use_container_width=True,
                        ):
                            pyperclip.copy(keywords)
                            st.success("✅ コピーしました！")

                    with col2:
                        if st.button(
                            "🗑️ 削除", key=f"del_fav_kwd_{i}", use_container_width=True
                        ):
                            if remove_from_favorites(key, "Keywords"):
                                st.session_state.categories = load_categories()
                                st.success(f"✅ '{key}' を削除しました！")
                                st.rerun()
        else:
            st.info("Keywordsお気に入りがまだありません。")
