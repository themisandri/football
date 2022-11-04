import pandas as pd
import csv
import requests


def get_data():
    url = "https://soccer-football-info.p.rapidapi.com/live/basic/"

    querystring = {"l":"en_US","e":"no"}

    headers = {
        "X-RapidAPI-Key": "ee15e87846mshadd7763b720883fp18db94jsn36d2690f3a98",
        "X-RapidAPI-Host": "soccer-football-info.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['result']

    return data

def transform_data(data):
    df = pd.DataFrame(data)

    #expand json data from teamA column to dataframe
    df_teamA = pd.json_normalize(df['teamA'])
    df_teamB = pd.json_normalize(df['teamB'])

    df_teamA = df_teamA.add_suffix('_teamA')
    df_teamB = df_teamB.add_suffix('_teamB')

    df = pd.concat([df, df_teamA['name_teamA']], axis=1)
    df = pd.concat([df, df_teamB['name_teamB']], axis=1)

    #connect teamA dataframe to main dataframe
    df = pd.concat([df, df_teamA['stats.attacks.n_teamA']], axis=1)
    df = pd.concat([df, df_teamA['stats.attacks.d_teamA']], axis=1)
    df = pd.concat([df, df_teamB['stats.attacks.n_teamB']], axis=1)
    df = pd.concat([df, df_teamB['stats.attacks.d_teamB']], axis=1)

    df = pd.concat([df, df_teamA['stats.shoots.t_teamA']], axis=1)
    df = pd.concat([df, df_teamB['stats.shoots.t_teamB']], axis=1)

    #delete row where timer is 0
    df = df[df['timer'] != "00:00"]

    #reset index
    df = df.reset_index(drop=True)

    #add shoots team A and team B
    df['shoots_total'] = df['stats.shoots.t_teamA'].astype(int) + df['stats.shoots.t_teamB'].astype(int)

    return df
