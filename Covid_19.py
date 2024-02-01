import requests
import re


def covid_19(country_name, country_code):
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"

    querystring = {"country": country_name}

    headers = {
        'x-rapidapi-key': "",#Enter your Rapid Api Covid 19 key here
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    message = re.findall(r'message["]:...', response.text)
    message = message[0][10:]
    if 'OK' in message:
        pass
    else:
        url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"

        querystring = {"country": country_code}

        headers = {
            'x-rapidapi-key': "", #Enter your Rapid Api Covid 19 key here
            'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.text
    recovered = (re.findall(r'recovered.*["]d', response))[0]
    recovered = recovered[11:-3]
    deaths = re.findall(r'deaths.*co', response)[0]
    deaths = deaths[8:-4]
    confirmed = re.findall(r'confirmed.*lastC', response)[0]
    confirmed = confirmed[11:-7]
    location = re.findall(r'location.*', response)[0]
    location = location[11:-3]
    if recovered == '0':
        recovered = 'not known'
    if location == 'Global':
        location = 'the World'
    return "In {}, The total number of confirmed cases is {} the total number of recovered cases is {} and the total number of deaths is {}".format(
        location, confirmed, recovered, deaths)
