from adk.builtins import ToolIO
from tools.report_scraper import find_annual_report_pdf  # your scraper module

def fetch_report(ticker: str) -> ToolIO:
    # Simple hardcoded mapping to IR URLs — later load from config or lookup
    known_sources = {
        "BAE": "https://investors.baesystems.com/financial-reporting",
        "TW": "https://www.taylorwimpey.co.uk/corporate/investors/results-and-reports"
    }

    url = known_sources.get(ticker.upper())
    if not url:
        return ToolIO(output={"error": "Unknown ticker or source not configured"})

    pdf_url = find_annual_report_pdf(url)
    return ToolIO(output={"pdf_url": pdf_url or "Not found"})
