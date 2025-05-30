import streamlit as st
import json
from pathlib import Path
from PIL import Image
import base64

st.set_page_config(page_title="Sorties Multi-Plateformes", layout="wide")
st.title("🎬🎮 Dernières sorties par plateforme")

def load_data(platform_name):
    data_path = Path("assets/dataset/platforms") / f"{platform_name}.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def display_item(item, platform):
    image_path = Path("assets/img") / platform / item["image"]
    if not image_path.exists():
        st.warning(f"Image introuvable : {image_path}")
        return

    image_b64 = image_to_base64(image_path)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <a href="{item['url']}" target="_blank">
                <img src="data:image/jpeg;base64,{image_b64}" 
                     style="width:390px;height:570px;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.2);" />
            </a>
            <div style="margin-top:0.5em;font-weight:bold;">{item['title']}</div>
            <div style="color:gray;font-size:0.85em;">{item.get("type", "")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

platforms = ["Netflix", "Amazon Prime", "Steam"]

for platform in platforms:
    st.markdown(f"## {platform}")
    data = load_data(platform)

    for i in range(0, len(data), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(data):
                with cols[j]:
                    display_item(data[i + j], platform)
