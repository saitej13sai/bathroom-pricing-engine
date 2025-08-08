from typing import Dict

# Baseline hourly rates by role (EUR)
HOURLY = {
    "tiler": 45.0,
    "painter": 38.0,
    "plumber": 52.0,
    "general": 35.0,
    "demolition": 32.0
}

CITY_MULTIPLIER = {
    "paris": 1.15,
    "marseille": 0.97,
    "lyon": 1.05,
    "toulouse": 1.00,
    "default": 1.00
}

def city_factor(city: str) -> float:
    if not city:
        return CITY_MULTIPLIER["default"]
    return CITY_MULTIPLIER.get(city.strip().lower(), CITY_MULTIPLIER["default"])

def labor_hours_estimate(task: Dict) -> float:
    """Heuristic hours per task based on small bathroom defaults."""
    t = task["task_type"]
    area = task.get("area_m2") or 4.0
    if t == "demolition_remove_tiles":
        return max(2.0, 0.7 * area)  # ~1.4 m2/hr
    if t == "plumbing_shower_redo":
        return 6.0
    if t == "toilet_replace":
        return 3.0
    if t == "vanity_install":
        return 2.5
    if t == "painting_walls":
        wall_ratio = 2.6
        paint_area = area * wall_ratio
        return max(3.0, 0.4 * paint_area)  # incl. prep + 2 coats
    if t == "floor_tiling_ceramic":
        return max(4.0, 0.9 * area)
    return 2.0

def labor_rate_for_task(task_type: str) -> float:
    if "tiling" in task_type:
        return HOURLY["tiler"]
    if "painting" in task_type:
        return HOURLY["painter"]
    if "plumbing" in task_type or "toilet" in task_type or "vanity" in task_type:
        return HOURLY["plumber"]
    if "demolition" in task_type:
        return HOURLY["demolition"]
    return HOURLY["general"]

def labor_cost(task: Dict, city: str) -> float:
    hrs = labor_hours_estimate(task)
    rate = labor_rate_for_task(task["task_type"]) * city_factor(city)
    return round(hrs * rate, 2)
