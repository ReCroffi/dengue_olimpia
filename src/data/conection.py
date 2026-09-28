
import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = BASE_DIR / "data" / "raw" / "dengue_1-53.csv"
DB_PATH = BASE_DIR / "dengue_olimpia.duckdb"



con = duckdb.connect(str(DB_PATH))

# O DuckDB pode ler o CSV direto sem nem precisar do Pandas:
con.execute(f"""CREATE OR REPLACE TABLE dengue_olimpia AS SELECT * FROM read_csv_auto('{CSV_PATH}', header=True)""")

con.close()