from queue import Empty
import pandas as pd
import requests
import json
from sodapy import Socrata
from datetime import datetime

import xml.etree.ElementTree as ET
from pandas.io.json import json_normalize
# dict = {'station_data_for_date': WeatherStationsForDate(), 'current_date': datetime.min}
'''
Abstracted service method to get basic weather data for temperature and return a data frame that can be written to a CSV file.
'''
# def get_basic_weather(file_name):
#     return Temperature(file_name).get_data_set()

'''
This method checks to see if this is the first invocation of the method. If so, the current_date is set to the parsed date.
''' 
def check_date(current_date, parsed_date):
    if dict['current_date'].date() == datetime.min.date():
        dict['current_date'] = parsed_date
        return parsed_date
    return current_date

'''
This method writes each station's minimum, maximum, first, and last temperatures for each date to the console in order specified by the project requirements.
[Station Name, Date, Min Temp, Max Temp, First Temp, Last Temp]
'''    
# def write_to_console(writer):
#     station_data = dict['station_data_for_date'].station_data
#     for station in station_data.keys():
#         key_dict = station_data[station]
#         date = key_dict.date_min.strftime('%m/%d/%Y')
#         writer.write("%s,%s,%s,%s,%s,%s\n" % (station, date, key_dict.min_temp, key_dict.max_temp, key_dict.first_temp, key_dict.last_temp))
      

'''
This method parses the date input as a string into proper datetime format.
'''    
def parse_date(split_line):
    date = split_line[1]
    return datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
    
  
'''
This method pulls all player data. Sleeper recommends invoking only once daily to update ID's/Active status for players across the league. 
See https://docs.sleeper.app/#players for info on this resource.
'''
def get_all_players():
    url = 'https://api.sleeper.app/v1/players/nfl'
    response = requests.get(url).json()
    df1 = pd.DataFrame(response)
    curr_date = datetime.now().strftime('%m_%d_%Y')
    # df1.to_json('data/sleeper-json-' + datetime.today.strftime('%d-%m-%Y') + '.json')
    df1.to_json('data/sleeper-json-' + curr_date + '.json')
    df = pd.read_json('data/sleeper-json-' + curr_date + '.json')
    rows = pd.DataFrame()
    columns = list(df)
    print(columns)
    for id in columns: # columns = list(df)
        row = pd.DataFrame(df[id]).transpose()
        rows = pd.concat([rows, row])
        print(rows)
    return df
   
   
'''
This method pulls all player data. Sleeper recommends invoking only once daily to update ID's/Active status for players across the league. 
See https://docs.sleeper.app/#players for info on this resource.
'''
def get_from_json():
    with open('data/sleeper-json.json') as data_file:    
        data = json.load(data_file) 
    df = pd.DataFrame(pd.read_json(data, lines=True))
    # dfNest = pd.DataFrame(pd.read_json(df[1]))
    
    df.to_csv('/c/Users/andre/Desktop/test.csv')
    print(df)
    return df
 
FIELDS = ['list of keys I care about']
def clean_data(data):
    table = pd.DataFrame()
    for i in range(len(data) - 1):
        df = pd.json_normalize(data[i + 1])
        # df = df[FIELDS]
        table = table.append(df)
    return table    
 
'''
This method is effectively the 'controller' for the streaming feature of the application. This will read and discard the first line of input which represents the headers.
Afterwards, it will write the console headers before reading each line of input and processing it. Finally, it writes the last date to the console as it is still cached.
'''   
def process_stream(reader, writer):
    df = get_all_players()
    df.to_csv('data/sleeper-players_' + datetime.now().strftime('%m_%d_%Y') + '.csv', index=False)

