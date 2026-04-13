from playwright.sync_api import sync_playwright

def scrape_website(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
                )
            page = browser.new_page()
            page.goto(url, timeout=60000)

            # wait for content to load
            page.wait_for_timeout(3000)

            content = page.content()

            # HEADLINE
            h1 = page.query_selector("h1")
            headline = h1.inner_text().strip() if h1 else "No headline found"

            # CTA (buttons)
            buttons = page.query_selector_all("button, a")
            cta = "Get Started"

            for btn in buttons:
                text = btn.inner_text().lower()
                if any(word in text for word in ["sign", "start", "get", "try", "join", "book"]):
                    cta = text.strip()
                    break

            sections = []

            paragraphs = page.query_selector_all("p")
            for p_tag in paragraphs:
                text = p_tag.inner_text().strip()

                if len(text) > 50 and len(sections) < 5:
                    sections.append(text)

            # fallback
            if not sections:
                sections = [
                    "High quality product",
                    "Affordable pricing",
                    "Trusted by customers"
                ]

            browser.close()

            return {
                "headline": headline,
                "cta": cta,
                "sections": sections
            }

    except Exception as e:
        return {"error": str(e)}