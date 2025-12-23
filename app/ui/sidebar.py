"""
サイドバーUIモジュール
"""

import streamlit as st
from app.config import APP_SETTINGS, save_settings


def render_sidebar():
    """サイドバーのレンダリング"""
    with st.sidebar:
        st.markdown("## ⚙️ 設定")

        # LoRA選択
        loras = ["None"] + APP_SETTINGS.get("loras", [])
        st.session_state.selected_lora = st.selectbox(
            "LoRAモデル選択",
            loras,
            index=(
                loras.index(st.session_state.selected_lora)
                if st.session_state.selected_lora in loras
                else 0
            ),
        )

        st.markdown("---")

        # テンプレート選択
        st.markdown("### テンプレート設定")

        positive_template_keys = [
            key
            for key in APP_SETTINGS.keys()
            if "positive_prompt_template" in key and key != "positive_prompt_template"
        ]
        current_positive = APP_SETTINGS.get(
            "selected_positive_template", "realistic_positive_prompt_template"
        )

        selected_positive_template = st.selectbox(
            "Positiveテンプレート",
            positive_template_keys,
            index=(
                positive_template_keys.index(current_positive)
                if current_positive in positive_template_keys
                else 0
            ),
            key="positive_template_select",
        )

        negative_template_keys = [
            key
            for key in APP_SETTINGS.keys()
            if "negative_prompt_template" in key and key != "negative_prompt_template"
        ]
        current_negative = APP_SETTINGS.get(
            "selected_negative_template", "realistic_negative_prompt_template"
        )

        selected_negative_template = st.selectbox(
            "Negativeテンプレート",
            negative_template_keys,
            index=(
                negative_template_keys.index(current_negative)
                if current_negative in negative_template_keys
                else 0
            ),
            key="negative_template_select",
        )

        # テンプレートの更新
        if selected_positive_template != APP_SETTINGS.get("selected_positive_template"):
            APP_SETTINGS["selected_positive_template"] = selected_positive_template
            save_settings()

        if selected_negative_template != APP_SETTINGS.get("selected_negative_template"):
            APP_SETTINGS["selected_negative_template"] = selected_negative_template
            save_settings()

        st.markdown("---")

        # AI生成設定
        st.markdown("### AI生成設定")

        use_model = st.checkbox(
            "AIモデルを使用",
            value=APP_SETTINGS.get("use_model_for_generation", False),
            key="use_model_checkbox",
        )

        if use_model != APP_SETTINGS.get("use_model_for_generation"):
            APP_SETTINGS["use_model_for_generation"] = use_model
            save_settings()

        if use_model:
            model_name = st.text_input(
                "モデル名",
                value=APP_SETTINGS.get(
                    "model_name", "Gustavosta/MagicPrompt-Stable-Diffusion"
                ),
                key="model_name_input",
            )

            if model_name != APP_SETTINGS.get("model_name"):
                APP_SETTINGS["model_name"] = model_name
                save_settings()

            ai_mode = st.radio(
                "AI生成モード",
                ["both", "positive_only", "negative_only"],
                index=["both", "positive_only", "negative_only"].index(
                    APP_SETTINGS.get("ai_generation_mode", "both")
                ),
                key="ai_mode_radio",
            )

            if ai_mode != APP_SETTINGS.get("ai_generation_mode"):
                APP_SETTINGS["ai_generation_mode"] = ai_mode
                save_settings()
