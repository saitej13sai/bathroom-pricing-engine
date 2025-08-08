from typing import Dict

# FR VAT assumptions (simplified):
# - 10% reduced VAT for home renovation in dwellings older than 2 years
# - 20% standard VAT otherwise
DEFAULT_RENOVATION_VAT = 0.10
STANDARD_VAT = 0.20

def vat_for_task(task, context: Dict) -> float:
    is_reno = context.get("is_renovation", True)
    dwelling_age_gt_2y = context.get("dwelling_age_gt_2y", True)
    if is_reno and dwelling_age_gt_2y:
        return DEFAULT_RENOVATION_VAT
    return STANDARD_VAT
