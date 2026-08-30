import pandas as pd

file_path = r"data/outputs/form20_results_repaired.csv"

df = pd.read_csv(file_path)

print("=" * 50)
print("FORM-20 RESULTS CHECK")
print("=" * 50)

print("\nTotal ACs:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isna().sum())

# Find the polled column
polled_col = "total_votes_polled"

if polled_col in df.columns:

    print("\n" + "=" * 50)
    print("POLLED VALUE CHECK")
    print("=" * 50)

    print("Total rows:", len(df))
    print("Polled available:", df[polled_col].notna().sum())
    print("Polled missing:", df[polled_col].isna().sum())

    print("\nMissing Polled ACs:")

    missing = df[df[polled_col].isna()]

    if len(missing) > 0:
        print(missing[["ac_number", "constituency"]].to_string(index=False))
    else:
        print("None")

else:
    print("\nColumn total_votes_polled not found!")

print("\n" + "=" * 50)
print("CHECK FINISHED")
print("=" * 50)