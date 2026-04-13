import streamlit as st
from agents.analyzer import analyze
from agents.planner import plan_changes
from agents.executor import apply_changes
from utils.scraper import scrape_website
from utils.llm import call_llm

import base64

st.set_page_config(page_title="AI Landing Page Optimizer", layout="wide")
st.title("🚀 AI Landing Page Optimizer")

def analyze_image_with_llm(image_file):
    try:
        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        prompt = f"""
Analyze this advertisement image.

Extract:
- product
- offer
- CTA
- tone
- audience

If unclear, make a reasonable guess.

Image (base64 sample):
{base64_image[:1000]}
"""

        response = call_llm(prompt)
        return response

    except Exception as e:
        print("IMAGE ERROR:", e)
        return None


def render_page(page, title="", key_prefix=""):
    if title:
        st.markdown(f"### {title}")

    st.markdown(f"# {page.get('headline', '')}")

    for section in page.get("sections", []):
        st.markdown(f"- {section}")

    st.button(page.get("cta", "Action"), key=f"{key_prefix}_cta")


st.subheader("Input")

ad_input = st.text_area("Paste Ad Content")

uploaded_image = st.file_uploader(
    "Upload Ad Image (optional)", type=["png", "jpg", "jpeg"]
)

url_input = st.text_input("Enter Website URL (optional)")

if st.button("Generate Personalized Page"):

    combined_input = ad_input if ad_input else ""

    if uploaded_image:
        st.info("🧠 Analyzing image...")

        image_analysis = analyze_image_with_llm(uploaded_image)

        if image_analysis:
            st.write("📸 Image Insights:")
            st.write(image_analysis)

            combined_input += f"\nIMAGE ANALYSIS:\n{image_analysis}"
        else:
            st.info("ℹ️ Image parsing is experimental. Using fallback logic.")


    if url_input:
        scraped = scrape_website(url_input)

        if "error" in scraped:
            st.warning("⚠️ Could not fetch website. Using fallback.")
            page = {
                "headline": "Generic Product Page",
                "cta": "Get Started",
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
            "cta": "Get Started",
            "sections": [
                "High quality product",
                "Affordable pricing",
                "Trusted by customers"
            ]
        }

    analysis = analyze(combined_input, page)
    plan = plan_changes(analysis)
    updated_page = apply_changes(page, plan, analysis)


    st.subheader("📊 Before vs After")

    col1, col2 = st.columns(2)

    with col1:
        render_page(page, "Original Page", "original")

    with col2:
        render_page(updated_page, "Optimized Page", "optimized")

    st.subheader("🧠 AI Change Plan")
    st.json(plan)

    with st.expander("🔍 Analysis Details"):
        st.json(analysis)

    st.success("✨ Page successfully optimized using AI agent")