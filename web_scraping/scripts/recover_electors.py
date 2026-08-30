import re
import requests
import fitz
import os
import pandas as pd


# =========================================================
# FILES
# =========================================================

ECI_URL = (
    "https://www.eci.gov.in/eci-backend/public/all_files/"
    "election_report/General_Election_to_the_Legislative_"
    "Assembly_of_Tamil_Nadu_2026_2026/"
    "10-Detailed_Results_1778165153.pdf"
)

PDF_PATH = "data/eci_detailed_results_2026.pdf"


# =========================================================
# DOWNLOAD ECI REPORT
# =========================================================

def download_eci_report():

    if os.path.exists(PDF_PATH):
        print("ECI report already downloaded.")
        return

    print("Downloading official ECI Detailed Results...")

    response = requests.get(
        ECI_URL,
        timeout=120
    )

    response.raise_for_status()

    os.makedirs(
        os.path.dirname(PDF_PATH),
        exist_ok=True
    )

    with open(PDF_PATH, "wb") as f:
        f.write(response.content)

    print("Saved:", PDF_PATH)


# =========================================================
# EXTRACT TOTAL ELECTORS
# =========================================================

def extract_electors():

    print("\nReading ECI report...")

    doc = fitz.open(PDF_PATH)

    full_text = ""

    for page in doc:
        full_text += page.get_text() + "\n"

    # Normalize spaces and newlines
    text = re.sub(r"\s+", " ", full_text)

    pattern = re.compile(
        r"Constituency\s+(\d+)\s*-\s*"
        r"(.*?)"
        r"\(\s*TOTAL\s+ELECTORS\s*-\s*"
        r"([\d,]+)\s*\)",
        re.IGNORECASE
    )

    records = []

    for match in pattern.finditer(text):

        ac_number = int(match.group(1))

        constituency = match.group(2).strip()

        total_electors = int(
            match.group(3).replace(",", "")
        )

        records.append({
            "ac_number": ac_number,
            "eci_constituency": constituency,
            "total_electors": total_electors
        })

    return pd.DataFrame(records)


# =========================================================
# MAIN
# =========================================================

def main():

    download_eci_report()

    elector_df = extract_electors()

    print("\n" + "=" * 60)
    print("ECI ELECTOR EXTRACTION")
    print("=" * 60)

    print(
        "Total ACs found:",
        len(elector_df)
    )

    print("\nFirst 10:")

    print(
        elector_df.head(10).to_string(index=False)
    )

    print("\nAC 27:")

    print(
        elector_df[
            elector_df["ac_number"] == 27
        ].to_string(index=False)
    )

    # =====================================================
    # VALIDATION
    # =====================================================

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    print(
        "Total ACs:",
        len(elector_df)
    )

    print(
        "Unique ACs:",
        elector_df["ac_number"].nunique()
    )

    print(
        "Duplicate ACs:",
        elector_df["ac_number"].duplicated().sum()
    )

    # Expected AC numbers are 1 to 234
    expected_acs = set(range(1, 235))

    actual_acs = set(
        elector_df["ac_number"]
    )

    missing_acs = sorted(
        expected_acs - actual_acs
    )

    extra_acs = sorted(
        actual_acs - expected_acs
    )

    print(
        "Missing ACs:",
        missing_acs
    )

    print(
        "Extra ACs:",
        extra_acs
    )

    # =====================================================
    # SAVE ECI ELECTOR MASTER
    # =====================================================

    eci_output = "data/eci_electors_2026.csv"

    elector_df.to_csv(
        eci_output,
        index=False
    )

    print(
        "\nECI elector master saved to:",
        eci_output
    )

    # =====================================================
    # ELECTOR VALUE CHECK
    # =====================================================

    print("\nElector statistics:")

    print(
        elector_df["total_electors"].describe()
    )


if __name__ == "__main__":
    main()