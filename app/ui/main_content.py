"""
メインコンテンツUIモジュール
"""

import streamlit as st
import pyperclip
from app.prompt_generator import generate_prompt
from app.config import load_categories
from app.history_manager import add_to_history, load_history
from app.favorites_manager import add_to_favorites, add_keyword_to_favorites


def generate_prompts(mode="both"):
    """プロンプトを生成"""
    keywords = st.session_state.keywords.strip()

    if not keywords:
        st.warning("⚠️ キーワードを入力してください。")
        return

    selected_lora = (
        st.session_state.selected_lora
        if st.session_state.selected_lora != "None"
        else ""
    )

    with st.spinner("プロンプトを生成中..."):
        positive_prompt, negative_prompt = generate_prompt(
            keywords, selected_lora, mode
        )

        if mode == "positive_only":
            st.session_state.positive_prompt = positive_prompt
        elif mode == "negative_only":
            st.session_state.negative_prompt = negative_prompt
        else:
            st.session_state.positive_prompt = positive_prompt
            st.session_state.negative_prompt = negative_prompt

        # 履歴に追加
        add_to_history(
            keywords,
            st.session_state.positive_prompt,
            st.session_state.negative_prompt,
            selected_lora,
        )
        st.session_state.prompt_history = load_history()

    st.success("✅ プロンプトを生成しました！")
    st.rerun()


def save_to_favorites(prompt_type, key):
    """お気に入りに保存する実行関数"""
    prompt = (
        st.session_state.positive_prompt
        if prompt_type == "Positive"
        else st.session_state.negative_prompt
    )

    if not prompt.strip():
        st.error(f"⚠️ {prompt_type}プロンプトが空です。")
        return False

    if not key.strip():
        st.error("⚠️ キーを入力してください。")
        return False

    result = add_to_favorites(prompt, prompt_type, key)
    if result:
        # カテゴリを再読み込みしてセッションステートを更新
        import app.config as config

        config.CATEGORIES = load_categories()
        st.session_state.categories = config.CATEGORIES
        st.session_state[f"show_fav_form_{prompt_type}"] = False
        st.session_state[f"fav_key_{prompt_type}"] = ""
        st.success(
            f"✅ {prompt_type}プロンプトをお気に入りに追加しました！（キー: {key}）"
        )
        return True
    else:
        st.error("❌ お気に入りへの追加に失敗しました。")
        return False


def save_keywords_to_favorites(key):
    """キーワードをお気に入りに保存する実行関数"""
    keywords = st.session_state.get("keywords_input", "").strip()

    if not keywords:
        st.error("⚠️ キーワードが空です。")
        return False

    if not key.strip():
        st.error("⚠️ キーを入力してください。")
        return False

    result = add_keyword_to_favorites(keywords, key)
    if result:
        # カテゴリを再読み込みしてセッションステートを更新
        import app.config as config

        config.CATEGORIES = load_categories()
        st.session_state.categories = config.CATEGORIES
        st.session_state.show_fav_form_Keywords = False
        st.session_state.fav_key_Keywords = ""
        st.success(f"✅ キーワードをお気に入りに追加しました！（キー: {key}）")
        return True
    else:
        st.error("❌ お気に入りへの追加に失敗しました。")
        return False


