def apply_changes(page, plan):
    updated = page.copy()

  
    if "headline" in plan:
        original = page.get("headline", "")
        new = plan["headline"]

        # blend instead of replace
        updated["headline"] = f"{original} — {new}"

 
    if "cta" in plan:
        updated["cta"] = plan["cta"]


    new_sections = []

    for item in plan.get("sections", []):
        if isinstance(item, dict):
            change = item.get("change", "")

            # Convert instruction → actual content
            if "highlight" in change.lower():
                new_sections.append("Discover powerful features designed to solve your business challenges efficiently.")

            elif "add" in change.lower():
                new_sections.append("Explore advanced capabilities that streamline workflows and boost productivity.")

            elif "replace" in change.lower():
                new_sections.append("Experience a smarter, faster way to manage your business operations.")

            else:
                new_sections.append(change)

        else:
            new_sections.append(item)

    # Merge with original instead of overwriting
    updated["sections"] = page.get("sections", [])[:2] + new_sections

    return updated