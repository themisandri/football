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

    #on target shoots
    df = pd.concat([df, df_teamA['stats.shoots.on_teamA']], axis=1)
    df = pd.concat([df, df_teamB['stats.shoots.on_teamB']], axis=1)

    #total corners
    df = pd.concat([df, df_teamA['stats.corners.t_teamA']], axis=1)
    df = pd.concat([df, df_teamB['stats.corners.t_teamB']], axis=1)

    #red cards
    df = pd.concat([df, df_teamA['stats.fouls.r_c_teamA']], axis=1)
    df = pd.concat([df, df_teamB['stats.fouls.r_c_teamB']], axis=1)


    #delete row where timer is 0
    df = df[df['timer'] != "00:00"]

    #reset index
    df = df.reset_index(drop=True)

    #add shoots team A and team B
    df['shoots_total'] = df['stats.shoots.t_teamA'].astype(int) + df['stats.shoots.t_teamB'].astype(int)

    #if shoots on is none, then set to 0
    df['stats.shoots.on_teamA'] = df['stats.shoots.on_teamA'].fillna(0)
    df['stats.shoots.on_teamB'] = df['stats.shoots.on_teamB'].fillna(0)

    #on target shoots total
    df['shoots_on_total'] = df['stats.shoots.on_teamA'].astype(int) + df['stats.shoots.on_teamB'].astype(int)

    #if shoots total is 0, then add 1 to avoid division by zero
    df['shoots_total'] = df['shoots_total'].replace(0, 1)

    #calculate on target shoots percentage
    df['shoots_on_percentage'] = df['shoots_on_total'] / df['shoots_total']

    #calculate corners total
    df['corners_total'] = df['stats.corners.t_teamA'].astype(int) + df['stats.corners.t_teamB'].astype(int)

    #calculate red cards total
    df['red_cards_total'] = df['stats.fouls.r_c_teamA'].astype(int) + df['stats.fouls.r_c_teamB'].astype(int)

    #delete columns
    df = df.drop(['dominance_index','teamA','teamB'], axis=1)

    return df
