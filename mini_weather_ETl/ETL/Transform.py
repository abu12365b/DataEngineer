import pandas as pd

def transform_data(df):
    if df.empty:
        return None

    # Normalize column names
    df.columns = [col.lower() for col in df.columns]

    # Keep only relevant weather columns
    columns_to_keep = [
        "city_name", "country_code",
        "temperature", "feels_like", "temp_min", "temp_max",
        "humidity", "weather_description",
        "rain_1h", "rain_3h", "snow_1h", "snow_3h",
        "wind_speed", "wind_direction", "cloudiness", "visibility"
    ]

    df = df[[col for col in columns_to_keep if col in df.columns]]

    # ---  Precipitation Summary ---
    def precip_info(row):
        rain = (row.get("rain_1h", 0) or 0) + (row.get("rain_3h", 0) or 0)
        snow = (row.get("snow_1h", 0) or 0) + (row.get("snow_3h", 0) or 0)

        # Type of precipitation
        if rain > 0 and snow == 0:
            precip_type = "Rain"
        elif snow > 0 and rain == 0:
            precip_type = "Snow"
        elif rain > 0 and snow > 0:
            precip_type = "Mixed"
        else:
            precip_type = "None"

        # Chance of precipitation (based on mm)
        total_precip = rain + snow
        if total_precip == 0:
            chance = "Low"
        elif total_precip < 1:
            chance = "Medium"
        else:
            chance = "High"

        # Intensity category
        if total_precip == 0:
            intensity = "None"
        elif total_precip < 2:
            intensity = "Light"
        elif total_precip < 5:
            intensity = "Moderate"
        else:
            intensity = "Heavy"

        return pd.Series({
            "precipitation_type": precip_type,
            "chance_of_precipitation": chance,
            "precipitation_intensity": intensity
        })

    precip_df = df.apply(precip_info, axis=1)
    df = pd.concat([df, precip_df], axis=1)

    # ---  Comfort Metrics ---
    def humidity_label(h):
        if h < 30:
            return "Dry"
        elif h < 60:
            return "Comfortable"
        else:
            return "Humid"

    df["humidity_level"] = df["humidity"].apply(humidity_label)
    df["temperature_feel_diff"] = (df["feels_like"] - df["temperature"]).round(1)

    # ---  Wind Snapshot ---
    if "wind_speed" in df.columns:
        def wind_category(speed):
            if pd.isna(speed):
                return None
            if speed < 2:
                return "Calm"
            elif speed < 5:
                return "Breezy"
            elif speed < 10:
                return "Windy"
            else:
                return "Strong"
        df["wind_speed_category"] = df["wind_speed"].apply(wind_category)

    if "wind_direction" in df.columns:
        def wind_direction_cardinal(deg):
            if pd.isna(deg):
                return None
            dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            return dirs[int((deg % 360) / 45)]
        df["wind_direction_cardinal"] = df["wind_direction"].apply(wind_direction_cardinal)

    # ---  Cloud / Visibility Snapshot ---
    if "cloudiness" in df.columns:
        def cloud_cover_label(c):
            if c < 20:
                return "Clear"
            elif c < 60:
                return "Partly Cloudy"
            else:
                return "Overcast"
        df["cloud_cover_level"] = df["cloudiness"].apply(cloud_cover_label)

    if "visibility" in df.columns:
        def visibility_label(v):
            if pd.isna(v):
                return None
            km = v / 1000
            if km < 2:
                return "Low"
            elif km < 10:
                return "Moderate"
            else:
                return "Clear"
        df["visibility_level"] = df["visibility"].apply(visibility_label)

    # ---  Clean Up ---
    df["weather_description"] = df["weather_description"].str.title()
    df[["temperature", "feels_like", "temp_min", "temp_max"]] = df[
        ["temperature", "feels_like", "temp_min", "temp_max"]
    ].round(1)

    # ---  Weather Snapshot Summary ---
    def make_summary(row):
        return (
            f"{row.city_name} ({row.country_code}): {row.temperature}°C, feels {row.feels_like}°C — "
            f"{row.weather_description}, {row.humidity_level}, "
            f"{row.get('wind_speed_category', '') or ''} winds, "
            f"{row.chance_of_precipitation} chance of {row.precipitation_type.lower()}."
        )

    df["weather_summary"] = df.apply(make_summary, axis=1)

    return df
