import pandas as pd
import shutil


# =========================================================
# FILE PATHS
# =========================================================

RESULTS_FILE = "data/outputs/form20_results.csv"

ECI_ELECTOR_FILE = "data/eci_electors_2026.csv"

BACKUP_FILE = "data/outputs/form20_results_backup.csv"

REPAIRED_FILE = "data/outputs/form20_results_repaired.csv"


# =========================================================
# STEP 1 — READ ORIGINAL RESULTS
# =========================================================

print("Reading original Form-20 results...")

df = pd.read_csv(RESULTS_FILE)

print("Total rows:", len(df))


# =========================================================
# STEP 2 — CREATE BACKUP
# =========================================================

print("\nCreating backup...")

shutil.copy2(
    RESULTS_FILE,
    BACKUP_FILE
)

print("Backup created:")
print(BACKUP_FILE)


# =========================================================
# STEP 3 — READ ECI ELECTOR MASTER
# =========================================================

print("\nReading ECI elector master...")

eci = pd.read_csv(
    ECI_ELECTOR_FILE
)

print(
    "ECI ACs:",
    eci["ac_number"].nunique()
)


# =========================================================
# STEP 4 — FIND MISSING ELECTORS
# =========================================================

missing_mask = (
    df["status"]
    .fillna("")
    .str.strip()
    == "MISSING_ELECTORS"
)

print(
    "\nMISSING_ELECTORS before repair:",
    missing_mask.sum()
)


# =========================================================
# STEP 5 — CREATE LOOKUP
# =========================================================

elector_lookup = dict(
    zip(
        eci["ac_number"],
        eci["total_electors"]
    )
)


# =========================================================
# STEP 6 — FILL ONLY MISSING ELECTORS
# =========================================================

repaired = 0

for idx in df.index[missing_mask]:

    ac = df.loc[idx, "ac_number"]

    if ac in elector_lookup:

        df.loc[idx, "total_electors"] = (
            elector_lookup[ac]
        )

        repaired += 1

    else:

        print(
            f"WARNING: AC {ac} not found in ECI master"
        )


print(
    "\nElectors repaired:",
    repaired
)


# =========================================================
# STEP 7 — CHECK REMAINING MISSING
# =========================================================

remaining_missing = (
    df.loc[
        missing_mask,
        "total_electors"
    ]
    .isna()
    .sum()
)

print(
    "Missing elector values remaining:",
    remaining_missing
)


# =========================================================
# STEP 8 — SHOW SAMPLE
# =========================================================

print("\nSample repaired records:")

sample_acs = [27, 30, 31]

sample = df[
    df["ac_number"].isin(sample_acs)
][
    [
        "ac_number",
        "total_electors",
        "status"
    ]
]

print(
    sample.to_string(index=False)
)


# =========================================================
# STEP 9 — SAVE REPAIRED FILE
# =========================================================

df.to_csv(
    REPAIRED_FILE,
    index=False
)

print("\n" + "=" * 60)
print("REPAIR COMPLETE")
print("=" * 60)

print(
    "Repaired file:",
    REPAIRED_FILE
)