#!/bin/bash
set -e

# Ask for the job description
echo "Please type the job description and press Enter:"
read JOB

# Today's date
DATE=$(date +%Y-%m-%d)
OUT_DIR="output/history"
OUT_FILE="$OUT_DIR/quote_$DATE.json"

# Ensure folders
mkdir -p "$OUT_DIR"

# Run the pricing engine (compact JSON)
python3 pricing_engine.py --transcript "$JOB" --format compact --out "$OUT_FILE"

# Also copy to a stable path
cp "$OUT_FILE" output/sample_quote.json

# Pretty, human-readable summary
python3 - <<PY "$OUT_FILE"
import json, sys, os
path = sys.argv[1]
with open(path) as f:
    q = json.load(f)

print("")
print("========== Donizo Quote ==========")
print(f"Date: {q['generated_at']}")
print(f"City: {q['context'].get('city','').title()} | Area: {q['context'].get('area_m2','?')} m² | Budget-conscious: {q['context'].get('budget_conscious')}")
print("")

# table header
print("{:<22} {:>10} {:>10} {:>12} {:>10} {:>11}".format(
    "Task", "Materials", "Labor", "Pre-VAT", "VAT", "Total"))
print("-"*80)

for t in q["summary"]["tasks"]:
    print("{:<22} {:>10.2f} {:>10.2f} {:>12.2f} {:>10.2f} {:>11.2f}".format(
        t["task_type"],
        float(t["materials_subtotal"]),
        float(t["labor_subtotal"]),
        float(t["pre_vat_total"]),
        float(t["vat_value"]),
        float(t["total_price"]),
    ))

print("-"*80)
tot = q["summary"]["totals"]
print("{:<22} {:>10.2f} {:>10.2f} {:>12.2f} {:>10.2f} {:>11.2f}".format(
    "TOTALS",
    float(tot["materials"]),
    float(tot["labor"]),
    float(tot["pre_vat"]),
    float(tot["vat"]),
    float(tot["grand_total"]),
))

print("")
print("Notes:")
flags = q["context"].get("flags", [])
if flags:
    print(" - Flags:", ", ".join(flags))
else:
    print(" - No flags.")
print(" - Global confidence:", q["context"].get("global_confidence"))

PY

# Big total price banner
TOTAL=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['totals']['grand_total'])" "$OUT_FILE")
echo ""
echo "======================================="
echo " TOTAL PRICE: €$TOTAL"
echo "======================================="

# Where files went
echo ""
echo "Saved files:"
echo " - $OUT_FILE"
echo " - output/sample_quote.json"
