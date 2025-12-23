"""
履歴表示UIモジュール
"""

import streamlit as st
import pyperclip
from datetime import datetime
from app.history_manager import clear_history, delete_history_item, load_history


def render_history():
    """履歴表示画面のレンダリング"""
    st.markdown("### 📜 プロンプト生成履歴")

    history = st.session_state.prompt_history

    if not history:
        st.info("履歴がまだありません。プロンプトを生成すると自動的に記録されます。")
        return

    # 履歴のクリアボタン
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ 履歴を全削除", use_container_width=True):
            if clear_history():
                st.session_state.prompt_history = []
                st.success("✅ 履歴を削除しました！")
                st.rerun()

    st.markdown(f"**履歴件数: {len(history)}件**")
    st.markdown("---")

    # 履歴を表示
    for i, entry in enumerate(history):
        timestamp = datetime.fromisoformat(entry["timestamp"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with st.expander(f"🕒 {timestamp} | キーワード: {entry['keywords'][:50]}..."):
            # 詳細情報
            st.markdown(f"**LoRA:** {entry.get('lora', 'None')}")
            st.markdown(f"**キーワード:**")
            st.text(entry["keywords"])

            st.markdown("**Positive Prompt:**")
            st.text_area(
                "Positive",
                value=entry["positive_prompt"],
                height=100,
                key=f"hist_pos_{i}",
                disabled=True,
            )

            st.markdown("**Negative Prompt:**")
            st.text_area(
                "Negative",
                value=entry["negative_prompt"],
                height=100,
                key=f"hist_neg_{i}",
                disabled=True,
            )

            # アクションボタン
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("📝 再利用", key=f"reuse_{i}", use_container_width=True):
                    st.session_state.keywords = entry["keywords"]
                    st.session_state.positive_prompt = entry["positive_prompt"]
                    st.session_state.negative_prompt = entry["negative_prompt"]
                    if entry.get("lora") and entry.get("lora") != "None":
                        st.session_state.selected_lora = entry["lora"]
                    st.success("✅ 履歴から復元しました！")
                    st.rerun()

            with col2:
                if st.button(
                    "📋 コピー (Pos)",
                    key=f"copy_hist_pos_{i}",
                    use_container_width=True,
                ):
                    pyperclip.copy(entry["positive_prompt"])
                    st.success("✅ Positiveをコピーしました！")

            with col3:
                if st.button(
                    "📋 コピー (Neg)",
                    key=f"copy_hist_neg_{i}",
                    use_container_width=True,
                ):
                    pyperclip.copy(entry["negative_prompt"])
                    st.success("✅ Negativeをコピーしました！")

            with col4:
                if st.button("🗑️ 削除", key=f"del_hist_{i}", use_container_width=True):
                    if delete_history_item(i):
                        st.session_state.prompt_history = load_history()
                        st.success("✅ 履歴を削除しました！")
                        st.rerun()
