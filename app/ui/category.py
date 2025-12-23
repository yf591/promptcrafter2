"""
カテゴリ選択UIモジュール
"""

import streamlit as st


def add_keyword_to_input(keyword, display_name=None):
    """キーワード入力欄にキーワードを追加"""
    st.session_state.keyword_to_add = keyword
    # 次の再描画時に表示する情報を保存
    if display_name:
        st.session_state.keyword_added_info = f"✅ '{display_name}' ({keyword})"
    else:
        st.session_state.keyword_added_info = f"✅ '{keyword}'"


def render_category_selection():
    """カテゴリ選択エリアのレンダリング"""
    st.markdown("### 📁 カテゴリからキーワード選択")

    # キーワード追加フィードバック（スクロール不要で見える位置に表示）
    if st.session_state.get("keyword_added_info"):
        st.success(
            f"🎉 {st.session_state.keyword_added_info} をキーワードに追加しました！"
        )
        st.session_state.keyword_added_info = None

    categories = st.session_state.categories
    category_names = list(categories.keys())

    # カテゴリを2つのグループに分ける
    # 1段目: NSFW, Prompts, Style, Favorites以外
    # 2段目: NSFW, Prompts, Style, Favorites
    group2_categories = ["NSFW", "Prompts", "Style", "Favorites"]
    group1_names = [name for name in category_names if name not in group2_categories]
    group2_names = [name for name in category_names if name in group2_categories]

    # 1段目のタブ
    if group1_names:
        st.markdown("#### メインカテゴリ")

        # 現在のキーワードを表示
        current_keywords = st.session_state.get("keywords_input", "")
        if current_keywords:
            st.info(f"📝 現在のキーワード: {current_keywords}")
        else:
            st.info("📝 現在のキーワード: (未入力)")

        tabs1 = st.tabs(group1_names)

        for idx, (category_name, tab) in enumerate(zip(group1_names, tabs1)):
            with tab:
                subcategories = categories[category_name]

                if not subcategories:
                    st.info(f"{category_name}カテゴリにはまだアイテムがありません。")
                    continue

                # サブカテゴリをエクスパンダーで表示
                for subcategory_name, items in subcategories.items():
                    with st.expander(f"📂 {subcategory_name}"):
                        if items:
                            # アイテムをボタンで表示（3列レイアウト）
                            cols = st.columns(3)
                            for i, (item_jp, item_en) in enumerate(items.items()):
                                col_idx = i % 3
                                with cols[col_idx]:
                                    if st.button(
                                        f"➕ {item_jp}",
                                        key=f"{category_name}_{subcategory_name}_{item_jp}_{idx}_g1",
                                        use_container_width=True,
                                    ):
                                        # キーワードを追加
                                        add_keyword_to_input(item_en, item_jp)
                                        st.rerun()
                        else:
                            st.info("このサブカテゴリにはアイテムがありません。")

    # 2段目のタブ
    if group2_names:
        st.markdown("#### 特殊カテゴリ")

        # 現在のキーワードを表示
        current_keywords = st.session_state.get("keywords_input", "")
        if current_keywords:
            st.info(f"📝 現在のキーワード: {current_keywords}")
        else:
            st.info("📝 現在のキーワード: (未入力)")

        tabs2 = st.tabs(group2_names)

        for idx, (category_name, tab) in enumerate(zip(group2_names, tabs2)):
            with tab:
                subcategories = categories[category_name]

                if not subcategories:
                    st.info(f"{category_name}カテゴリにはまだアイテムがありません。")
                    continue

                # サブカテゴリをエクスパンダーで表示
                for subcategory_name, items in subcategories.items():
                    # FavoritesカテゴリではKeywordsだけを表示
                    if category_name == "Favorites" and subcategory_name != "Keywords":
                        continue

                    with st.expander(f"📂 {subcategory_name}"):
                        if items:
                            # Keywordsサブカテゴリの場合は特別な表示
                            if (
                                category_name == "Favorites"
                                and subcategory_name == "Keywords"
                            ):
                                # キーワードの場合は値をそのまま表示
                                cols = st.columns(3)
                                for i, (item_jp, keywords) in enumerate(items.items()):
                                    col_idx = i % 3
                                    with cols[col_idx]:
                                        if st.button(
                                            f"➕ {item_jp}",
                                            key=f"{category_name}_{subcategory_name}_{item_jp}_{idx}_g2",
                                            use_container_width=True,
                                        ):
                                            # キーワードをそのまま追加
                                            add_keyword_to_input(keywords, item_jp)
                                            st.rerun()
                            else:
                                # 通常のアイテムをボタンで表示（3列レイアウト）
                                cols = st.columns(3)
                                for i, (item_jp, item_en) in enumerate(items.items()):
                                    col_idx = i % 3
                                    with cols[col_idx]:
                                        if st.button(
                                            f"➕ {item_jp}",
                                            key=f"{category_name}_{subcategory_name}_{item_jp}_{idx}_g2",
                                            use_container_width=True,
                                        ):
                                            # キーワードを追加
                                            add_keyword_to_input(item_en, item_jp)
                                            st.rerun()
                        else:
                            st.info("このサブカテゴリにはアイテムがありません。")
