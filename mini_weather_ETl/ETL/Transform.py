import pandas as pd

def transform_data(df):
    if df.empty:
        return None

    df.columns = [col.lower() for col in df.columns]

    # Keep only relevant base columns
    columns_to_keep = [
        "city_name", "country_code",
        "temperature", "feels_like",
        "humidity", "weather_description",
        "rain_1h", "rain_3h", "snow_1h", "snow_3h",
        "wind_speed", "wind_direction",
        "cloudiness", "visibility"
    ]
    df = df[[c for c in columns_to_keep if c in df.columns]]

    # --- Precipitation logic ---
    def precip_info(row):
        rain = (row.get("rain_1h", 0) or 0) + (row.get("rain_3h", 0) or 0)
        snow = (row.get("snow_1h", 0) or 0) + (row.get("snow_3h", 0) or 0)
        total = rain + snow

        if total == 0:
            return pd.Series({"precip_type": "None", "precip_chance": "Low"})
        elif total < 1:
            level = "Medium"
        else:
            level = "High"

        if rain > 0 and snow > 0:
            ptype = "Mixed"
        elif rain > 0:
            ptype = "Rain"
        else:
            ptype = "Snow"

        return pd.Series({"precip_type": ptype, "precip_chance": level})

    df = pd.concat([df, df.apply(precip_info, axis=1)], axis=1)

    # --- Derived metrics ---
    df["weather_description"] = df["weather_description"].str.title()
    df["temperature"] = df["temperature"].round(1)
    df["feels_like"] = df["feels_like"].round(1)

    def humidity_label(h):
        if h < 30:
            return "Dry"
        elif h < 60:
            return "Comfortable"
        else:
            return "Humid"

    df["humidity_label"] = df["humidity"].apply(humidity_label)

    # --- Wind ---
    def wind_label(speed):
        if pd.isna(speed): return None
        if speed < 2: return "Calm"
        elif speed < 6: return "Light breeze"
        elif speed < 10: return "Windy"
        else: return "Strong"
    df["wind_label"] = df["wind_speed"].apply(wind_label)

    # --- Concise summary ---
    def concise_summary(row):
        if row.precip_type == "None":
            precip_text = "No precipitation expected"
        else:
            precip_text = f"{row.precip_chance} chance of {row.precip_type.lower()}"

        return (
            f"{row.city_name} ({row.country_code}): {row.temperature}°C "
            f"(feels {row.feels_like}°C), {row.weather_description}. "
            f"{precip_text}. {row.humidity_label}, {row.wind_label.lower()} winds."
        )

    df["snapshot"] = df.apply(concise_summary, axis=1)

    # Return only the essentials for a clean display
    return df[[
        "city_name", "country_code",
        "temperature", "feels_like",
        "humidity_label", "precip_type", "precip_chance",
        "wind_label", "snapshot"
    ]]
