import pandas as pd
import requests


class WReader():
    def __init__(api_key, sleep_time = 10):
        self.api_key = api_key
        self.sleep_time = sleep_time


    def set_api_key(api_key):
        """Set  wunderground api_key

        args:
            param1: (str) api_key
        
        """
        self.api_key = api_key


    def _get_location_json(location):
        
        """Get 24h weather data from location

        Args:
            param1: (str) location as XXXX,YYYY

        Returns:
            Json

        """
        

        url = "http://api.wunderground.com/api/%s/hourly/q/%s.json" % (api_key, location)

        response = requests.get(url)

        return response.json()

    def _transform_location_json_to_dataframe(location_data):
        """Return a list containing hour for hour data for selected location
        
        args:
            param1: (str) location as XXXX,YYYY

        Returns:
            Pandas DataFrame with hours as rows and data as columns

        """

        # Go through location json and add relevant data to DataFrame
        for whour in beach['hourly_forecast']:

            # Set time of extraction
            nowtime = datetime.now().isoformat(' ')

            # Create isodate from fcttime
            fcttime = whour['FCTTIME']

            fdate = (fcttime['year'] + 
            '-' + fcttime['mon_padded'] +
            '-' + fcttime['mday_padded'])

            fhour = (fcttime['hour_padded'] + 
            ':' + fcttime['min'])

            weather_data= {'predicted_rain': float(whour['qpf']['english']),
            'prediction_of_perspiration': float(whour['pop']),
            'temperature': float(whour['temp']['english']),
            'dew_point': float(whour['dewpoint']['english']),
            'mslp': float(whour['mslp']['english']),
            'humidity': int(whour['humidity']),
            'fctcode': (int(whour['fctcode'])),
            'wind_direction_degrees': int(whour['wdir']['degrees']),
            'wind_direction': str(whour['wdir']['dir']),
            'wind_speed': float(whour['wspd']['english']),
            'uv_index': int(whour['uvi']),
            'icon_url': str(whour['icon_url']),
            'isodate': str(fdate + 
                    ' ' + fhour + 
                    ':00.00000')
            }

        return pd.DataFrame(weather_data)


    def get_location_data(location):
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
    
        return location_dataframe

    def get_all_locations_data(locations):
        """Returns a datatable of 24h, hour by hour weather of all locations
            Intention is to return a pandas DataFrame of with 24 hour datarows per location.
            Columns in DataFrame are the variables from wunderground.

        args: 
            (list) list of location coordinates.

        returns:
            (pandas DataFrame) 24h, Hour by hour weather of all locations
        """
        
        # Define dataframe
        locations_datatable = pf.DataFrame()
        
        # Go through all locations
        for location in locations:

            # Fetch location weather data for the next 24h
            location_json = get_location_json(self.api_key, location.location)

            # Transform location json to DataFrame
            location_datatable = self._transform_location_json_to_dataframe(
                    location_json)

            # Combine locations_dataframes into one dataframe
            all_locations_datatable = all_locations_datatable.concat(location_datatable, ignoew_index=True)

        return locations_datatable
