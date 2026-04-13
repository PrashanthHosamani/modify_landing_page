from agents.planner import plan_changes

analysis = {
    "audience": "students",
    "message": "50% off shoes",
    "tone": "promotional",
    "offer": "50% discount",
    "problems_in_page": [
        "No student focus",
        "Discount not visible"
    ]
}

result = plan_changes(analysis)

print(result)