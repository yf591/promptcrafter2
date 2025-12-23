"""
PromptCrafter2 - Streamlit版
Stable Diffusion用プロンプト生成ツール
"""

import streamlit as st
from app.ui import (
    initialize_session_state,
    render_sidebar,
    render_category_selection,
    render_search,
    render_main_content,
    render_favorites_manager,
    render_history,
)

# ページ設定
st.set_page_config(
    page_title="PromptCrafter2",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# カスタムCSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2196F3;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .prompt-box {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #ddd;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# メイン関数
def main():
    """メインアプリケーション"""
    # セッション状態の初期化
    initialize_session_state()

    # サイドバーをレンダリング
    render_sidebar()

    # メインエリアにタブを作成
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📝 プロンプト生成",
            "🔍 検索",
            "📁 カテゴリ選択",
            "⭐ お気に入り管理",
            "📜 履歴",
        ]
    )

    with tab1:
        render_main_content()

    with tab2:
        render_search()

    with tab3:
        render_category_selection()

    with tab4:
        render_favorites_manager()

    with tab5:
        render_history()

    # フッター
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "PromptCrafter v2.0 (Streamlit版) | 開発者: yf591 | "
        "ライセンス: CC BY-NC-SA 4.0"
        "</div>",
        unsafe_allow_html=True,
    )


# アプリケーションの実行
if __name__ == "__main__":
    main()
