import fitz
import re
import pandas as pd
from pathlib import Path

OUTPUT = Path("data/outputs/total_electors_missing.csv")

# ONLY problematic ACs
TARGET_ACS = [
    38, 41, 42,
    151, 152, 153, 154, 155, 156, 157, 158, 159,
    229, 230, 232, 233, 234
]


def find_pdf(ac):

    matches = []

    for root in [
        Path("data"),
        Path("data/pdfs"),
        Path("data/retry"),
        Path("data/retry_polled")
    ]:

        if root.exists():

            matches.extend(
                root.rglob(f"AC{ac}.pdf")
            )

    if matches:
        return matches[0]

    return None


def extract_electors(pdf_path):

    doc = fitz.open(pdf_path)

    # Electors are on page 1
    text = doc[0].get_text("text")

    text = re.sub(r"\s+", " ", text)

    patterns = [

        r"Total\s+No\.?\s+of\s+Electors\s+in\s+Assembly\s+Constituency\s*:?\s*([\d,]+)",

        r"Total\s+No\.?\s+of\s+Electors.*?:\s*([\d,]+)",

        r"Electors\s+in\s+Assembly\s+Constituency\s*:?\s*([\d,]+)"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).replace(",", "")

            return int(value)

    return None


records = []

print("=" * 70)
print("SCRAPING ONLY PROBLEMATIC ELECTOR VALUES")
print("=" * 70)

for ac in TARGET_ACS:

    print(f"\nAC {ac}")

    pdf = find_pdf(ac)

    if pdf is None:

        print("❌ PDF NOT FOUND")

        records.append({
            "ac_number": ac,
            "total_electors": None,
            "source": None,
            "status": "PDF_NOT_FOUND"
        })

        continue

    print("PDF:", pdf)

    try:

        value = extract_electors(pdf)

        if value:

            print("✅ Total Electors:", value)

            records.append({
                "ac_number": ac,
                "total_electors": value,
                "source": str(pdf),
                "status": "OK"
            })

        else:

            print("❌ Elector value not found")

            records.append({
                "ac_number": ac,
                "total_electors": None,
                "source": str(pdf),
                "status": "NOT_FOUND"
            })

    except Exception as e:

        print("❌ ERROR:", e)

        records.append({
            "ac_number": ac,
            "total_electors": None,
            "source": str(pdf),
            "status": "ERROR"
        })


df = pd.DataFrame(records)

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT,
    index=False
)

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)

print(df.to_string(index=False))

print("\nSaved:", OUTPUT)