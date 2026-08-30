import pandas as pd
import os

# =========================================================
# FILES
# =========================================================

INPUT_FILE = "data/outputs/form20_results_repaired.csv"
OUTPUT_FILE = "data/outputs/form20_results_final.csv"

# =========================================================
# RECOVERED TOTAL VOTES POLLED
# =========================================================

RECOVERED_POLLED = {
    38: 182493,
    39: 233969,
    41: 221259,
    42: 226005,
    43: 190573,
    52: 214129,
    62: 243703,
    63: 220066,
    64: 220055,
    66: 212247,
    67: 230796,
    68: 222933,
    69: 191401,
    149: 236042,
    150: 228895,
    178: 167618,
    179: 203999,
    181: 182792,
    182: 180483,
    183: 182730
}

# =========================================================
# READ REPAIRED FILE
# =========================================================

print("Reading repaired Form-20 file...")

df = pd.read_csv(INPUT_FILE)

print("Total rows:", len(df))

# =========================================================
# CHECK REQUIRED COLUMN
# =========================================================

if "total_votes_polled" not in df.columns:
    raise KeyError(
        "Column 'total_votes_polled' not found. "
        f"Available columns: {df.columns.tolist()}"
    )

# =========================================================
# BACKUP
# =========================================================

backup_file = (
    "data/outputs/"
    "form20_results_repaired_backup_before_polled.csv"
)

df.to_csv(
    backup_file,
    index=False
)

print("\nBackup created:")
print(backup_file)

# =========================================================
# CHECK ORIGINAL MISSING POLLED
# =========================================================

missing_before = df["total_votes_polled"].isna().sum()

print(
    "\nMissing total_votes_polled before repair:",
    missing_before
)

# =========================================================
# REPAIR VALUES
# =========================================================

repaired = 0

for ac_number, polled_value in RECOVERED_POLLED.items():

    mask = (
        (df["ac_number"] == ac_number)
        & (df["total_votes_polled"].isna())
    )

    count = mask.sum()

    if count > 0:

        df.loc[
            mask,
            "total_votes_polled"
        ] = polled_value

        repaired += count

    else:

        print(
            f"WARNING: AC {ac_number} "
            f"was not missing total_votes_polled."
        )

# =========================================================
# VALIDATION
# =========================================================

missing_after = df["total_votes_polled"].isna().sum()

print("\n" + "=" * 60)
print("POLLED REPAIR COMPLETE")
print("=" * 60)

print(
    "Records repaired:",
    repaired
)

print(
    "Missing total_votes_polled before:",
    missing_before
)

print(
    "Missing total_votes_polled after:",
    missing_after
)

# =========================================================
# SAMPLE CHECK
# =========================================================

print("\nRecovered values:")

sample_acs = sorted(
    RECOVERED_POLLED.keys()
)

print(
    df[
        df["ac_number"].isin(sample_acs)
    ][
        ["ac_number", "total_votes_polled"]
    ]
    .sort_values("ac_number")
    .to_string(index=False)
)

# =========================================================
# SAVE FINAL FILE
# =========================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFinal file saved:")
print(OUTPUT_FILE)