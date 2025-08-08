# Donizo Bathroom Pricing Engine

Smart pricing engine for full bathroom renovations.  
Parses a messy transcript into a structured quote with labor, materials, estimated time, VAT, margin, and confidence scoring as per Donizo Founding Data Engineer Test Case 1.

---

## 📂 Project Structure
```plaintext
/bathroom-pricing-engine/
├── pricing_engine.py
├── pricing_logic/
│   ├── material_db.py
│   ├── labor_calc.py
│   ├── vat_rules.py
│   ├── parser.py
│   └── confidence.py
├── data/
│   ├── materials.json
│   └── price_templates.csv
├── output/
│   ├── sample_quote.json
│   └── history/
├── tests/
│   └── test_logic.py
├── run.sh
├── requirements.txt
└── README.md

## 🚀 1) How to Run

### Install dependencies
```bash
pip install -r requirements.txt

✅Run interactively (recommended)
chmod +x run.sh
./run.sh

✅You will be prompted:
✅Please type the job description and press Enter:
Example input:
✅4m² bathroom in Marseille. Remove old tiles, redo plumbing for shower, replace toilet, install vanity, repaint walls, lay ceramic floor tiles. Budget-conscious.
Outputs:

Human-readable table summary in terminal

✅JSON saved to:
output/history/quote_YYYY-MM-DD.json (archived)
output/sample_quote.json (latest)

✅Run directly with Python

python3 pricing_engine.py \
  --transcript "5m² bathroom in Paris. Install a new vanity, paint walls, and lay ceramic floor tiles. High-end finish." \
  --format compact \
  --out output/history/quote_test.json

📄 2) Output JSON Schema (compact example)

{
  "generated_at": "2025-08-08T06:34:51.576591+00:00",
  "input_transcript": "...",
  "context": {
    "zone": "bathroom",
    "area_m2": 4.0,
    "city": "Marseille",
    "budget_conscious": true,
    "is_renovation": true,
    "dwelling_age_gt_2y": true,
    "global_confidence": 0.95,
    "flags": []
  },
  "system": { "city_multiplier": 0.97 },
  "summary": {
    "tasks": [
      {
        "zone": "bathroom",
        "task_type": "demolition_remove_tiles",
        "materials_subtotal": 40.0,
        "labor_subtotal": 86.91,
        "pre_vat_total": 152.29,
        "vat_value": 15.23,
        "total_price": 167.52,
        "confidence_score": 0.85,
        "estimated_duration": "2.8 h"
      }
    ],
    "totals": {
      "materials": 791.08,
      "labor": 994.91,
      "pre_vat": 2132.19,
      "vat": 213.23,
      "grand_total": 2345.42
    }
  },
  "totals": {
    "materials": 791.08,
    "labor": 994.91,
    "pre_vat": 2132.19,
    "vat": 213.23,
    "grand_total": 2345.42
  }
}
✅Note:
Use --format full to include full zones[].tasks[] breakdown with material lines, margin, VAT, and per-task totals.
⚙️ 3) Pricing & Margin Logic
✅Materials: Unit prices from data/materials.json
Paint area ≈ 2.6 × floor m²
Tile waste ≈ 8%
✅Labor: From pricing_logic/labor_calc.py
Labor cost = estimated hours × hourly rate by trade × city multiplier

✅Margin:
Base 18%
+5% for plumbing tasks
+2% for demolition tasks
+3% if global confidence < 0.8
+2% for Paris
Adjusted by feedback loop
Clamped between 10–35%

✅VAT (France simplified):
10% if renovation & dwelling > 2 years
20% otherwise
✅Confidence:
Per-task: pricing_logic/confidence.py
Global: from parser flags

📌 4) Assumptions & Edge Cases
Defaults to 4.0 m² if area not detected.
Supported city detection: Paris, Marseille, Lyon, Toulouse, Nice, Bordeaux.
✅Flags:
no_tasks_detected — no tasks parsed from transcript
suspicious_area_value — area ≤ 0 or > 30 m²
shower_implied_but_no_plumbing_task — shower mentioned but no plumbing task detected
Budget-conscious inputs slightly reduce confidence score.
Feedback loop stores adjustments in data/feedback_memory.json.

🧠 5) Bonus Features Implemented
✅ City-based pricing variation
✅ Feedback memory loop
✅ Edge-case / low-confidence flags
✅ Compact vs full JSON output modes
✅ Interactive run script for quick testing

🔮 6) Future Improvements
Vectorized pricing memory with pgvector / ChromaDB
Real-time supplier pricing API
Contractor productivity adjustments
Multilingual parsing (EN/FR)

🧪 7) Run Tests
pytest tests/





