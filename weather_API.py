#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 18:11:02 2021

@author: jt

Komunikaty wyświetlane w konsoli będą w języku polskim, a funkcje są w j. angielskim.
"""

#import bibliotek

import datetime
import requests
import json
#import bibliotek 2
import json
import numpy as np
import datetime
from statistics import mean

def get_historical_data(downloaded_day):
    '''
    Funkcja pobiera dane z openweathermap dla i-go dnia temu dla Warszawy.
    '''

    API_key = ''
    lat = '52.237049'
    lon = '21.017532'
    dt = str(int(datetime.datetime.utcnow().timestamp())-downloaded_day*3600*24)

    response = requests.get(
        'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat='+lat +
        '&lon='+lon+'&dt='+dt+'&units=metric&appid='+API_key)

    if not response:
        raise Exception('Błąd połączenia')
    else:
        return response

# Poniżej tworzone są listy na których, będzie program pracował.

# temperature_data - [t, T] wszystkie godziny
# transposed_temperature_data - transpozycja
# full_data - wszystkie dane sformatowane jako elementy listy


full_data = list()
temperature_data = list()
for i_day in range(3, 0, -1):
    n_day = get_historical_data(i_day).json()['hourly']
    for i_time in range(24):
        temperature_data.append([n_day[i_time]['dt'],  n_day[i_time]['temp']])
        full_data.append([n_day[i_time]])

transposed_temperature_data = list(zip(*temperature_data))

# Poniżej sprawdzane jest, czy temperatura wzrasta po kolejnym rekordzie.

# temperature_raised - lista z informacją (bool), czy temperatura rośnie, czy nie [list]

temperature_raised = [temp1 < temp2 for temp1, temp2 in zip(
    transposed_temperature_data[1], transposed_temperature_data[1][1:])]


# Poniżej tworzona jest lista rekordów, przy których temperatura wzrasta

# temp_list - lista zawierająca nieprzerwany ciąg wzrostów temperatury
# result - lista zbudowana z temp_list
# active_timestamp - czas w których temperatura wzrastała

result = list()
temp_list = list()
active_timestamps = list()

for i_test in range(len(transposed_temperature_data[1])-1):
    if temperature_raised[i_test] is False:
        temp_list = list()
    else:
        temp_list.append(temperature_data[i_test])
        active_timestamps.append(temperature_data[i_test][0])
        if temperature_raised[i_test+1] is True:
            continue
        else:
            # dodawany jest jeszcze ostatni dzień wzrostu
            temp_list.append(temperature_data[i_test+1])
            # dodawany jest jeszcze ostatni dzień wzrostu
            active_timestamps.append(temperature_data[i_test+1][0])
            result.append(temp_list)

# Poniżej tworzona jest lista z kompletnymi godzinowymi danymi ze źródła
# z tego przedziału.

# full_data_result - lista zawierająca kompletne godzinowe dane ze źródła

full_data_result = list()
for i_full_data in full_data:
    if i_full_data[0]['dt'] in active_timestamps:
        full_data_result.append(i_full_data[0])

# Pomniżej tworzony jest końcowy rekord jako słownik, jako id jest czas rozpoczęcia
# okresu wzrostu w formacie UNIX time.

# result_dict - słownik z wynikime końcowym
# start_point - wykorzystane do podziału pełnych danych źródłowych


result_dict = dict()
start_point = 0
for i_result in result:
    temp_dict = {i_result[0][0]: {
        # jako, że dodany jest 'końcowy' dzień nie wlicza się on do długości okresu wzrostów
        'length': len(i_result) - 1,
        'init_temp': i_result[0][1],
        'end_temp': i_result[-1][1],
        'hourly_data':

        full_data_result[start_point: start_point + len(i_result)]

    }}
    start_point += len(i_result)
    result_dict.update(temp_dict)

with open('json_result.json', 'w') as json_file:
    json.dump(result_dict, json_file)
json_file.close()
######################

json_file = json.load(open('json_result.json',))

# Z pliku źródłowego wyciągane są dane temperatury oraz czasu.

# temperature_full - lista list podzielonych na poszczególne okresy [t, T]

temperature_full = list()
for value in json_file.values():
    temperature = list()
    for h_data in value['hourly_data']:
        temperature.append([h_data['dt'], h_data['temp']])
    temperature_full.append(temperature)

# Poniżej przeprawdzane są obliczenia i szukana jest wartość największego
# godzinowego wzrostu temperatury, okresu w jakim ten wzrost się odbył
# oraz czasu jego rozpoczęcia.

# max_temperature_change - [czas rozpoczęcia okresu wzrostu, wartość wzrostu temperatury] //mogło by być jako 2 wartości
# timestamp - moment skoku temperatury unix time
# temperature_change - [godzina, wartość wzrostu]

max_temperature_change = [float(), float()]
timestamp = int()

for i_temp in temperature_full:
    transposed_temperature = list(zip(*i_temp))
    temperature_change = np.array([[time, round(temp2 - temp1, 2)] for time, temp1, temp2 in zip(
        transposed_temperature[0], transposed_temperature[1], transposed_temperature[1][1:])], dtype=float)
    # sprawdzane jest w tym miescu czy wartość wzrostu temperatury jest największa
    if float(max(temperature_change[:, 1])) > max_temperature_change[1]:
        max_temperature_change[1], max_temperature_change[0] = float(max(
            temperature_change[:, 1])), int(i_temp[0][0])  # okresy są identifikowane czasem początkowym

        # w tym miejscu wyliczane jest moment wzrostu
        # (nie jest to najbardziej optymalne rozwiązanie, lecz przy takiej ilości danych nie stanowi to problemu)
        n_order = 0
        for inner in temperature_change:
            if inner[1] == max_temperature_change[1]:
                timestamp = (int(inner[0]))
                n_order_list = n_order
            n_order += 1

# Wyniki są formatowane do zadanych formatów (czas UTC)

initial_time = datetime.datetime.utcfromtimestamp(max_temperature_change[0])
end_time = initial_time + \
    datetime.timedelta(
        hours=json_file[str(max_temperature_change[0])]['length'])
jump_time = datetime.datetime.utcfromtimestamp(timestamp)
initial_temperature = json_file[str(
    max_temperature_change[0])]['hourly_data'][n_order_list]['temp']

# Obliczenia związane z średnią wilgotnością i ciśnieniem w okresie występowania rekordowego wzrostu temperatury

humidity = list()
pressure = list()
for p_h_value in json_file[str(max_temperature_change[0])]['hourly_data']:
    pressure.append(p_h_value['pressure'])
    humidity.append(p_h_value['humidity'])

avg_humidity, avg_pressure = round(mean(humidity), 2), round(mean(pressure), 2)

print('Początek okresu wzrostu z najwyższym godzinowym skokiem temperatury:', initial_time)
print('Koniec okresu wzrostu z najwyższym godzinowym skokiem temperatury: ', end_time)
print('Godzina początkowa najwyższego skoku temperatury:', jump_time)
print('Wartość temperatury przed skokiem:', initial_temperature, 'st. C')
print('Wielkość skoku:', max_temperature_change[1], 'st. C')
print('Średnia wilgotność w powyższym okresie:', avg_humidity)
print('Średnie ciśniene w powyższym okresie', avg_pressure)
