import streamlit as st
from agents.analyzer import analyze
from agents.planner import plan_changes
from agents.executor import apply_changes
from utils.scraper import scrape_website

import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


st.set_page_config(page_title="AI Landing Page Optimizer", layout="wide")

st.title("🚀 AI Landing Page Optimizer")


def analyze_image_with_llm(image_file):
    try:
        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = """
Analyze this advertisement image and extract structured marketing information.

Return JSON ONLY:
{
  "product": "",
  "brand": "",
  "headline": "",
  "cta": "",
  "offer": "",
  "tone": "",
  "audience": ""
}

Focus on:
- visible text
- discount/offer
- product type
- call-to-action
- marketing tone
"""

        data = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return "Image analysis failed"


def render_page(page, title=""):
    if title:
        st.markdown(f"### {title}")

    st.markdown(f"# {page.get('headline', '')}")

    for section in page.get("sections", []):
        st.markdown(f"- {section}")

    st.button(page.get("cta", "Action"))

st.subheader("Input")

ad_input = st.text_area("Paste Ad Content")

uploaded_image = st.file_uploader(
    "Upload Ad Image (optional)", type=["png", "jpg", "jpeg"]
)

url_input = st.text_input("Enter Website URL (optional)")

if st.button("Generate Personalized Page"):

    combined_input = ad_input if ad_input else ""

    if uploaded_image:
        st.info("🧠 Understanding image using AI...")

        image_analysis = analyze_image_with_llm(uploaded_image)

        st.write("📸 Image Analysis:")
        st.write(image_analysis)

        combined_input += f"\nIMAGE ANALYSIS:\n{image_analysis}"


    if url_input:
        scraped = scrape_website(url_input)

        if "error" in scraped:
            st.warning("⚠️ Could not fetch website. Using fallback.")
            page = {
                "headline": "Generic Product Page",
                "cta": "Buy Now",
                "sections": [
                    "High quality product",
                    "Affordable pricing",
                    "Trusted by customers"
                ]
            }
        else:
            page = scraped
    else:
        page = {
            "headline": "Generic Product Page",
            "cta": "Buy Now",
            "sections": [
                "High quality product",
                "Affordable pricing",
                "Trusted by customers"
            ]
        }

    # -----------------------------
    # AGENT FLOW
    # -----------------------------
    analysis = analyze(combined_input, page)
    plan = plan_changes(analysis)
    updated_page = apply_changes(page, plan)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.subheader("📊 Before vs After")

    col1, col2 = st.columns(2)

    with col1:
        render_page(page, "Original Page")

    with col2:
        render_page(updated_page, "Optimized Page")

    st.subheader("🧠 AI Change Plan")
    st.json(plan)

    with st.expander("🔍 Analysis Details"):
        st.json(analysis)

    st.success("✨ Page successfully optimized using AI agent")