''' WReader package

Free to use and distribute.

Author:
Marcus Luck
marcus.luck@outlook.com
'''
from time import sleep, gmtime
from requests import get

class WReader():
    ''' Class to read weatherdata from DarkSky API.

    input:
        (str) api_key
        (int) sleep_time, the time betwen calls to the API
    '''

    def __init__(self, api_key, sleep_time=10):
        self._api_key = api_key
        self._sleep_time = sleep_time


    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Set Darksky api_key
        Sign up for an API key at:
        https://darksky.net/dev

        args:
            param1: (str) api_key

        """

        if isinstance(api_key, str):
            self._api_key = api_key
        else:
            raise ValueError("api key need to be a string")



    @property
    def sleep_time(self):
        '''The time in between calls to the API.

        input:
            (int) sleep_time

        '''
        return self._sleep_time


    @sleep_time.setter
    def sleep_time(self, sleep_time):
        """Set sleeptime in between api calls
        Sleeptime is used to not flood the api if they
        decide to enforce a max calls per minute policy.
        Remnant from Wundergrounds API.

        args:
            sleep_time (int): time in seconds between calls to the api.

        """
        if sleep_time <= 0:
            raise ValueError("sleep time need to be a postive integer")
        if isinstance(sleep_time, int):
            self._sleep_time = sleep_time
        else:
            raise TypeError("sleep time need to be an integer")

    def _get_location_json(self, coordinates, exclude="currently,minutely,daily,alerts,flags"):
        """Get 24h weather data from location

        Inputs:
            name (str): Human readable name of location.
            Location (str): location as XXXX,YYYY
            exclude (str): "currently,minutely,hourly,daily,alerts,flags" without spaces.

        Returns:
            JSON (dict): JSON

        """

        url = f"https://api.darksky.net/forecast/{self._api_key}/{coordinates}?exclude={exclude}"

        try:
            response = get(url)
        except ConnectionError as e_msg:
            print('get_location_json failed: %s', e_msg)

        try:
            return response.json()
        except ValueError as e_msg:
            print('get_location_json failed: %s', e_msg)
            return {}


    def _parse_location_json(self, name, coordinates, location_data):
        """Return a list containing hour for hour data for selected location

        args:
            location_data (JSON):

        Returns:
            List of dicts

        """

        # Define list
        weather_data = []

        # Go through location json
        for location in location_data['hourly']['data']:

            # Set time of extraction
            location['read_time'] = gmtime()
            location['name'] = name
            location['coordinates'] = coordinates
            weather_data.append(location)

        return weather_data


    def get_all_locations_data(self, locations):
        """Returns a datatable of 24h, hour by hour weather of all locations
        Intention is to return a pandas DataFrame of with 24 hour datarows per location.
        Columns in DataFrame are the variables from wunderground.

        args:
            locations (dict): dict of 'location name': location coordinates as XXXXX,YYYYY
            {"location name1": "longitude,latitude", "location2 name": "logitude2,latitude2"}

        returns:
            (list) of dicts

                returns:
            location (dict): time: dicts, see example dict.

        Example:
            dict = {'location': 'Wahiwa beach',
                    'latitude': 21.2870072,
                    'longitude': -157.8390944,
                    'time': 1541397600,
                    'summary': 'Partly Cloudy',
                    'icon': 'partly-cloudy-night',
                    'precipIntensity': 0.0065,
                    'precipProbability': 0.1,
                    'precipType': 'rain',
                    'temperature': 77.12,
                    'apparentTemperature': 78.15,
                    'dewPoint': 69.37,
                    'humidity': 0.77,
                    'pressure': 1015.44,
                    'windSpeed': 8.23,
                    'windGust': 12.43,
                    'windBearing': 80,
                    'cloudCover': 0.27,
                    'uvIndex': 0,
                    'visibility': 9.43,
                    'ozone': 266.25}
        """

        all_locations = []
        # Go through all locations
        for name, coordinates in locations.items():

            # Fetch location weather data for the next 24h
            location_json = self._get_location_json(coordinates)

            all_locations += self._parse_location_json(name, coordinates, location_json)

            # Don't overflow the api
            sleep(self._sleep_time)

        return all_locations
