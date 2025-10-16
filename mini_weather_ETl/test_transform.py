#!/usr/bin/env python3
"""
These are our super special transform tests!
Like checking if our weather data gets cleaned up nicely before we show it to friends.

We'll use a friendly unittest style (like in our extract tests),
with clear checks and playful explanations.
"""

import unittest  # Our helpful test runner
import sys
import os
import pandas as pd

# Make sure Python can find our ETL package (mirrors the extract tests' pattern)
sys.path.append(os.path.join(os.path.dirname(__file__), 'ETL'))

from ETL.Transform import transform_data


def make_base_row(**overrides):
    """
    Build a single weather record with sensible defaults that we can override.
    Like a base LEGO structure we can tweak with different bricks.
    """
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


class TestTransformFunction(unittest.TestCase):
    """
    Our cozy transform test playground!
    We'll check precipitation logic, labels, rounding, and the snapshot text.
    """

    def test_empty_df_returns_none(self):
        """If we give an empty table, we should get back nothing (None)."""
        df = pd.DataFrame()
        self.assertIsNone(transform_data(df))

    def test_precipitation_none_low(self):
        """No rain or snow means precip_type None and Low chance."""
        df = pd.DataFrame([make_base_row()])
        out = transform_data(df)
        self.assertEqual(out.loc[0, "precip_type"], "None")
        self.assertEqual(out.loc[0, "precip_chance"], "Low")

    def test_precipitation_rain_high(self):
        """Lots of rain should be typed as Rain with High chance."""
        r = make_base_row(rain_3h=2.0)
        df = pd.DataFrame([r])
        out = transform_data(df)
        self.assertEqual(out.loc[0, "precip_type"], "Rain")
        self.assertEqual(out.loc[0, "precip_chance"], "High")

    def test_precipitation_snow_high(self):
        """Lots of snow should be typed as Snow with High chance."""
        r = make_base_row(snow_1h=1.5)
        df = pd.DataFrame([r])
        out = transform_data(df)
        self.assertEqual(out.loc[0, "precip_type"], "Snow")
        self.assertEqual(out.loc[0, "precip_chance"], "High")

    def test_precipitation_mixed_medium(self):
        """A little of both rain and snow (<1 total) becomes Mixed with Medium chance."""
        r = make_base_row(rain_1h=0.5, snow_1h=0.4)
        df = pd.DataFrame([r])
        out = transform_data(df)
        self.assertEqual(out.loc[0, "precip_type"], "Mixed")
        self.assertEqual(out.loc[0, "precip_chance"], "Medium")

    def test_humidity_label(self):
        """Humidity buckets: Dry (<30), Comfortable (<60), Humid (>=60)."""
        cases = [
            (20, "Dry"),
            (30, "Comfortable"),  # 30 is not <30 so Comfortable
            (59, "Comfortable"),
            (60, "Humid"),
            (85, "Humid"),
        ]
        for h, expected in cases:
            with self.subTest(humidity=h):
                r = make_base_row(humidity=h)
                df = pd.DataFrame([r])
                out = transform_data(df)
                self.assertEqual(out.loc[0, "humidity_label"], expected)

    def test_wind_label(self):
        """Wind labels: Calm (<2), Light breeze (<6), Windy (<10), Strong (>=10)."""
        cases = [
            (0.5, "Calm"),
            (2.0, "Light breeze"),  # 2.0 is not <2 so Light breeze
            (5.9, "Light breeze"),
            (6.0, "Windy"),
            (9.9, "Windy"),
            (10.0, "Strong"),
        ]
        for speed, expected in cases:
            with self.subTest(speed=speed):
                r = make_base_row(wind_speed=speed)
                df = pd.DataFrame([r])
                out = transform_data(df)
                self.assertEqual(out.loc[0, "wind_label"], expected)

    def test_temperature_rounding_and_snapshot_contents(self):
        """Temperature rounds to 1 decimal; snapshot includes title-cased weather and key fields."""
        r = make_base_row(
            temperature=12.349,
            feels_like=11.944,
            weather_description="light rain",
            wind_speed=7,
        )
        df = pd.DataFrame([r])
        out = transform_data(df)

        # Rounding to 1 decimal place
        self.assertAlmostEqual(out.loc[0, "temperature"], 12.3, places=2)
        self.assertAlmostEqual(out.loc[0, "feels_like"], 11.9, places=2)

        # Snapshot content checks
        snapshot = out.loc[0, "snapshot"]
        self.assertIn("Light Rain", snapshot)  # Title-cased description
        self.assertIn("TestCity (TC):", snapshot)  # City and country
        self.assertIn(out.loc[0, "humidity_label"], snapshot)  # Humidity label appears
        self.assertIn(out.loc[0, "wind_label"].lower(), snapshot)  # wind label lowercased in text


if __name__ == '__main__':
    # Run our transform tests with a chatty output, just like in the extract unittest file
    unittest.main(verbosity=2)
