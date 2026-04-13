def generate_smart_cta(analysis, page):

    # Combine signals
    text_blob = (
        analysis.get("message", "").lower()
        + " "
        + analysis.get("offer", "").lower()
        + " "
        + page.get("headline", "").lower()
        + " "
        + " ".join(page.get("sections", [])).lower()
    )


    # SaaS / Tools / Platforms
    if any(word in text_blob for word in ["platform", "tool", "software", "automate", "ai"]):
        return "Get Started"

    # Templates / builders (like your case)
    if any(word in text_blob for word in ["template", "website", "builder", "design"]):
        return "Explore Templates"

    # B2B / services
    if any(word in text_blob for word in ["business", "solution", "enterprise"]):
        return "Book a Demo"

    # Free offer
    if "free" in text_blob:
        return "Try for Free"

    # Ecommerce / product
    if any(word in text_blob for word in ["buy", "product", "shop", "sale", "discount"]):
        return "Shop Now"

    # Learning / content
    if any(word in text_blob for word in ["learn", "guide", "course"]):
        return "Learn More"

    # fallback
    return "Get Started"


def apply_changes(page, plan, analysis):

    updated = page.copy()

    original_headline = page.get("headline", "")
    new_headline = plan.get("headline", "")

    if new_headline:
        updated["headline"] = f"{original_headline} — {new_headline}"


    updated["cta"] = generate_smart_cta(analysis, page)

    original_sections = page.get("sections", [])
    new_sections = []

    for item in plan.get("sections", []):
        change = item.get("change", "").lower()

        if "value" in change:
            new_sections.append(
                "Solve your key challenges with powerful, easy-to-use solutions tailored to your needs."
            )

        elif "cta" in change:
            new_sections.append(
                "Take the next step today and start seeing real results instantly."
            )

        elif "offer" in change:
            new_sections.append(
                "Unlock exclusive benefits and limited-time advantages designed just for you."
            )

        else:
            new_sections.append(change.capitalize())

    updated["sections"] = original_sections[:2] + new_sections

    return updated