from supabase import create_client, Client
import pandas as pd
import os

def load_to_supabase(df: pd.DataFrame, supabase_url: str, supabase_key: str, table_name: str):
    """
    Loads a transformed weather snapshot DataFrame to Supabase.

    Args:
        df (pd.DataFrame): Transformed weather snapshot DataFrame.
        supabase_url (str): Your Supabase project URL.
        supabase_key (str): Your Supabase API key (service role key recommended).
        table_name (str): Target table name in Supabase.

    Returns:
        None
    """
    if df.empty:
        print("DataFrame is empty. Nothing to load.")
        return

    # Initialize Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)

    # Add a UTC timestamp for this extraction
    df["extraction_timestamp"] = pd.Timestamp.utcnow()

    # Convert all data to native Python types for JSON compatibility
    records = df.to_dict(orient="records")

    # Insert rows into Supabase table
    for record in records:
        response = supabase.table(table_name).insert(record).execute()
        if response.status_code not in (200, 201):
            print(f"Error inserting record: {record}")
        else:
            print(f"Inserted: {record['city_name']} ({record['country_code']})")

    print(f"Loaded {len(records)} rows to Supabase table '{table_name}'.")
