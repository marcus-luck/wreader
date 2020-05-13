import pytest

from wreader import WReader

class Testwreader():

    @pytest.fixture
    def wreader(self):
        self.init_key = 'inital_apikey'
        self.init_time = 3
        return WReader(self.init_key, self.init_time)

    @pytest.fixture
    def json_response(self):
        mock_json = [{'latitude': 21.2870072,
                            'longitude': -157.8390944,
                            'timezone': 'Pacific/Honolulu',
                            'hourly': {'summary': 'Partly cloudy throughout the day and breezy starting tomorrow morning.',
                            'icon': 'wind',
                            'data': [{'time': 1542351600,
                                'summary': 'Partly Cloudy',
                                'icon': 'partly-cloudy-night',
                                'precipIntensity': 0,
                                'precipProbability': 0,
                                'temperature': 75.35,
                                'apparentTemperature': 76.13,
                                'dewPoint': 67.05,
                                'humidity': 0.75,
                                'pressure': 1014.94,
                                'windSpeed': 5.6,
                                'windGust': 9.22,
                                'windBearing': 55,
                                'cloudCover': 0.56,
                                'uvIndex': 0,
                                'visibility': 10,
                                'ozone': 253.28},
                            {'time': 1542355200,
                                'summary': 'Mostly Cloudy',
                                'icon': 'partly-cloudy-night',
                                'precipIntensity': 0.0011,
                                'precipProbability': 0.03,
                                'precipType': 'rain',
                                'temperature': 75.11,
                                'apparentTemperature': 76.06,
                                'dewPoint': 68.38,
                                'humidity': 0.8,
                                'pressure': 1015.12,
                                'windSpeed': 9.26,
                                'windGust': 13.41,
                                'windBearing': 62,
                                'cloudCover': 0.66,
                                'uvIndex': 0,
                                'visibility': 10,
                                'ozone': 254.16},
                            ]}}
                            ]
        return mock_json

    def test_getset_attributes(self, wreader):
        
        assert wreader.init_key == wreader.api_key

        new_key = '12345'
        wreader.api_key = new_key
        assert new_key == wreader.api_key 

        
        assert wreader.init_time == wreader.sleep_time

        new_time = 12
        wreader.sleep_time = new_time
        assert new_time, wreader.sleep_time

    def test_transform_location_json_to_dataframe(self):

        df = self.wr._parse_location_json("name", "12.3456,78.9012", self.mock_json)
    
        self.assertEqual(df[0]['dewPoint'], 67.05)
        self.assertEqual(df[0]['icon'], 'partly-cloudy-night')
        self.assertEqual(df[0]['precipIntensity'], 0)
        self.assertEqual(df[0]['precipProbability'], 0)
        self.assertEqual(df[0]['temperature'], 75.35)
        self.assertNotEqual(df[0]['time'], 1542355200)
        self.assertEqual(df[1]['apparentTemperature'], 76.06)
        self.assertEqual(df[1]['uvIndex'], 0)
        self.assertEqual(df[1]['pressure'], 1015.12)
        self.assertEqual(df[1]['windSpeed'], 9.26)
        self.assertEqual(df[1]['windGust'],13.41)
        self.assertEqual(df[1]['windBearing'], 62)
