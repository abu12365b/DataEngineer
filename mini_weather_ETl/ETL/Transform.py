import pandas as pd  # This helps us organize data like a spreadsheet

def transform_data(df):
    if df.empty:
        return None

    # Example transformation: convert all column names to lowercase
    df.columns = [col.lower() for col in df.columns]
    
    columns_to_keep = [
        "city_name", "country_code",
        "temperature", "feels_like", "temp_min", "temp_max",
        "humidity", "weather_description",
        "rain_1h", "rain_3h", "snow_1h", "snow_3h"]

    df = df[columns_to_keep]
    
    def chance_of_precipitation(row):
        rain = (row.get("rain_1h", 0) or 0) + (row.get("rain_3h", 0) or 0)
        snow = (row.get("snow_1h", 0) or 0) + (row.get("snow_3h", 0) or 0)

        # Determine type
        if rain > 0 and snow == 0:
            precip_type = "Rain"
        elif snow > 0 and rain == 0:
            precip_type = "Snow"
        elif rain > 0 and snow > 0:
            precip_type = "Mixed"
        else:
            precip_type = "None"

        # Determine chance level (based on total mm)
        total_precip = rain + snow
        if total_precip == 0:
            chance = "Low"
        elif total_precip < 1:
            chance = "Medium"
        else:
            chance = "High"

        return pd.Series({"precipitation_type": precip_type, "chance_of_precipitation": chance})
    
    precip_df = df.apply(chance_of_precipitation, axis=1)
    df = pd.concat([df, precip_df], axis=1)

    df["weather_description"] = df["weather_description"].str.title()
    df[["temperature", "feels_like", "temp_min", "temp_max"]] = df[
        ["temperature", "feels_like", "temp_min", "temp_max"]
    ].round(1)

    return df

