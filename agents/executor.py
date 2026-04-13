def generate_smart_cta(analysis, page):
    text_blob = (
        analysis.get("message", "").lower()
        + " "
        + analysis.get("offer", "").lower()
        + " "
        + page.get("headline", "").lower()
        + " "
        + " ".join(page.get("sections", [])).lower()
    )

    # Priority-based intent
    if "free" in text_blob:
        return "Try for Free"

    if any(w in text_blob for w in ["enterprise", "b2b", "business"]):
        return "Book a Demo"

    if any(w in text_blob for w in ["platform", "software", "tool", "ai"]):
        return "Get Started"

    if any(w in text_blob for w in ["template", "builder", "design"]):
        return "Explore Templates"

    if any(w in text_blob for w in ["buy", "shop", "sale", "product"]):
        return "Shop Now"

    return "Get Started"


def apply_changes(page, plan, analysis):
    updated = page.copy()

    original_headline = page.get("headline", "")
    original_cta = page.get("cta", "").lower()

    # CLEAN sections
    original_sections = [
        s for s in page.get("sections", [])
        if s and "no content" not in s.lower()
    ]

    # ---------------- HEADLINE (FIXED LOGIC) ----------------
    new_headline = plan.get("headline", "").strip()

    is_b2b = any(
        word in original_headline.lower()
        for word in ["business", "platform", "ads", "software"]
    )

    if new_headline:
        # 🚨 CRITICAL FIX: reject bad headlines
        if is_b2b and any(x in new_headline.lower() for x in ["offer", "sale", "limited"]):
            updated["headline"] = original_headline
        else:
            updated["headline"] = new_headline
    else:
        updated["headline"] = original_headline

    # ---------------- CTA (FIXED LOGIC) ----------------
    generated_cta = generate_smart_cta(analysis, page)

    # 🚨 CRITICAL FIX: reject generic CTA from plan
    bad_ctas = ["shop now", "buy now", "click here"]

    if any(x in original_cta for x in ["sign up", "login", "join"]):
        updated["cta"] = original_cta.title()

    elif plan.get("cta", "").lower() in bad_ctas and is_b2b:
        updated["cta"] = generated_cta

    else:
        updated["cta"] = generated_cta

    # ---------------- SECTIONS ----------------
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
            # 🚨 ignore promotional junk for B2B
            if not is_b2b:
                new_sections.append(
                    "Unlock exclusive benefits and limited-time advantages designed just for you."
                )

        else:
            new_sections.append(
                "Enhance clarity and highlight key benefits to improve user engagement."
            )

    updated["sections"] = (original_sections[:2] + new_sections)[:5]

    return updated