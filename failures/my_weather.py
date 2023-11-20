import requests
import json

# OpenWeatherMap API: https://openweathermap.org/current

# TODO: Sign up for an API key
OWM_API_KEY = '2ff1db768c9107c7bbb96ebbc015d34b'  # OpenWeatherMap API Key

DEFAULT_ZIP = 90089

def get_weather(zip_code):
    params = {
        'appid': OWM_API_KEY,
        # TODO: referencing the API documentation, add the missing parameters for zip code and units (Fahrenheit)
        'zip': 90089,
        'units': 'imperial'
    }

    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)

    if response.status_code == 200: # Status: OK
        data = response.json()

        # print the json to parse what i need
        # print(json.dumps(data, sort_keys=True, indent=4))

        # TODO: Extract the temperature & humidity from data, and return as a tuple
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        #test types of temp and humidity
        # print(type(temperature), ' ', temperature)
        # print(type(humidity), " ", humidity)
        return (temperature, humidity)

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0

def weather_init():
    zip_code = DEFAULT_ZIP
    temp, hum = get_weather(zip_code)
    
    output = '{:.1f}F, {:>.0f}% humidity'.format(temp, hum)
    print('weather for {}: {}'.format(zip_code, output))

    return output


WEATHER_APP = {
    'name': 'Weather',
    'init': weather_init
}


if __name__ == '__main__':
    weather_init()
