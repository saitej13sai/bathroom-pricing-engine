from typing import Dict

def task_confidence(task_type: str, context: Dict) -> float:
    # Simple heuristic per task type
    base = {
        "demolition_remove_tiles": 0.9,
        "plumbing_shower_redo": 0.7,
        "toilet_replace": 0.85,
        "vanity_install": 0.85,
        "painting_walls": 0.8,
        "floor_tiling_ceramic": 0.8
    }.get(task_type, 0.7)

    # Budget constraints add uncertainty about quality choices
    if context.get("budget_conscious"):
        base -= 0.05

    # Clamp
    return min(1.0, max(0.1, round(base, 2)))
