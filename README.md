# wreader
This project intend to give a simple package to receive hourly data for a given coordinate, returning a pandas DataFrame with 24h weather data from Wunderground.

### Information

The package returns a dataframe with the following columns:
'predicted_rain'
'prediction_of_perspiration'
'temperature'
'dew_point'
'mslp'
'humidity'
'fctcode'
'wind_direction_degrees'
'wind_direction'
'wind_speed'
'uv_index'
'icon_url'
'isodate'
'nowtime'

### Using


Import the package

```
from wreader import WReader
```

Use api key from wunderground.

```
wr = WReader('api key')
```

Input coordinate, output pandas DataFrame.

```
output = wr.get_location_data("21.255220,-157.806872")
```

### License

This project is licensed under the MIT License
