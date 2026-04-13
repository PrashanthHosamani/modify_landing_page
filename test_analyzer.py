from agents.analyzer import analyze

ad = "Get 50% off premium shoes for students"

page = {
    "headline": "Best Shoes",
    "cta": "Buy Now",
    "sections": ["Comfortable", "Affordable"]
}

result = analyze(ad, page)

print(result)