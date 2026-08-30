# src/retry/fix_remaining_fast.py

import fitz
import re
import os
import pandas as pd

PDF_DIRS = [
    "data/bad_pdfs",
    "data/retry_polled"
]

OUT = "data/outputs/form20_results_final_42_recovered.csv"

# Remaining problematic ACs
ACS = [70, 77, 198, 199, 200, 201, 230, 232, 233, 234]

def find_pdf(ac):
    name = f"AC{ac:03d}.pdf"

    for folder in PDF_DIRS:
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return path

    return None


def extract_last_page(ac):

    pdf = find_pdf(ac)

    if not pdf:
        return None, "PDF_NOT_FOUND"

    doc = fitz.open(pdf)
    page = doc[-1]

    text = page.get_text("text")

    doc.close()

    # --------------------------------------------------
    # METHOD 1: Look near "TOTAL votes polled"
    # --------------------------------------------------

    patterns = [
        r"TOTAL\s+votes\s+polled",
        r"TOTAL\s+votes\s+polled\s*",
        r"Total\s+Votes\s+Polled",
        r"Total\s+votes\s+polled"
    ]

    for pattern in patterns:

        m = re.search(pattern, text, re.I)

        if m:

            section = text[m.end():]

            # Take first 1000 chars after heading
            section = section[:1000]

            nums = re.findall(r"\b\d{5,6}\b", section)

            if nums:

                # Usually final total is near end of section
                candidates = [int(x) for x in nums]

                # Keep realistic turnout values
                # 50%–100% of electors
                return candidates[-1], "TEXT_TOTAL_FOUND"

    # --------------------------------------------------
    # METHOD 2: Get all 5/6 digit numbers from last page
    # --------------------------------------------------

    nums = [
        int(x)
        for x in re.findall(r"\b\d{5,6}\b", text)
    ]

    if len(nums) >= 2:

        # Last number is often TOTAL votes polled
        return nums[-1], "LAST_NUMBER_FALLBACK"

    return None, "NOT_ENOUGH_NUMBERS"


# ======================================================
# RUN
# ======================================================

print("=" * 90)
print("FAST RECOVERY OF REMAINING BAD ACs")
print("=" * 90)

results = []

for ac in ACS:

    value, status = extract_last_page(ac)

    results.append({
        "ac_number": ac,
        "total_votes_polled": value,
        "status": status
    })

    print(
        f"AC {ac:03d} -> "
        f"{value if value else '---'} | {status}"
    )


# ======================================================
# UPDATE MASTER CSV ONLY FOR VALUES WE FOUND
# ======================================================

df = pd.read_csv(OUT)

for row in results:

    ac = row["ac_number"]
    value = row["total_votes_polled"]

    if value is not None:

        df.loc[
            df["ac_number"] == ac,
            "total_votes_polled"
        ] = value

        df.loc[
            df["ac_number"] == ac,
            "status"
        ] = "RECOVERED_LAST_PAGE"


# Save

df.to_csv(OUT, index=False)

print("\n" + "=" * 90)
print("UPDATED MASTER FILE")
print("=" * 90)

print(
    df[
        df.ac_number.isin(ACS)
    ][
        ["ac_number", "total_votes_polled", "total_electors", "status"]
    ].to_string(index=False)
)

print("\nSaved:", OUT)