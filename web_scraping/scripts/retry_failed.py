import pandas as pd

# =========================================================
# FILE PATHS
# =========================================================

INPUT_FILE = "data/outputs/form20_results.csv"
OUTPUT_FILE = "data/outputs/form20_retry.csv"


def main():

    print("Reading existing results...")

    # -----------------------------------------------------
    # READ MAIN RESULTS
    # -----------------------------------------------------

    df = pd.read_csv(INPUT_FILE)

    # -----------------------------------------------------
    # SELECT ONLY PROBLEMATIC RECORDS
    # -----------------------------------------------------

    retry_df = df[
        df["status"].fillna("").str.strip() != "OK"
    ].copy()

    # -----------------------------------------------------
    # SORT BY AC NUMBER
    # -----------------------------------------------------

    retry_df = retry_df.sort_values(
        "ac_number"
    )

    # -----------------------------------------------------
    # SAVE RETRY LIST
    # -----------------------------------------------------

    retry_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # -----------------------------------------------------
    # REPORT
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("RETRY LIST CREATED")
    print("=" * 60)

    print(
        f"Total PDFs: {len(df)}"
    )

    print(
        f"Successful (OK): "
        f"{(df['status'] == 'OK').sum()}"
    )

    print(
        f"Need retry: "
        f"{len(retry_df)}"
    )

    print("\nProblematic status breakdown:")

    print(
        retry_df["status"].value_counts()
    )

    print("\nACs needing retry:")

    print(
        retry_df[
            ["ac_number", "status"]
        ].to_string(index=False)
    )

    print(
        f"\nSaved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()