''' WReader package

Free to use and distribute.

Author:
Marcus Luck
'''
from time import sleep, gmtime
from requests import get
from typing import List, Dict, Any
import time
from logging import getLogger

LOGGER = getLogger(__name__)

class WReader():
    ''' Class to read weatherdata from DarkSky API.

    Read a list of locations from the API, agregates the responses 
    into a list. where each item is a dictionary with the data representing
    one hour at one location.

    Functions:
        get_all_locations_data

    Attributes:
        api_key (str) : Sign up for an API key at: https://darksky.net/dev
        sleep_time (float), the time betwen calls to the API
        individual (bool): store hourly data instead of collection by location.
    '''

    def __init__(self, api_key: str, sleep_time: float = 10):
        self._api_key = api_key
        self._sleep_time = sleep_time
        self.individual = False


    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str):
        """Set Darksky api_key

        args:
            api_key (str): api_key
        """
        if not isinstance(api_key, str):
            raise ValueError("api key need to be a string")
        self._api_key = api_key


    @property
    def sleep_time(self) -> float:
        """Get/Set sleeptime in between api calls.

        Sleeptime is used to not flood the api if they
        decide to enforce a max calls per minute policy.
        Remnant from Wundergrounds API.

        args:
            sleep_time (int): time in seconds between calls to the api.

        """
        return self._sleep_time

    @sleep_time.setter
    def sleep_time(self, sleep_time: float):

        if sleep_time <= 0:
            raise ValueError("sleep time need to be a postive integer")
        if not isinstance(sleep_time, int):
            raise TypeError("sleep time need to be an integer")
        self._sleep_time = sleep_time

    def get_all_locations_data(self, locations: List[Dict[str, str]], exclude: list) -> List[dict]:
        """Returns a list of 24 hour, hour by hour weather of all locations.

        args:
            locations (list): list of dicts containing: name, side, latitude, longitude
            exclude (list): list of excludes eg. ["currently","minutely","daily","alerts","flags"]

        returns:
            location (dict): a list of dictionaries of forecast data, see https://darksky.net/dev/docs
        """

        all_locations = []
        # Go through all locations
        for loc in locations:
            print(loc)
            coordinates = (loc["latitude"], loc["longitude"])
            # Fetch location weather data for the next 24h
            location_json = self._get_location_json(coordinates, exclude)

            if self.individual:
                all_locations += self._parse_location_json(loc['name'], coordinates, location_json)
            else:
                location_json['name'] = loc['name']
                location_json['side'] = loc['side']
                location_json['hourly'] = location_json['hourly']['data']
                all_locations.append(location_json)

            # Don't overflow the api
            sleep(self._sleep_time)

        return all_locations

    def _get_location_json(self, coordinates: tuple, exclude: List[str]):
        """Get 24h weather data from location

        Inputs:
            name (str): Human readable name of location.
            Location (tuple): (XXXX, YYYY)
            exclude (list): list of excludes eg. ["currently","minutely","daily","alerts","flags"]

        Returns:
            JSON (dict): JSON

        """
        exclude = self._excludes_to_string(exclude)

        latitude, longitude = coordinates

        url = f"https://api.darksky.net/forecast/{self._api_key}/{latitude},{longitude}?exclude={exclude}"

        return self._get_retry(url)

    def _get_retry(self, url, tries=4, delay=3, backoff=2):
        """Get with a exponential retry.

        Returns the value of the url unless there's an error
        in which case it logs it and retrys again with an exponentially longer
        wait time.

        Args:
            url (str):
            tries (int):
            delay (int):
            backoff (int):

        Returns:

        """
        mtries, mdelay = tries, delay
        while mtries > 1:
            try:
                response = get(url)
                return response.json()
            except (ConnectionError, ValueError) as e:
                msg = f'{e}, Retrying in {mdelay} seconds...'

                LOGGER.warning(msg)

                time.sleep(mdelay)
                mtries -= 1
                mdelay *= backoff
        LOGGER.error("Couldn't connect to %s, timed out after %s retries.", url, tries)
        return {}


    def _excludes_to_string(self, exclude: list) -> str:
        """Takes a list of words to exclude returns a comma separated string.

        Args:
            exclude(list):list of words, eg. ["currently","minutely","daily","alerts","flags"]

        Returns:
            a comma separated string of the words, eg. 'currently,minutely,daily,alerts,flags'
        """
        return",".join(exclude)

    def _parse_location_json(self, name: str, coordinates: tuple, location_data: dict) -> List[Dict[str, Any]]:
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
            location['coordinates'] = ",".join(coordinates)
            weather_data.append(location)

        return weather_data
