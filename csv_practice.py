# ISM2411 Lab 12 - Read a Sales CSV, Write a Cleaned Report
# Name: Antonio Quiros
#
# REFLECTION 1 (Python ETL vs. Excel):
# Doing this in Excel would mean clicking through filters and formulas by hand,
# and the steps aren't recorded anywhere. In Python the whole read-transform-write
# pipeline is a script I can rerun on a new file in seconds, and it scales to
# files far too big for a spreadsheet. Excel is still better for quickly eyeballing
# data, ad-hoc what-if changes, and for people who don't code.
#
# REFLECTION 2 (Append-mode log):
# A business could log every nightly inventory or sales import: one line with the
# timestamp and the total processed. Append mode ("a") adds to the end of the file
# without erasing history, so the log becomes an audit trail of every run. Write
# mode ("w") would wipe out earlier entries each time the script ran.

import csv
from datetime import datetime

SALES_PATH = "data/sales.csv"
CLEANED_PATH = "data/cleaned.csv"
LOG_PATH = "data/run_log.txt"

# ---------- EXERCISE 1: confirm the file opens ----------
with open(SALES_PATH, newline="") as f:
    pass
print("Exercise 1: sales.csv opened successfully\n")

# ---------- EXERCISE 2: read and print raw rows ----------
print("Exercise 2: raw rows (all values are strings)")
with open(SALES_PATH, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
print()

# ---------- EXERCISE 3: skip the header ----------
print("Exercise 3: header printed separately, then data rows")
with open(SALES_PATH, newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)
print()

# ---------- EXERCISE 4: compute totals ----------
print("Exercise 4: line totals")
total_revenue = 0.0
with open(SALES_PATH, newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for product, price, quantity in reader:
        price = float(price)
        quantity = int(quantity)
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}\n")

# ---------- EXERCISE 5: filter and write cleaned.csv ----------
print("Exercise 5: filter orders with total > $100")
original_count = 0
written_count = 0
with open(SALES_PATH, newline="") as infile, \
     open(CLEANED_PATH, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for product, price, quantity in reader:
        original_count += 1
        price = float(price)
        quantity = int(quantity)
        line_total = price * quantity
        if line_total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{line_total:.2f}"])
            written_count += 1
print(f"Rows written: {written_count} of {original_count} original rows\n")

# ---------- EXERCISE 6: csv.DictReader ----------
# csv.reader gives plain lists, so it is simple and fast but relies on column
# position; I'd use it for tiny files with a fixed layout.
# DictReader accesses columns by name, so it keeps working if columns get
# reordered and is easier to read; I'd prefer it for most real files.
print("Exercise 6: DictReader totals")
dict_total = 0.0
with open(SALES_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${dict_total:.2f}")
print("Matches Exercise 4:", abs(dict_total - total_revenue) < 0.005, "\n")

# ---------- EXERCISE 7: summary by product ----------
print("Exercise 7: revenue by product")
summary = {}
with open(SALES_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["product"]
        summary[name] = summary.get(name, 0.0) + float(row["price"]) * int(row["quantity"])
for name in sorted(summary):
    print(f"{name}: ${summary[name]:.2f}")
print()

# ---------- EXERCISE 8: append-mode log ----------
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_PATH, "a") as log:
    log.write(f"{timestamp} - total revenue: ${total_revenue:.2f}\n")
print(f"Exercise 8: appended a line to {LOG_PATH}")