import pandas as pd


# =========================================================
# FILES
# =========================================================

ORIGINAL_FILE = "data/outputs/form20_results.csv"

REPAIRED_FILE = "data/outputs/form20_results_repaired.csv"


# =========================================================
# READ FILES
# =========================================================

print("Reading original file...")
original = pd.read_csv(ORIGINAL_FILE)

print("Reading repaired file...")
repaired = pd.read_csv(REPAIRED_FILE)


# =========================================================
# BASIC CHECK
# =========================================================

print("\n" + "=" * 60)
print("BASIC CHECK")
print("=" * 60)

print("Original rows:", len(original))
print("Repaired rows:", len(repaired))

print(
    "Same row count:",
    len(original) == len(repaired)
)


# =========================================================
# CHECK MISSING ELECTORS
# =========================================================

print("\n" + "=" * 60)
print("MISSING ELECTORS CHECK")
print("=" * 60)

original_missing = (
    original["status"]
    .fillna("")
    .str.strip()
    == "MISSING_ELECTORS"
).sum()

repaired_missing = (
    repaired["status"]
    .fillna("")
    .str.strip()
    == "MISSING_ELECTORS"
).sum()

print(
    "Original MISSING_ELECTORS:",
    original_missing
)

print(
    "Repaired MISSING_ELECTORS:",
    repaired_missing
)


# =========================================================
# CHECK ELECTOR VALUES
# =========================================================

print("\n" + "=" * 60)
print("ELECTOR VALUE CHECK")
print("=" * 60)

filled_electors = (
    repaired.loc[
        original["status"]
        .fillna("")
        .str.strip()
        == "MISSING_ELECTORS",
        "total_electors"
    ]
    .notna()
    .sum()
)

print(
    "Previously missing elector values now filled:",
    filled_electors
)


# =========================================================
# CHECK OTHER PROBLEM STATUSES
# =========================================================

print("\n" + "=" * 60)
print("OTHER STATUS CHECK")
print("=" * 60)

print("\nOriginal:")
print(
    original["status"].value_counts(dropna=False)
)

print("\nRepaired:")
print(
    repaired["status"].value_counts(dropna=False)
)


# =========================================================
# CHECK IMPORTANT SAMPLE
# =========================================================

print("\n" + "=" * 60)
print("SAMPLE CHECK")
print("=" * 60)

print(
    repaired[
        repaired["ac_number"].isin([27, 30, 31])
    ][
        [
            "ac_number",
            "total_electors",
            "status"
        ]
    ].to_string(index=False)
)


# =========================================================
# FINAL MESSAGE
# =========================================================

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)