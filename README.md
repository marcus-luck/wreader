# wreader
This project intend to give a simple package to receive hourly data for a given coordinate, returning a list of dictionaries with 24h weather data from DarkSky API.

### Information

The package returns a list of dictionaries with the following keys:
* 'predicted_rain'
* 'prediction_of_perspiration'
* 'temperature'
* 'dew_point'
* 'mslp'
* 'humidity'
* 'fctcode'
* 'wind_direction_degrees'
* 'wind_direction'
* 'wind_speed'
* 'uv_index'
* 'icon_url'
* 'isodate'
* 'nowtime'

As of v 0.3 it also returns the following metric values:
* 'predicted_rain_metric'
* 'temperature_metric'
* 'dew_point_metric'
* 'mslp_metric'
* 'wind_speed_metric'

As of v 0.4 the wunderground API is replaced with DarkSky. Wunderground is deprecating their API and it is as of december 2018 no longer available.


### Using


Import the package

```
from wreader import WReader
```

Use api key from wunderground.

```
wr = WReader('api key')
```

Input coordinate, output dictionary.

```
output = wr.get_location_data("21.255220,-157.806872")
```

input dictinary of {locations: coordinates}. Output list of dictionaries.

```
locations = {"}
output = wr.get_all_locations_data(locations)
```

### License

This project is licensed under the MIT License
