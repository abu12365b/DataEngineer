from supabase import create_client, Client
import pandas as pd

def load_to_supabase(df: pd.DataFrame, supabase_url: str, supabase_key: str, table_name: str):
    """
    Loads a transformed weather snapshot DataFrame to Supabase.

    Args:
        df (pd.DataFrame): Transformed weather snapshot DataFrame.
        supabase_url (str): Your Supabase project URL.
        supabase_key (str): Your Supabase API key (service role key recommended).
        table_name (str): Target table name in Supabase.

    Returns:
        dict: Summary of the load operation with success/failure counts.
    """
    if df.empty:
        print("DataFrame is empty. Nothing to load.")
        return {"status": "skipped", "loaded": 0, "failed": 0}

    # Initialize Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)

    # Create a copy to avoid mutating the original DataFrame
    df_copy = df.copy()
    
    # Add a UTC timestamp for this extraction
    df_copy["extraction_timestamp"] = pd.Timestamp.now(tz='UTC')

    # Convert DataFrame to dict and handle type conversion
    records = df_copy.astype(object).where(pd.notnull(df_copy), None).to_dict(orient="records")
    
    # Convert any remaining pandas/numpy types to native Python types
    for record in records:
        for key, value in record.items():
            # Handle pandas Timestamp objects
            if isinstance(value, pd.Timestamp):
                record[key] = value.isoformat() if value else None
            # Handle datetime objects
            elif hasattr(value, 'isoformat') and callable(value.isoformat):
                record[key] = value.isoformat() if value else None
            # Handle numpy types
            elif hasattr(value, 'item'):
                record[key] = value.item()
            # Handle NaN/None
            elif pd.isna(value):
                record[key] = None

    try:
        # Batch insert for efficiency
        response = supabase.table(table_name).insert(records).execute()
        print(f"Successfully loaded {len(records)} rows to Supabase table '{table_name}'.")
        return {"status": "success", "loaded": len(records), "failed": 0}
        
    except Exception as e:
        print(f"Error loading data to Supabase: {e}")
        print("Attempting individual inserts as fallback...")
        
        # Fallback: try inserting one by one to identify problematic records
        success_count = 0
        failed_records = []
        
        for record in records:
            try:
                supabase.table(table_name).insert(record).execute()
                print(f"✓ Inserted: {record.get('city_name', 'Unknown')} ({record.get('country_code', 'Unknown')})")
                success_count += 1
            except Exception as e:
                print(f"✗ Failed to insert {record.get('city_name', 'Unknown')}: {e}")
                failed_records.append(record)
        
        print(f"Loaded {success_count}/{len(records)} rows. {len(failed_records)} failed.")
        return {"status": "partial", "loaded": success_count, "failed": len(failed_records), "failed_records": failed_records}
