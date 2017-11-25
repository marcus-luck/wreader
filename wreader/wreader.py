import pandas as pd
from requests import get
from datetime import datetime
from time import sleep


class WReader():
    def __init__(self, api_key, sleep_time = 10):
        self._api_key = api_key
        self._sleep_time = sleep_time


    def set_sleep_time(self, sleep_time):
        """Set sleeptime in between api calls

        args:
            param1: (int) sleep_time
        
        """
        self._sleep_time = sleep_time


    def set_api_key(self, api_key):
        """Set  wunderground api_key

        args:
            param1: (str) api_key
        
        """
        self._api_key = api_key


    def _get_location_json(self, location):
        """Get 24h weather data from location

        Args:
            param1: (str) location as XXXX,YYYY

        Returns:
            Json

        """
        

        url = "http://api.wunderground.com/api/%s/hourly/q/%s.json" % (self._api_key, location)

        response = get(url)

        return response.json()


    def _transform_location_json_to_dataframe(self, location_data):
        """Return a list containing hour for hour data for selected location
        
        args:
            param1: (str) location as XXXX,YYYY

        Returns:
            Pandas DataFrame with hours as rows and data as columns

        """

        # Define dictionary
        weather_data = pd.DataFrame()
        
        # Go through location json and add relevant data to DataFrame
        ld = location_data['hourly_forecast']

        # Set time of extraction
        nowtime = datetime.now().isoformat(' ')

        weather_data= pd.concat([weather_data, pd.DataFrame({
        'predicted_rain': [float(whour['qpf']['english']) for whour in ld],
        'prediction_of_perspiration': [float(whour['pop']) for whour in ld],
        'temperature': [float(whour['temp']['english']) for whour in ld],
        'dew_point': [float(whour['dewpoint']['english']) for whour in ld],
        'mslp': [float(whour['mslp']['english']) for whour in ld],
        'humidity': [int(whour['humidity']) for whour in ld],
        'fctcode': [int(whour['fctcode']) for whour in ld],
        'wind_direction_degrees': [int(whour['wdir']['degrees']) for whour in ld],
        'wind_direction': [str(whour['wdir']['dir']) for whour in ld],
        'wind_speed': [float(whour['wspd']['english']) for whour in ld],
        'uv_index': [int(whour['uvi']) for whour in ld],
        'icon_url': [str(whour['icon_url']) for whour in ld],
        'isodate': [str('{}-{}-{} {}:{}:00.00000'.format(whour['FCTTIME']['year'],
            whour['FCTTIME']['mon_padded'],
            whour['FCTTIME']['mday_padded'],
            whour['FCTTIME']['hour_padded'],
            whour['FCTTIME']['min'])) for whour in ld],
        'nowtime': nowtime,
        })], ignore_index=True)

        return weather_data


    def get_location_data(self, location):
        """Returns a datatable of 24h, hour by hour weather of one locations
            Intention is to return a pandas DataFrame of with 24 hour for one specific location.
            Columns in DataFrame are the variables from wunderground.

        args: 
            (str) string of location coordinates.

        returns:
            (pandas DataFrame) 24h, Hour by hour weather of all locations
        """

        # Get location data as json
        location_json = self._get_location_json(location)
        
        # Transform json data to DataFrame
        location_dataframe = self._transform_location_json_to_dataframe(location_json)        
        
        # Add location as a column
        location_dataframe['location'] = location

        return location_dataframe


    def get_all_locations_data(self, locations):
        """Returns a datatable of 24h, hour by hour weather of all locations
            Intention is to return a pandas DataFrame of with 24 hour datarows per location.
            Columns in DataFrame are the variables from wunderground.

        args: 
            (list) list of location coordinates.

        returns:
            (pandas DataFrame) 24h, Hour by hour weather of all locations
        """
                
        # Define dataframe
        all_locations_datatable = pd.DataFrame()
        
        # Go through all locations
        for location in locations:

            # Fetch location weather data for the next 24h
            location_json = self._get_location_json(location)

            # Transform location json to DataFrame
            location_datatable = self._transform_location_json_to_dataframe(
                    location_json)
            
            # Add location to dataframe
            location_datatable['location'] = location

            # Combine locations_dataframes into one dataframe
            all_locations_datatable = pd.concat([all_locations_datatable, location_datatable], ignore_index=True)
            
            # Don't overflow the api
            sleep(self._sleep_time)


        return all_locations_datatable

