import json, os, math
from typing import Dict, List
from datetime import datetime, timezone

from pricing_logic import material_db, labor_calc, vat_rules
from pricing_logic import parser as transcript_parser
from pricing_logic.confidence import task_confidence

FEEDBACK_PATH = os.path.join(os.path.dirname(__file__), "data", "feedback_memory.json")

def _read_feedback():
    if os.path.exists(FEEDBACK_PATH):
        with open(FEEDBACK_PATH, "r") as f:
            return json.load(f)
    return {"accepted_margin_shift": 0.0, "rejected_margin_shift": 0.0}

def _write_feedback(data):
    with open(FEEDBACK_PATH, "w") as f:
        json.dump(data, f, indent=2)

def margin_for_task(task_type: str, global_conf: float, city: str) -> float:
    """Return margin multiplier (e.g., 0.18 == 18%)."""
    base = 0.18  # baseline 18%
    # risk-based adjustments
    if "plumbing" in task_type:
        base += 0.05
    if "demolition" in task_type:
        base += 0.02
    # confidence-based
    if global_conf < 0.8:
        base += 0.03
    # city variations could shift margin if logistics are harder
    if city.lower() == "paris":
        base += 0.02
    fb = _read_feedback()
    base += fb.get("accepted_margin_shift", 0.0)
    base -= fb.get("rejected_margin_shift", 0.0)
    return round(max(0.10, min(0.35, base)), 3)

def materials_cost_for_task(task: Dict, area_m2: float) -> Dict[str, float]:
    t = task["task_type"]
    m = {}
    if t == "demolition_remove_tiles":
        m["demolition_bags"] = 2
        return {"subtotal": round(material_db.price_for("demolition_bags", 2), 2), "lines": m}
    if t == "plumbing_shower_redo":
        lines = {"plumbing_kit_shower": 1, "silicone_sealant": 1, "misc_fasteners": 1}
        subtotal = sum(material_db.price_for(k, v) for k, v in lines.items())
        return {"subtotal": round(subtotal, 2), "lines": lines}
    if t == "toilet_replace":
        lines = {"toilet_standard": 1, "silicone_sealant": 1}
        subtotal = sum(material_db.price_for(k, v) for k, v in lines.items())
        return {"subtotal": round(subtotal, 2), "lines": lines}
    if t == "vanity_install":
        lines = {"vanity_standard": 1, "misc_fasteners": 1, "silicone_sealant": 1}
        subtotal = sum(material_db.price_for(k, v) for k, v in lines.items())
        return {"subtotal": round(subtotal, 2), "lines": lines}
    if t == "painting_walls":
        wall_ratio = 2.6
        paint_area = area_m2 * wall_ratio
        lines = {
            "primer": paint_area,
            "wall_paint": paint_area,
        }
        subtotal = sum(material_db.price_for(k, v) for k, v in lines.items())
        return {"subtotal": round(subtotal, 2), "lines": {**{k: round(v, 2) for k, v in lines.items()}}}
    if t == "floor_tiling_ceramic":
        waste = 1.08
        tile_area = area_m2 * waste
        lines = {
            "ceramic_floor_tile": tile_area,
            "thinset_mortar": area_m2,
            "grout": area_m2
        }
        subtotal = sum(material_db.price_for(k, v) for k, v in lines.items())
        return {"subtotal": round(subtotal, 2), "lines": {**{k: round(v, 2) for k, v in lines.items()}}}
    return {"subtotal": 0.0, "lines": {}}

def build_task_quote(task: Dict, ctx: Dict) -> Dict:
    city = ctx.get("city", "")
    area = ctx.get("area_m2", 4.0)
    materials = materials_cost_for_task(task, area)
    labor = labor_calc.labor_cost(task, city)
    vat_rate = vat_rules.vat_for_task(task, ctx)
    conf = task_confidence(task["task_type"], ctx)

    base_cost = materials["subtotal"] + labor
    margin = margin_for_task(task["task_type"], ctx["global_confidence"], city)
    margin_value = round(base_cost * margin, 2)
    pre_vat = round(base_cost + margin_value, 2)
    vat_value = round(pre_vat * vat_rate, 2)
    total = round(pre_vat + vat_value, 2)

    return {
        "task_type": task["task_type"],
        "materials": {"lines": materials["lines"], "subtotal": materials["subtotal"]},
        "labor": {"hours": None, "subtotal": labor},
        "estimated_duration": f"{max(1, round(labor / (labor_calc.labor_rate_for_task(task['task_type']) * labor_calc.city_factor(city)), 1))} h",
        "vat_rate": vat_rate,
        "margin": margin,
        "confidence_score": conf,
        "pricing": {
            "base_cost": base_cost,
            "margin_value": margin_value,
            "pre_vat_total": pre_vat,
            "vat_value": vat_value,
            "total_price": total
        }
    }

