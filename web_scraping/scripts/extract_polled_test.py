import pandas as pd
import requests
import fitz
import os
import re


# =========================================================
# FILES
# =========================================================

RESULTS_FILE = "data/outputs/form20_results.csv"

DOWNLOAD_DIR = "data/retry_polled"


# =========================================================
# READ RESULTS
# =========================================================

df = pd.read_csv(RESULTS_FILE)

polled_df = df[
    df["status"]
    .fillna("")
    .str.strip()
    == "MISSING_POLLED"
].copy()


# =========================================================
# DOWNLOAD FOLDER
# =========================================================

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


# =========================================================
# EXTRACT TOTAL POLLED
# =========================================================

def extract_polled(pdf_path):

    doc = fitz.open(pdf_path)

    # Last page
    last_page = doc[-1]

    text = last_page.get_text()

    # -----------------------------------------------------
    # Find final summary row
    # -----------------------------------------------------

    # The final summary row contains:
    #
    # Polling Station Votes
    # Postal Ballot Votes
    # TOTAL votes polled
    #
    # In extracted text, the last numeric block before
    # "Place :" contains the final summary values.

    place_match = re.search(
        r"\bPlace\s*:",
        text,
        re.IGNORECASE
    )

    if not place_match:
        return None

    before_place = text[
        :place_match.start()
    ]

    # -----------------------------------------------------
    # Get numeric values near the end
    # -----------------------------------------------------

    numbers = re.findall(
        r"\b\d+\b",
        before_place
    )

    if len(numbers) < 5:
        return None

    # Last 5 numbers are the final summary values
    final_numbers = numbers[-5:]

    print("\nFinal numeric block:")
    print(final_numbers)

    # Structure:
    #
    # polling station votes
    # postal ballot votes
    # total valid votes / related value
    # TOTAL votes polled
    # rejected votes
    #
    # TOTAL votes polled = 4th value

    total_polled = int(
        final_numbers[-2]
    )

    return total_polled


# =========================================================
# TEST ACs
# =========================================================

test_acs = [38, 39, 41]


for ac in test_acs:

    row = polled_df[
        polled_df["ac_number"] == ac
    ]

    if row.empty:

        print(
            f"\nAC {ac} not found."
        )

        continue

    url = row.iloc[0]["pdf_url"]

    pdf_path = os.path.join(
        DOWNLOAD_DIR,
        f"AC{ac:03d}.pdf"
    )

    print("\n" + "=" * 70)
    print(f"AC {ac}")
    print("=" * 70)

    # -----------------------------------------------------
    # Download
    # -----------------------------------------------------

    if not os.path.exists(pdf_path):

        print("Downloading...")

        response = requests.get(
            url,
            timeout=60
        )

        response.raise_for_status()

        with open(pdf_path, "wb") as f:
            f.write(response.content)

    else:

        print("PDF already downloaded.")

    # -----------------------------------------------------
    # Extract
    # -----------------------------------------------------

    polled = extract_polled(
        pdf_path
    )

    print(
        f"AC {ac} → Total Voted/Polled = {polled}"
    )


print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)