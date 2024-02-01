import pandas as pd


def city(sentence):
    dataset = pd.read_csv('world-cities_csv.csv')
    x = dataset.iloc[:, 0]
    k = []
    s = sentence.split()
    f = 0
    for i in x:
        for b in s:
            if i.lower() == b.lower():
                k = i
                f = 1
        if f == 1:
            break

    return k


def lat_long(sentence):
    dataset = pd.read_csv('worldcities.csv')
    x = dataset.iloc[:, 0]
    f = 0
    lat = 0
    long = 0
    c = int
    for count, i in enumerate(x):
        if i.lower() in sentence.lower():
            cit = i
            c = count
            f = 1
            break
    if f == 1:
        lat = dataset.iloc[c]['lat']
        long = dataset.iloc[c]['lng']
    return cit, lat, long


def country(sentence):
    dataset = pd.read_csv('countries.csv')
    x = dataset.iloc[:, 0]
    y = dataset.iloc[:, -1]
    y = list(y)
    x = list(x)
    country_code = []
    country_name = []
    f = 0
    for i in x:
        if i.lower() in sentence.lower():
            country_name = i
            j = x.index(country_name)
            country_code = y[j]
            f = 1
            break
    if f == 0:
        s = sentence.split()
        f = 0
        for i in y:
            for b in s:
                if i == b:
                    country_code = i
                    j = y.index(i)
                    country_name = x[j]
                    f = 1
            if f == 1:
                break
    country_name = str(country_name)
    country_name = country_name.replace('[', '')
    country_name = country_name.replace(']', '')
    country_code = str(country_code)
    country_code = country_code.replace('[', '')
    country_code = country_code.replace(']', '')
    return country_name, country_code
