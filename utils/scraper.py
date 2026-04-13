import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scrape_website(url):
    try:
        response = requests.get(url, timeout=5, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        # HEADLINE
        headline = ""
        for tag in ["h1", "h2"]:
            h = soup.find(tag)
            if h:
                headline = h.get_text(strip=True)
                break

        # CTA (better detection)
        cta = ""
        buttons = soup.find_all(["button", "a"])

        for b in buttons:
            text = b.get_text(strip=True)
            if any(word in text.lower() for word in ["buy", "shop", "start", "learn", "try"]):
                cta = text
                break

        # SECTIONS (clean extraction)
        sections = []
        paragraphs = soup.find_all("p")

        for p in paragraphs[:5]:
            text = p.get_text(strip=True)
            if len(text) > 30:
                sections.append(text)

        return {
            "headline": headline or "No headline found",
            "cta": cta or "Learn More",
            "sections": sections if sections else ["No content found"]
        }

    except Exception as e:
        return {"error": str(e)}