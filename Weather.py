import requests
import re
import datefinder


def weather_data(query):
    res = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?' + query + '&APPID=c3bb2b1eca7e0fd5b10e844852c8e6c3&units=metric')
    return res.json()


def print_weather(result, city):
    a = ["{}'s temperature: {}°C ".format(city, result['main']['temp']),
         "Wind speed: {} m/s".format(result['wind']['speed']),
         "Description: {}".format(result['weather'][0]['description']),
         "Weather: {}".format(result['weather'][0]['main'])]
    a = tuple(a)
    return a

def greeting():
    query = 'q=' + 'kolkata'
    w_data = weather_data(query)
    a = "The weather outside is {} Celsius. It will be a {} weather today".format(w_data['main']['temp'], w_data['weather'][0]['main']+"y")
    return a


def weather_forecast(lat, long):
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"

    querystring = {"lat": str(lat), "lon": str(long)}

    headers = {
        'x-rapidapi-key': "c267e5172fmsh5d38b667a7c2f95p17d7eajsn8b1e16574ba4",
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    k = {'date': [], 'temp': re.findall(r'temp["]:[\d]*\.[\d]*', response.text)}
    for count, i in enumerate(k['temp']):
        k['temp'][count] = i[6:]
    k['date'] = re.findall(r'["]valid_date["]:["]..........', response.text)
    for count, i in enumerate(k['date']):
        k['date'][count] = i[14:]
        for i in datefinder.find_dates(k['date'][count]):
            k['date'][count] = i
    return k


def main(city):
    try:
        query = 'q=' + city
        w_data = weather_data(query)
        return print_weather(w_data, city)
    except:
        print('City name not found...')
