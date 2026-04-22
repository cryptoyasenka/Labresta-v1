"""Find second sheet structure + sample products."""
import json


def main():
    with open("labresta_x_dump.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Find the products sheet (the one with 207 rows)
    prod_sheet = None
    for name, sheet in data.items():
        if sheet["max_row"] > 100:
            prod_sheet = (name, sheet)
            break

    if not prod_sheet:
        print("Could not find products sheet")
        return

    name, sheet = prod_sheet
    print(f"=== {name}: {sheet['max_row']} rows x {sheet['max_col']} cols ===\n")
    rows = sheet["rows"]

    # Show first 5 rows (headers + samples)
    for i, r in enumerate(rows[:5]):
        print(f"Row {i}: {r}")

    # Find where data starts (first row where col 0 is a number)
    data_start = None
    for i, r in enumerate(rows):
        if r and isinstance(r[0], int):
            data_start = i
            break

    print(f"\nData starts at row {data_start}")
    print(f"\n=== Sample 3 data rows ===")
    for i in range(data_start, min(data_start + 3, len(rows))):
        print(f"Row {i}: {rows[i]}")


if __name__ == "__main__":
    main()
