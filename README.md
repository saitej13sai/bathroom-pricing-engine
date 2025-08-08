Donizo Bathroom Pricing Engine
This is a smart pricing engine for full bathroom renovations.
It parses a messy transcript into a structured, professional renovation quote with labor, materials, estimated time, VAT, margin, and confidence scoring — following Donizo's technical test specification.


📂 Project Structure


/bathroom-pricing-engine/
├── pricing_engine.py             # Main script: transcript → JSON quote
├── pricing_logic/                # Modular business logic
│   ├── material_db.py             # Material pricing
│   ├── labor_calc.py              # Labor hours & city multipliers
│   ├── vat_rules.py               # VAT logic
│   ├── parser.py                  # Transcript parsing & confidence flags
│   └── confidence.py              # Per-task confidence scoring
├── data/
│   ├── materials.json             # Material cost database
│   └── price_templates.csv        # Example price templates
├── output/
│   ├── sample_quote.json          # Latest generated quote (for review)
│   └── history/                   # Archive of past quotes
├── tests/
│   └── test_logic.py              # Basic test for parsing & pricing
├── run.sh                         # Interactive helper script
├── requirements.txt               # Dependencies
└── README.md                      # This file

🚀 How to Run
1. Install requirements

pip install -r requirements.txt

2. Easiest: Run interactively

chmod +x run.sh
./run.sh

You will be prompted:

Please type the job description and press Enter:

Example:

4m² bathroom in Marseille. Remove old tiles, redo plumbing for shower, replace toilet, install vanity, repaint walls, lay ceramic floor tiles. Budget-conscious.

Output:
Human-readable table summary printed to terminal
JSON saved in:
output/history/quote_YYYY-MM-DD.json (archived)
output/sample_quote.json (latest quote for review)

3. Run directly with Python
python3 pricing_engine.py \
--transcript "5m² bathroom in Paris. Install a new vanity, paint walls, and lay ceramic floor tiles. High-end finish." \
--format compact \
--out output/history/quote_test.json

📄 Output JSON (compact mode)
Example:
{
  "generated_at": "...",
  "input_transcript": "...",
  "context": { "zone": "bathroom", "area_m2": 4.0, "city": "Marseille", ... },
  "system": { "city_multiplier": 0.97 },
  "summary": {
    "tasks": [
      { "task_type": "demolition_remove_tiles", "materials_subtotal": 40.0, "labor_subtotal": 86.91, "total_price": 167.52 }
    ],
    "totals": { "grand_total": 2345.42 }
  },
  "totals": { "grand_total": 2345.42 }
}

⚙️ How It Works
Materials from materials.json
Labor = hours × hourly rate × city multiplier
Margin = 18% + adjustments (plumbing, demolition, low confidence, Paris) + feedback loop
VAT = 10% (reno >2y) or 20% otherwise
Confidence from task type & context
🧠 Bonus Features
City price variation
Feedback memory loop
Low-confidence flags
Compact/full JSON output modes
Easy run script (run.sh)

🔮 Future Ideas
Vector memory for pricing history
Live supplier price API
Contractor productivity data
Multilingual parsing

🧪 Tests
pytest tests/



