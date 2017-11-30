from unittest import TestCase

from wreader import WReader

class Testwreader(TestCase):
    def setUp(self):
        self.init_key = 'inital_apikey'
        self.init_time = 3
        self.wr = WReader(self.init_key, self.init_time)

        self.mock_json = {'hourly_forecast': [{'FCTTIME': {'UTCDATE': '',
            'age': '',
            'ampm': 'PM',
            'civil': '10:00 PM',
            'epoch': '1511942400',
            'hour': '22',
            'hour_padded': '22',
            'isdst': '0',
            'mday': '28',
            'mday_padded': '28',
            'min': '00',
            'min_unpadded': '0',
            'mon': '11',
            'mon_abbrev': 'Nov',
            'mon_padded': '11',
            'month_name': 'November',
            'month_name_abbrev': 'Nov',
            'pretty': '10:00 PM HST on November 28, 2017',
            'sec': '0',
            'tz': '',
            'weekday_name': 'Tuesday',
            'weekday_name_abbrev': 'Tue',
            'weekday_name_night': 'Tuesday Night',
            'weekday_name_night_unlang': 'Tuesday Night',
            'weekday_name_unlang': 'Tuesday',
            'yday': '331',
            'year': '2017'},
            'condition': 'Mostly Cloudy',
            'dewpoint': {'english': '67',
                'metric': '19'},
            'fctcode': '3',
            'feelslike': {'english': '75',
                'metric': '24'},
            'heatindex': {'english': '-9999',
                'metric': '-9999'},
            'humidity': '78',
            'icon': 'mostlycloudy',
            'icon_url': 'http://icons.wxug.com/i/c/k/nt_mostlycloudy.gif',
            'mslp': {'english': '30.05',
                'metric': '1018'},
            'pop': '0',
            'qpf': {'english': '0.0',
                'metric': '0'},
            'sky': '64',
            'snow': {'english': '0.0',
                'metric': '0'},
            'temp': {'english': '75',
                'metric': '24'},
            'uvi': '0',
            'wdir': {'degrees': '61',
                    'dir': 'ENE'},
            'windchill': {'english': '-9999',
                    'metric': '-9999'},
            'wspd': {'english': '12',
                    'metric': '19'},
            'wx': 'Mostly Cloudy'},
            {'FCTTIME': {'UTCDATE': '',
                'age': '',
                'ampm': 'PM',
                'civil': '11:00 PM',
                'epoch': '1511946000',
                'hour': '23',
                'hour_padded': '23',
                'isdst': '0',
                'mday': '28',
                'mday_padded': '28',
                'min': '00',
                'min_unpadded': '0',
                'mon': '11',
                'mon_abbrev': 'Nov',
                'mon_padded': '11',
                'month_name': 'November',
                'month_name_abbrev': 'Nov',
                'pretty': '11:00 PM HST on November 28, 2017',
                'sec': '0',
                'tz': '',
                'weekday_name': 'Tuesday',
                'weekday_name_abbrev': 'Tue',
                'weekday_name_night': 'Tuesday Night',
                'weekday_name_night_unlang': 'Tuesday Night',
                'weekday_name_unlang': 'Tuesday',
                'yday': '331',
                'year': '2017'},
                'condition': 'Mostly Cloudy',
                'dewpoint': {'english': '67',
                    'metric': '19'},
                'fctcode': '3',
                'feelslike': {'english': '75',
                    'metric': '24'},
                'heatindex': {'english': '-9999',
                    'metric': '-9999'},
                'humidity': '77',
                'icon': 'mostlycloudy',
                'icon_url': 'http://icons.wxug.com/i/c/k/nt_mostlycloudy.gif',
                'mslp': {'english': '30.05',
                    'metric': '1018'},
                'pop': '1',
                'qpf': {'english': '0.0',
                    'metric': '0'},
                'sky': '67',
                'snow': {'english': '0.0',
                    'metric': '0'},
                'temp': {'english': '75',
                    'metric': '24'},
                'uvi': '0',
                'wdir': {'degrees': '60',
                        'dir': 'ENE'},
                'windchill': {'english': '-9999',
                        'metric': '-9999'},
                'wspd': {'english': '12',
                        'metric': '19'},
                'wx': 'Mostly Cloudy'}],
                'response': {'features': {'hourly': 1},
                        'termsofService': 'http://www.wunderground.com/weather/api/d/terms.html',
                        'version': '0.1'}}


    def test_set_apikey(self):
        
        self.assertEqual(self.init_key, self.wr._api_key)

        new_key = '12345'
        self.wr.set_api_key(new_key)
        self.assertEqual(new_key, self.wr._api_key) 

    def test_set_sleeptime(self):
        
        self.assertEqual(self.init_time, self.wr._sleep_time)

        new_time = 12
        self.wr.set_sleep_time(new_time)
        self.assertEqual(new_time, self.wr._sleep_time)

    def test_transform_location_json_to_dataframe(self):

        df = self.wr._transform_location_json_to_dataframe(self.mock_json)
    
        self.assertEqual(df.loc[0,'dew_point'],67) 
        self.assertEqual(df.loc[0,'fctcode'],3) 
        self.assertEqual(df.loc[0,'icon_url'],'http://icons.wxug.com/i/c/k/nt_mostlycloudy.gif') 
        self.assertEqual(df.loc[0,'isodate'],'2017-11-28 22:00:00.00000') 
        self.assertEqual(df.loc[0,'predicted_rain'],0.0) 
        self.assertEqual(df.loc[0,'prediction_of_perspiration'],0.0) 
        
        self.assertEqual(df.loc[1,'temperature'],75) 
        self.assertEqual(df.loc[1,'uv_index'],0) 
        self.assertEqual(df.loc[1,'wind_direction'],'ENE') 
        self.assertEqual(df.loc[1,'wind_direction_degrees'],60) 
        self.assertEqual(df.loc[1,'wind_speed'],12.0) 
        #test json to dataframe

        #test json to dataframe fails if invalid json


if __name__ == '__main__':
    unittest.main()

