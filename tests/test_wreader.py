from unittest import TestCase

from wreader import WReader

class Testwreader(TestCase):
    def setUp(self):
        self.init_key = 'inital_apikey'
        self.init_time = 3
        self.wr = WReader(self.init_key, self.init_time)

        self.mock_json = {'latitude': 21.2870072,
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


    def test_set_apikey(self):
        
        self.assertEqual(self.init_key, self.wr.api_key)

        new_key = '12345'
        self.wr.api_key = new_key
        self.assertEqual(new_key, self.wr.api_key) 

    def test_set_sleeptime(self):
        
        self.assertEqual(self.init_time, self.wr.sleep_time)

        new_time = 12
        self.wr.sleep_time = new_time
        self.assertEqual(new_time, self.wr.sleep_time)



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


if __name__ == '__main__':
    unittest.main()