def render_main_content():
    """メインコンテンツのレンダリング"""
    st.markdown(
        '<div class="main-header">🎨 PromptCrafter</div>', unsafe_allow_html=True
    )
    st.markdown("**Stable Diffusion用プロンプト生成ツール - Streamlit版**")

    # キーワード入力
    st.markdown("### ✏️ キーワード入力")
    st.text_area(
        "プロンプト生成に使用するキーワードを入力（カンマ区切り）",
        value=st.session_state.get("keywords_input", ""),
        height=100,
        key="keywords_input",
        placeholder="例: beautiful landscape, sunset, mountains",
    )
    st.session_state.keywords = st.session_state.get("keywords_input", "")

    # 生成ボタン
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button(
            "✨ プロンプト生成（両方）", key="generate_both", use_container_width=True
        ):
            generate_prompts("both")

    with col2:
        if st.button(
            "➕ Positiveのみ生成", key="generate_positive", use_container_width=True
        ):
            generate_prompts("positive_only")

    with col3:
        if st.button(
            "➖ Negativeのみ生成", key="generate_negative", use_container_width=True
        ):
            generate_prompts("negative_only")

    with col4:
        if st.button(
            "⭐ お気に入りに追加", key="fav_keywords", use_container_width=True
        ):
            st.session_state.show_fav_form_Keywords = True
            st.rerun()

    with col5:
        if st.button(
            "🗑️ キーワードをクリア", key="clear_keywords", use_container_width=True
        ):
            st.session_state.clear_keywords_flag = True
            st.rerun()

    # お気に入り追加フォーム（Keywords）
    if st.session_state.get("show_fav_form_Keywords", False):
        with st.form(f"add_to_favorites_Keywords", clear_on_submit=True):
            st.markdown("#### お気に入りに追加（キーワード）")
            key_input = st.text_input(
                "お気に入りのキーを入力",
                key="fav_key_input_Keywords",
                placeholder="例: 風景写真用",
            )
            col_submit, col_cancel = st.columns(2)
            with col_submit:
                submitted = st.form_submit_button("💾 保存", use_container_width=True)
            with col_cancel:
                cancelled = st.form_submit_button(
                    "❌ キャンセル", use_container_width=True
                )

            if submitted:
                if save_keywords_to_favorites(key_input):
                    st.rerun()
            if cancelled:
                st.session_state.show_fav_form_Keywords = False
                st.rerun()

    st.markdown("---")

    # Positiveプロンプト表示
    st.markdown("### ➕ Positive Prompt")
    st.text_area(
        "生成されたPositiveプロンプト",
        value=st.session_state.positive_prompt,
        height=150,
        key="positive_prompt",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(
            "📋 Positiveをコピー", key="copy_positive", use_container_width=True
        ):
            pyperclip.copy(st.session_state.positive_prompt)
            st.success("✅ Positiveプロンプトをクリップボードにコピーしました！")

    with col2:
        if st.button(
            "⭐ お気に入りに追加", key="fav_positive", use_container_width=True
        ):
            st.session_state.show_fav_form_Positive = True
            st.rerun()

    with col3:
        if st.button("🗑️ クリア", key="clear_positive", use_container_width=True):
            st.session_state.clear_positive_flag = True
            st.rerun()

    # お気に入り追加フォーム（Positive）
    if st.session_state.get("show_fav_form_Positive", False):
        with st.form(f"add_to_favorites_Positive", clear_on_submit=True):
            st.markdown("#### お気に入りに追加（Positive）")
            key_input = st.text_input(
                "お気に入りのキーを入力",
                key="fav_key_input_Positive",
                placeholder="例: 美しい風景",
            )
            col_submit, col_cancel = st.columns(2)
            with col_submit:
                submitted = st.form_submit_button("💾 保存", use_container_width=True)
            with col_cancel:
                cancelled = st.form_submit_button(
                    "❌ キャンセル", use_container_width=True
                )

            if submitted:
                if save_to_favorites("Positive", key_input):
                    st.rerun()
            if cancelled:
                st.session_state.show_fav_form_Positive = False
                st.rerun()

    st.markdown("---")

    # Negativeプロンプト表示
    st.markdown("### ➖ Negative Prompt")
    st.text_area(
        "生成されたNegativeプロンプト",
        value=st.session_state.negative_prompt,
        height=150,
        key="negative_prompt",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(
            "📋 Negativeをコピー", key="copy_negative", use_container_width=True
        ):
            pyperclip.copy(st.session_state.negative_prompt)
            st.success("✅ Negativeプロンプトをクリップボードにコピーしました！")

    with col2:
        if st.button(
            "⭐ お気に入りに追加", key="fav_negative", use_container_width=True
        ):
            st.session_state.show_fav_form_Negative = True
            st.rerun()

    with col3:
        if st.button("🗑️ クリア", key="clear_negative", use_container_width=True):
            st.session_state.clear_negative_flag = True
            st.rerun()

    # お気に入り追加フォーム（Negative）
    if st.session_state.get("show_fav_form_Negative", False):
        with st.form(f"add_to_favorites_Negative", clear_on_submit=True):
            st.markdown("#### お気に入りに追加（Negative）")
            key_input = st.text_input(
                "お気に入りのキーを入力",
                key="fav_key_input_Negative",
                placeholder="例: 低品質",
            )
            col_submit, col_cancel = st.columns(2)
            with col_submit:
                submitted = st.form_submit_button("💾 保存", use_container_width=True)
            with col_cancel:
                cancelled = st.form_submit_button(
                    "❌ キャンセル", use_container_width=True
                )

            if submitted:
                if save_to_favorites("Negative", key_input):
                    st.rerun()
            if cancelled:
                st.session_state.show_fav_form_Negative = False
                st.rerun()
