import pandas as pd
import pytest

from ETL.Transform import transform_data


def base_row(**overrides):
    row = {
        "city_name": "TestCity",
        "country_code": "TC",
        "temperature": 12.345,
        "feels_like": 11.678,
        "humidity": 50,
        "weather_description": "clear sky",
        "rain_1h": 0,
        "rain_3h": 0,
        "snow_1h": 0,
        "snow_3h": 0,
        "wind_speed": 1.5,
        "wind_direction": 0,
        "cloudiness": 0,
        "visibility": 10000,
    }
    row.update(overrides)
    return row


def test_empty_df_returns_none():
    df = pd.DataFrame()
    assert transform_data(df) is None


def test_precipitation_none_low():
    df = pd.DataFrame([base_row()])
    out = transform_data(df)
    assert out.loc[0, "precip_type"] == "None"
    assert out.loc[0, "precip_chance"] == "Low"


def test_precipitation_rain_high():
    r = base_row(rain_3h=2.0)
    df = pd.DataFrame([r])
    out = transform_data(df)
    assert out.loc[0, "precip_type"] == "Rain"
    assert out.loc[0, "precip_chance"] == "High"


def test_precipitation_snow_high():
    r = base_row(snow_1h=1.5)
    df = pd.DataFrame([r])
    out = transform_data(df)
    assert out.loc[0, "precip_type"] == "Snow"
    assert out.loc[0, "precip_chance"] == "High"


def test_precipitation_mixed_medium():
    # total < 1 but both rain and snow > 0 -> Mixed, Medium
    r = base_row(rain_1h=0.5, snow_1h=0.4)
    df = pd.DataFrame([r])
    out = transform_data(df)
    assert out.loc[0, "precip_type"] == "Mixed"
    assert out.loc[0, "precip_chance"] == "Medium"


@pytest.mark.parametrize(
    "humidity,expected",
    [
        (20, "Dry"),
        (30, "Comfortable"),  # 30 is not <30 so Comfortable
        (59, "Comfortable"),
        (60, "Humid"),
        (85, "Humid"),
    ],
)
def test_humidity_label(humidity, expected):
    r = base_row(humidity=humidity)
    df = pd.DataFrame([r])
    out = transform_data(df)
    assert out.loc[0, "humidity_label"] == expected


@pytest.mark.parametrize(
    "speed,expected",
    [
        (0.5, "Calm"),
        (2.0, "Light breeze"),  # 2.0 is not <2 so Light breeze
        (5.9, "Light breeze"),
        (6.0, "Windy"),
        (9.9, "Windy"),
        (10.0, "Strong"),
    ],
)
def test_wind_label(speed, expected):
    r = base_row(wind_speed=speed)
    df = pd.DataFrame([r])
    out = transform_data(df)
    assert out.loc[0, "wind_label"] == expected


def test_temperature_rounding_and_snapshot_contents():
    r = base_row(temperature=12.349, feels_like=11.944, weather_description="light rain", wind_speed=7)
    df = pd.DataFrame([r])
    out = transform_data(df)
    # Check rounding to 1 decimal place
    assert out.loc[0, "temperature"] == pytest.approx(12.3, rel=1e-3)
    assert out.loc[0, "feels_like"] == pytest.approx(11.9, rel=1e-3)
    # Check weather description title-cased
    assert "Light Rain" in out.loc[0, "snapshot"]
    # Check that the city and country appear
    assert "TestCity (TC):" in out.loc[0, "snapshot"]
    # Check humidity label and wind_label text in snapshot (wind_label is lowercased there)
    assert out.loc[0, "humidity_label"] in out.loc[0, "snapshot"]
    assert out.loc[0, "wind_label"].lower() in out.loc[0, "snapshot"]


test_temperature_rounding_and_snapshot_contents()
