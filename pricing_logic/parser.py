import re
from typing import Dict, List, Tuple

# Expanded synonyms to catch more natural phrases
TASK_MAP = {
    # Demolition
    "remove the old tiles": "demolition_remove_tiles",
    "remove old tiles": "demolition_remove_tiles",
    "remove tiles": "demolition_remove_tiles",
    "tile removal": "demolition_remove_tiles",

    # Plumbing / shower
    "redo the plumbing": "plumbing_shower_redo",
    "redo plumbing": "plumbing_shower_redo",
    "shower plumbing": "plumbing_shower_redo",
    "plumbing for the shower": "plumbing_shower_redo",

    # Toilet
    "replace the toilet": "toilet_replace",
    "replace toilet": "toilet_replace",
    "new toilet": "toilet_replace",

    # Vanity
    "install a vanity": "vanity_install",
    "install vanity": "vanity_install",
    "vanity install": "vanity_install",

    # Painting (walls)
    "repaint the walls": "painting_walls",
    "paint the walls": "painting_walls",
    "repaint walls": "painting_walls",
    "paint walls": "painting_walls",
    "repaint wall": "painting_walls",
    "paint wall": "painting_walls",

    # Floor tiling (ceramic)
    "lay new ceramic floor tiles": "floor_tiling_ceramic",
    "ceramic floor tiles": "floor_tiling_ceramic",
    "floor tiling": "floor_tiling_ceramic",
    "tile the floor": "floor_tiling_ceramic",
    "tile floor": "floor_tiling_ceramic"
}

CITY_REGEX = r"(paris|marseille|lyon|toulouse|nice|bordeaux)"
AREA_REGEX = r"(\d+(?:\.\d+)?)\s*m(?:2|²)"
BUDGET_CUES = ["budget-conscious", "tight budget", "cost sensitive", "budget", "cheap", "low cost"]

def extract_area(text: str) -> float:
    m = re.search(AREA_REGEX, text, re.IGNORECASE)
    if not m:
        return 4.0
    try:
        return float(m.group(1))
    except:
        return 4.0

def extract_city(text: str) -> str:
    m = re.search(CITY_REGEX, text, re.IGNORECASE)
    return m.group(1) if m else ""

def is_budget_conscious(text: str) -> bool:
    return any(cue in text.lower() for cue in BUDGET_CUES)

def parse_tasks(text: str) -> List[Dict]:
    tasks = []
    lower = text.lower()
    for phrase, ttype in TASK_MAP.items():
        if phrase in lower:
            tasks.append({"task_type": ttype})
    # De-duplicate
    seen = set()
    dedup = []
    for t in tasks:
        if t["task_type"] not in seen:
            seen.add(t["task_type"])
            dedup.append(t)
    return dedup

def confidence_flags(text: str, tasks: List[Dict], area: float) -> Tuple[float, List[str]]:
    flags = []
    score = 1.0
    if not tasks:
        flags.append("no_tasks_detected")
        score -= 0.4
    if area <= 0 or area > 30:
        flags.append("suspicious_area_value")
        score -= 0.2
    if "shower" in text.lower() and all(t["task_type"] != "plumbing_shower_redo" for t in tasks):
        flags.append("shower_implied_but_no_plumbing_task")
        score -= 0.1
    if "budget" in text.lower():
        score -= 0.05
    return max(0.1, round(score, 2)), flags
