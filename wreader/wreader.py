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


    def get_location_json(location):
        
        """Get 24h weather data from location

        Args:
            param1: (str) location as XXXX,YYYY

        Returns:
            Json

        """
        

        url = "http://api.wunderground.com/api/%s/hourly/q/%s.json" % (api_key, location)

        response = requests.get(url)

        return response.json()

    def transform_location_json_to_dataframe(location):
        """Return a list containing hour for hour data for selected location
        
        args:
            param1: (str) location as XXXX,YYYY

        Returns:
            Pandas DataFrame with hours as rows and data as columns

        """
        
        #print beach
        beach_name = location.name

        beach_id = location.location_id

        # Go through hours
        for whour in beach['hourly_forecast']:

            location_id = int(beach_id)

            nowtime = datetime.now().isoformat(' ')


            predicted_rain = float(whour['qpf']['english'])
            prediction_of_perspiration = float(whour['pop'])
            temperature = float(whour['temp']['english'])
            dew_point = float(whour['dewpoint']['english'])
            mslp = float(whour['mslp']['english'])
            humidity = int(whour['humidity'])

            fctcode = (int(whour['fctcode']))

            wind_direction_degrees = int(whour['wdir']['degrees'])
            wind_direction = str(whour['wdir']['dir'])
            wind_speed = float(whour['wspd']['english'])
            #uv_index = int(whour['uvi'])
            icon_url = str(whour['icon_url'])

            fcttime = whour['FCTTIME']
            date = fcttime['year'] + '-' + fcttime['mon_padded'] +
            '-' + fcttime['mday_padded']
            hour = fcttime['hour_padded'] + ':' + fcttime['min']
            isodate = date + ' ' + hour + ':00.00000'
            isodate = str(isodate)

            app.logger.info("Data gathered, prepare to save")


    def get_all_location_data():
        '''
        Returns a datatable of all locations
        '''
        
        # Get all location from database
        locations = get_locations()
        
        # define dataframe
        locations_datatable = pf.DataFrame()
        
        # Go through all locations
        for location in locations:

            # get the api_key
            api_key = get_api_key()

            # fetch location weather data for the next 24h
            location_json = get_location_json(api_key, location.location)

            location_datatable = transform_location_json_to_dataframe(
                    location_json)

            # Combine locations_dataframes into one dataframe
            locations = locations.concat(location_datatable, ignoew_index=True)

