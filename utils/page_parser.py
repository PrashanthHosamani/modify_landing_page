import requests
from bs4 import BeautifulSoup

def extract_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title"

        headings = [h.get_text() for h in soup.find_all(["h1", "h2"])[:3]]

        return {
            "headline": title,
            "cta": "Learn More",
            "sections": headings if headings else ["Default Section"]
        }

    except:
        return {
            "headline": "Sample Product",
            "cta": "Buy Now",
            "sections": ["Feature 1", "Feature 2"]
        }