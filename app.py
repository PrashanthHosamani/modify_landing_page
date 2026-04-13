import streamlit as st
from agents.analyzer import analyze
from agents.planner import plan_changes
from agents.executor import apply_changes
from utils.scraper import scrape_website

import pytesseract
from PIL import Image
import cv2
import numpy as np
import re


st.set_page_config(page_title="AI Landing Page Optimizer", layout="wide")

st.title("AI Landing Page Optimizer")


def extract_text_from_image(image_file):
    image = Image.open(image_file)
    img = np.array(image)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    texts = []

    # 1. Raw
    texts.append(pytesseract.image_to_string(img_rgb))

    # 2. Grayscale
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    texts.append(pytesseract.image_to_string(gray))

    # 3. Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    texts.append(pytesseract.image_to_string(thresh))

    combined = "\n".join(texts)

    # Clean text
    cleaned = []
    for line in combined.split("\n"):
        line = line.strip()
        if len(line) > 3:
            cleaned.append(line)

    return "\n".join(cleaned)

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
        try:
            extracted_text = extract_text_from_image(uploaded_image)

            st.info("📸 Extracted Text from Image:")
            st.write(extracted_text)

            text_lower = extracted_text.lower()

            # SIGNAL DETECTION
            offer = ""
            percent_match = re.search(r"\d+%", text_lower)
            if percent_match:
                offer = percent_match.group()

            if "sale" in text_lower:
                offer = (offer + " sale").strip()

            if "off" in text_lower:
                offer = (offer + " off").strip()

            cta = ""
            if "shop" in text_lower:
                cta = "Shop Now"
            elif "buy" in text_lower:
                cta = "Buy Now"

            # STRUCTURED INPUT (IMPORTANT)
            structured_context = f"""
AD CONTENT:
{extracted_text}

DETECTED SIGNALS:
Offer: {offer if offer else "Unknown discount"}
CTA: {cta if cta else "Not clear"}
"""

            combined_input += structured_context

        except Exception as e:
            st.warning("⚠️ Image processing failed")


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


    analysis = analyze(combined_input, page)
    plan = plan_changes(analysis)
    updated_page = apply_changes(page, plan)


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