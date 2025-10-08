from dotenv import load_dotenv
import os

from etl.extract import extract
from etl.transform import transform
from etl.load import init_db, load_df_to_sqlite
from etl.cities import CANADIAN_CITIES

def run_etl():
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        raise ValueError("Please set WEATHER_API_KEY in .env")

    conn = init_db()

    for city in CANADIAN_CITIES:
        print(f"Fetching weather for {city}...")
        raw_data = extract(api_key, city)
        df = transform(raw_data)
        load_df_to_sqlite(df, conn)

    conn.close()
    print("ETL complete. All cities saved to data/weather.db")

if __name__ == "__main__":
    run_etl()
