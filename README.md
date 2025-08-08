# Donizo Bathroom Pricing Engine

Smart pricing engine for full bathroom renovations.  
Parses messy transcript into structured quote with labor, materials, estimated time, VAT, margin, and confidence scoring — built per Donizo test specification.

## 📂 Project Structure
/bathroom-pricing-engine/
├── pricing_engine.py # Main script: transcript → JSON quote
├── pricing_logic/ # Modular business logic
│ ├── material_db.py # Material pricing
│ ├── labor_calc.py # Labor hours & city multipliers
│ ├── vat_rules.py # VAT logic
│ ├── parser.py # Transcript parsing & confidence flags
│ └── confidence.py # Per-task confidence scoring
├── data/
│ ├── materials.json # Material cost database
│ └── price_templates.csv # Example price templates
├── output/
│ ├── sample_quote.json # Latest generated quote
│ └── history/ # Archive of past quotes
├── tests/
│ └── test_logic.py # Basic parsing & pricing test
├── run.sh # Interactive helper script
├── requirements.txt # Dependencies
└── README.md

## 🚀 How to Run

### Install dependencies
```bash
pip install -r requirements.txt


Run interactively
chmod +x run.sh
./run.sh

Type job description when prompted:
4m² bathroom in Marseille. Remove old tiles, redo plumbing for shower, replace toilet, install vanity, repaint walls, lay ceramic floor tiles. Budget-conscious.

Output:
Table summary printed to terminal

JSON saved to:

output/history/quote_YYYY-MM-DD.json
output/sample_quote.json

Run directly with Python
python3 pricing_engine.py \
  --transcript "5m² bathroom in Paris. Install a new vanity, paint walls, and lay ceramic floor tiles. High-end finish." \
  --format compact \
  --out output/history/quote_test.json
⚙️ Pricing Logic
Materials → data/materials.json
Labor = hours × hourly rate × city multiplier
Margin = 18% + adjustments:
+5% plumbing
+2% demolition
+3% low confidence
+2% Paris
Feedback loop adjustments

VAT:
10% renovation (>2y dwelling)
20% otherwise
Confidence: per-task + global

🧠 Bonus
City-based pricing variation
Feedback memory loop
Low-confidence flags
Compact/full JSON modes
Interactive run.sh

🔮 Future Ideas
Vector memory for pricing history
Live supplier pricing API
Contractor productivity data
Multilingual parsing

🧪 Run Tests
pytest tests/




