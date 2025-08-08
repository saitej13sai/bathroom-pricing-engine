# Donizo Bathroom Pricing Engine

Smart pricing engine for full bathroom renovations.  
Parses a messy transcript into a structured quote with labor, materials, estimated time, VAT, margin, and confidence scoring — per Donizo Founding Data Engineer Test Case 1.

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


🚀 How to Run
Install dependencies

pip install -r requirements.txt
Run interactively

chmod +x run.sh
./run.sh
Type the job description when prompted.
Example:

4m² bathroom in Marseille. Remove old tiles, redo plumbing for shower, replace toilet, install vanity, repaint walls, lay ceramic floor tiles. Budget-conscious.
Output

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
Materials: data/materials.json

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

🧠 Bonus Features
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
bash
Copy
Edit
pytest tests/



