import sys
from requests import get
from datetime import datetime
from time import sleep

from logging import basicConfig, Formatter, getLogger, StreamHandler, 
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()


class WReader():
    def __init__(self, api_key, sleep_time = 10, logger=None):
        self._api_key = api_key
        self._sleep_time = sleep_time


    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def set_api_key(self, api_key):
        """Set Darksky api_key
        Sign up for an API key at:
        https://darksky.net/dev

        args:
            param1: (str) api_key
        
        """

        if type(api_key) is not str:
            raise ValueError("api key need to be a string")
        self._api_key = api_key


    @property
    def sleep_time(self):
        return self._api_key

    @sleep_time.setter
    def set_sleep_time(self, sleep_time):
        """Set sleeptime in between api calls
        Sleeptime is used to not flood the api if they
        decide to enforce a max calls per minute policy.
        Remnant from Wundergrounds API.

        args:
            param1: (int) sleep_time
        
        """
        if sleep_time <= 0 or type(sleep_time) is not int:
            raise ValueError("sleep time need to be a postive integer")
        self._sleep_time = sleep_time


    def _get_location_json(self, location):
        """Get 24h weather data from location

        Args:
            param1: (str) location as XXXX,YYYY

        Returns:
            (dict) JSON

        """
        

        url = "http://api.wunderground.com/api/%s/hourly/q/%s.json" % (self._api_key, location)

        try:
            response = get(url)
        except ConnectionError:
            logger.error('get_location_json failed: %s' % (e,))
        try:
            return response.json()
        except ValueError, e:
            logger.error('get_location_json failed: %s' % (e,))
            return {}


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
        'predicted_rain_metric': [float(whour['qpf']['metric']) for whour in ld],
        'prediction_of_perspiration': [float(whour['pop']) for whour in ld],
        'temperature': [float(whour['temp']['english']) for whour in ld],
        'temperature_metric': [float(whour['temp']['metric']) for whour in ld],
        'dew_point': [float(whour['dewpoint']['english']) for whour in ld],
        'dew_point_metric': [float(whour['dewpoint']['metric']) for whour in ld],
        'mslp': [float(whour['mslp']['english']) for whour in ld],
        'mslp_metric': [float(whour['mslp']['metric']) for whour in ld],
        'humidity': [int(whour['humidity']) for whour in ld],
        'fctcode': [int(whour['fctcode']) for whour in ld],
        'wind_direction_degrees': [int(whour['wdir']['degrees']) for whour in ld],
        'wind_direction': [str(whour['wdir']['dir']) for whour in ld],
        'wind_speed': [float(whour['wspd']['english']) for whour in ld],
        'wind_speed_metric': [float(whour['wspd']['metric']) for whour in ld],
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

