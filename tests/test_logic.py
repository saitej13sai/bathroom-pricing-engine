from pricing_engine import quote_from_transcript

def test_basic_quote():
    text = ("Client wants to renovate a small 4m² bathroom. They’ll remove the old tiles, "
            "redo the plumbing for the shower, replace the toilet, install a vanity, "
            "repaint the walls, and lay new ceramic floor tiles. Budget-conscious. Located in Marseille.")
    q = quote_from_transcript(text)
    assert q["context"]["city"].lower() == "marseille"
    assert len(q["zones"][0]["tasks"]) >= 5
    assert q["totals"]["grand_total"] > 0
