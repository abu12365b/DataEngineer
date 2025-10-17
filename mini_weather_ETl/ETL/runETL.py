from dotenv import load_dotenv
import os
import sys
import pandas as pd

# Add parent directory to path to import cities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Extract import extract
from Transform import transform_data
from Load import load_to_supabase
from cities import CANADIAN_CITIES

def run_etl():
    # Load .env from parent directory
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(env_path, override=True)
    
    # Load environment variables
    api_key = os.getenv("WEATHER_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    # Use the exact table name as it appears in Supabase (case-sensitive!)
    table_name = "Weather_data"
    
    print(f"Using table: {table_name}")

    # Validate required environment variables
    if not api_key:
        raise ValueError("Please set WEATHER_API_KEY in .env")
    if not supabase_url:
        raise ValueError("Please set SUPABASE_URL in .env")
    if not supabase_key:
        raise ValueError("Please set SUPABASE_KEY in .env")

    # Collect all weather data
    all_data = []
    
    for city in CANADIAN_CITIES:
        print(f"Fetching weather for {city}...")
        raw_df = extract(api_key, city)
        
        if not raw_df.empty:
            transformed_df = transform_data(raw_df)
            if transformed_df is not None and not transformed_df.empty:
                all_data.append(transformed_df)
    
    # Combine all city data
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"\nLoading {len(combined_df)} records to Supabase...")
        
        # Load to Supabase
        result = load_to_supabase(combined_df, supabase_url, supabase_key, table_name)
        print(f"ETL complete. Status: {result['status']}, Loaded: {result['loaded']}, Failed: {result['failed']}")
    else:
        print("No data to load.")

if __name__ == "__main__":
    run_etl()