def _build_summary(zones: List[Dict], totals: Dict) -> Dict:
    tasks_summary = []
    for z in zones:
        for t in z["tasks"]:
            tasks_summary.append({
                "zone": z["name"],
                "task_type": t["task_type"],
                "materials_subtotal": t["materials"]["subtotal"],
                "labor_subtotal": t["labor"]["subtotal"],
                "pre_vat_total": t["pricing"]["pre_vat_total"],
                "vat_value": t["pricing"]["vat_value"],
                "total_price": t["pricing"]["total_price"],
                "confidence_score": t["confidence_score"],
                "estimated_duration": t["estimated_duration"]
            })
    return {"tasks": tasks_summary, "totals": totals}

def quote_from_transcript(text: str) -> Dict:
    area = transcript_parser.extract_area(text)
    city = transcript_parser.extract_city(text)
    tasks = transcript_parser.parse_tasks(text)
    budget = transcript_parser.is_budget_conscious(text)
    global_conf, flags = transcript_parser.confidence_flags(text, tasks, area)
    ctx = {
        "zone": "bathroom",
        "area_m2": area,
        "city": city or "marseille",
        "budget_conscious": budget,
        "is_renovation": True,
        "dwelling_age_gt_2y": True,
        "global_confidence": global_conf,
        "flags": flags
    }

    grouped_tasks = []
    for t in tasks:
        t["area_m2"] = area
        grouped_tasks.append(build_task_quote(t, ctx))

    totals = {
        "materials": round(sum(t["materials"]["subtotal"] for t in grouped_tasks), 2),
        "labor": round(sum(t["labor"]["subtotal"] for t in grouped_tasks), 2),
        "pre_vat": round(sum(t["pricing"]["pre_vat_total"] for t in grouped_tasks), 2),
        "vat": round(sum(t["pricing"]["vat_value"] for t in grouped_tasks), 2),
        "grand_total": round(sum(t["pricing"]["total_price"] for t in grouped_tasks), 2)
    }

    zones = [{
        "name": "bathroom",
        "area_m2": area,
        "tasks": grouped_tasks
    }]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_transcript": text,
        "context": ctx,
        "system": {"city_multiplier": labor_calc.city_factor(ctx["city"])},
        "summary": _build_summary(zones, totals),
        "zones": zones,
        "totals": totals
    }

def feedback_update(accepted: bool):
    fb = _read_feedback()
    if accepted:
        fb["accepted_margin_shift"] = round(min(0.05, fb.get("accepted_margin_shift", 0.0) + 0.005), 3)
        fb["rejected_margin_shift"] = max(0.0, fb.get("rejected_margin_shift", 0.0) - 0.002)
    else:
        fb["rejected_margin_shift"] = round(min(0.05, fb.get("rejected_margin_shift", 0.0) + 0.005), 3)
        fb["accepted_margin_shift"] = max(0.0, fb.get("accepted_margin_shift", 0.0) - 0.002)
    _write_feedback(fb)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Donizo Bathroom Pricing Engine")
    parser.add_argument("--transcript", type=str, required=True, help="Raw transcript text to price")
    parser.add_argument("--out", type=str, default=os.path.join(os.path.dirname(__file__), "output", "sample_quote.json"))
    parser.add_argument("--format", type=str, choices=["full", "compact"], default="full",
                        help="full: full quote JSON (default). compact: short JSON with only summary & totals.")
    args = parser.parse_args()
    quote = quote_from_transcript(args.transcript)

    if args.format == "compact":
        payload = {
            "generated_at": quote["generated_at"],
            "input_transcript": quote["input_transcript"],
            "context": quote["context"],
            "system": quote["system"],
            "summary": quote["summary"],
            "totals": quote["totals"],
        }
    else:
        payload = quote

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote quote to {args.out}")

    # Always update output/sample_quote.json
    
    sample_path = os.path.join(os.path.dirname(__file__), "output", "sample_quote.json")
    os.makedirs(os.path.dirname(sample_path), exist_ok=True)
    with open(sample_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Also saved latest quote to {sample_path}")

