import pandas as pd
import sqlite3
import os

DB_FILE = "food_wastage.db"

# Delete the database file if it already exists to start fresh
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Removed old database file '{DB_FILE}'.")

conn = sqlite3.connect(DB_FILE)
print(f"Database file '{DB_FILE}' created.")

# List of your CSV files
csv_files = [
    "providers_data.csv",
    "receivers_data.csv",
    "food_listings_data.csv",
    "claims_data.csv"
]

# Loop through each CSV and load it into a table
for file in csv_files:
    table_name = os.path.splitext(file)[0]
    try:
        df = pd.read_csv(file)
        print(f"Loading data from '{file}' into table '{table_name}'...")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"✅ Success: Table '{table_name}' loaded.")
    except FileNotFoundError:
        print(f"❌ Error: The file '{file}' was not found.")
    except Exception as e:
        print(f"❌ Error loading '{file}': {e}")

conn.close()
print("\nDatabase creation complete!")