import json
import os
from typing import Dict, Any, List

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "materials.json")

def load_materials() -> Dict[str, Any]:
    with open(DATA_PATH, "r") as f:
        return json.load(f)

_MATERIALS = load_materials()

def price_for(item_key: str, qty: float) -> float:
    item = _MATERIALS.get(item_key)
    if not item:
        return 0.0
    return round(item["base_price"] * qty, 2)

def get_item(item_key: str) -> Dict[str, Any]:
    return _MATERIALS.get(item_key, {})

def list_all() -> List[str]:
    return list(_MATERIALS.keys())
