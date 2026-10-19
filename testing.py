"""
print_secret_message.py

Takes the URL of a published Google Doc containing a table of
(x-coordinate, Character, y-coordinate) rows and prints the grid
of characters forming a readable graphic secret message.
"""

import re
import sys
import requests
from bs4 import BeautifulSoup

# Ensure UTF-8 stdout encoding for Windows terminals to prevent UnicodeEncodeError
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def print_secret_message(doc_url: str, clean_background: bool = True) -> None:
    """
    Parses a published Google Doc table of coordinates and prints the secret message grid.

    :param doc_url: Published Google Doc URL.
    :param clean_background: If True, replaces background fill characters (like '░')
                             with spaces so the graphic is easily readable by humans.
    """
    # Ensure hitting the published version of the document
    if "/pub" not in doc_url:
        doc_url = doc_url.rstrip("/") + "/pub"

    resp = requests.get(doc_url, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("No table found in the document — unexpected format.")

    rows = table.find_all("tr")

    # Parse rows: expected structure is [x-coordinate, Character, y-coordinate]
    points = []
    for row in rows[1:]:
        cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
        if len(cells) < 3:
            continue
        x_str, char, y_str = cells[0], cells[1], cells[2]
        if not re.match(r"^-?\d+$", x_str) or not re.match(r"^-?\d+$", y_str):
            continue
        x, y = int(x_str), int(y_str)
        points.append((x, y, char))

    if not points:
        raise ValueError("No valid character rows were parsed from the table.")

    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)

    # Initialize grid filled with spaces
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y, char in points:
        # Replace background fill character ('░') with space for clean human-readable output
        if clean_background and char == "░":
            grid[y][x] = " "
        else:
            grid[y][x] = char

    # Print grid line by line
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
    print_secret_message(url)
