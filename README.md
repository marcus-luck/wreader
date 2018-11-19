# wreader
This project intend to give a simple package to receive hourly data for a given coordinate, returning a list of dictionaries with 24h weather data from DarkSky API.

### Information

The package returns a list of dictionaries with the following keys:
*.'time'
*.'summary'
*.'icon'
*.'precipIntensity'
*.'precipProbability'
*.'temperature'
*.'apparentTemperature'
*.'dewPoint'
*.'humidity'
*.'pressure'
*.'windSpeed'
*.'windGust'
*.'windBearing'
*.'cloudCover'
*.'uvIndex'
*.'visibility'
*.'ozone'

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

input dictinary of {locations: coordinates}. Output list of dictionaries.

```
locations = {"Waikiki": "21.255220,-157.806872", "Sunset Beach": "21.255220,-157.806872"}
output = wr.get_all_locations_data(locations)
```


### License

This project is licensed under the MIT License
