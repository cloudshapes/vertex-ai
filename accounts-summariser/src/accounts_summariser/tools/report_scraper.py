import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def fetch_page_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def is_probably_annual_report(text, year):
    if not text: return False
    text = text.lower()
    return (
        year in text
        and ("annual" in text or "report and accounts" in text or "annual results" in text)
    )

def find_annual_report_pdf(ir_url: str, year: str = "2023") -> str:
    visited = set()
    
    def scan_links(url):
        if url in visited:
            return []
        visited.add(url)

        soup = fetch_page_soup(url)
        if not soup:
            return []

        links = soup.find_all("a", href=True)
        results = []

        for link in links:
            href = link["href"]
            label = link.get_text(" ", strip=True)

            full_url = urljoin(url, href)
            if href.lower().endswith(".pdf") and is_probably_annual_report(label, year):
                results.append(full_url)

            # Also follow if link label looks promising (even if not a PDF)
            elif is_probably_annual_report(label, year) and not href.startswith("#"):
                # Try following it (one level deep only)
                nested_soup = fetch_page_soup(full_url)
                if nested_soup:
                    nested_links = nested_soup.find_all("a", href=True)
                    for nlink in nested_links:
                        nhref = nlink["href"]
                        nlabel = nlink.get_text(" ", strip=True)
                        if nhref.lower().endswith(".pdf") and is_probably_annual_report(nlabel, year):
                            results.append(urljoin(full_url, nhref))

        return results

    found = scan_links(ir_url)
    return found[0] if found else None
