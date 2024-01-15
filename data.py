import pandas as pd
import csv
import requests
import config



def get_data():
    url = "https://soccer-football-info.p.rapidapi.com/live/basic/"

    querystring = {"l":"en_US","e":"no"}
    headers = {
        "X-RapidAPI-Key": config.api_key,
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

def create_features(data):
    df = pd.DataFrame(data)


    #expand json data from teamA column to dataframe
    df_teamA = pd.json_normalize(df['teamA'])

    df_teamB = pd.json_normalize(df['teamB'])


    df_teamA = df_teamA.add_suffix('_teamA')
    df_teamB = df_teamB.add_suffix('_teamB')


    #add df_teamA and df_teamB to df_transformed
    df_transformed = pd.concat([df, df_teamA, df_teamB], axis=1)
    #delete teamA and teamB and odds columns
    df_transformed = df_transformed.drop(['teamA', 'teamB'], axis=1)
    #keep only timer > 50:00
    df_transformed = df_transformed[df_transformed['timer'] > '50:00']


    #reset index
    df_transformed = df_transformed.reset_index(drop=True)
    #replace None with 0
    df_transformed = df_transformed.fillna(0)
    #shoots total
    df_transformed['stats.shoots_total'] = df_transformed['stats.shoots.t_teamA'].astype(int) + df_transformed['stats.shoots.t_teamB'].astype(int)
    #on target shoots total
    df_transformed['stats.shoots_on_total'] = df_transformed['stats.shoots.on_teamA'].astype(int) + df_transformed['stats.shoots.on_teamB'].astype(int)
    #off target shoots total
    df_transformed['stats.shoots_off_total'] = df_transformed['stats.shoots.off_teamA'].astype(int) + df_transformed['stats.shoots.off_teamB'].astype(int)
    #if shoots total is 0, then add 1 to avoid division by zero
    df_transformed['stats.shoots_total'] = df_transformed['stats.shoots_total'].replace(0, 1)

    #calculate on target shoots percentage
    df_transformed['stats.shoots_on_percentage'] = df_transformed['stats.shoots_on_total'] / df_transformed['stats.shoots_total']

    #corners total
    df_transformed['stats.corners_total'] = df_transformed['stats.corners.t_teamA'].astype(int) + df_transformed['stats.corners.t_teamB'].astype(int)

    #red cards total
    df_transformed['stats.red_cards_total'] = df_transformed['stats.fouls.r_c_teamA'].astype(int) + df_transformed['stats.fouls.r_c_teamB'].astype(int)

    #total goals 
    df_transformed['stats.goals_total'] = df_transformed['score.f_teamA'].astype(int) + df_transformed['score.f_teamB'].astype(int)

    features = ['score.f_teamA', 'stats.possession_teamA', 'stats.penalties_teamA',
       'stats.corners.t_teamA', 'stats.substitutions_teamA', 'stats.injuries_teamA',
       'stats.attacks.n_teamA', 'stats.attacks.d_teamA', 'stats.shoots.t_teamA',
       'stats.shoots.on_teamA', 'stats.shoots.off_teamA', 'stats.shoots.g_a_teamA',
       'stats.fouls.t_teamA', 'stats.fouls.y_c_teamA', 'stats.fouls.y_t_r_c_teamA',
       'stats.fouls.r_c_teamA', 'stats.dominance_avg_2_5_teamA',
       'score.f_teamB', 'stats.possession_teamB', 'stats.penalties_teamB',
       'stats.corners.t_teamB', 'stats.substitutions_teamB', 'stats.injuries_teamB',
       'stats.attacks.n_teamB', 'stats.attacks.d_teamB', 'stats.shoots.t_teamB',
       'stats.shoots.on_teamB', 'stats.shoots.off_teamB', 'stats.shoots.g_a_teamB',
       'stats.fouls.t_teamB', 'stats.fouls.y_c_teamB', 'stats.fouls.y_t_r_c_teamB',
       'stats.fouls.r_c_teamB', 'stats.dominance_avg_2_5_teamB',
       'stats.shoots_total', 'stats.shoots_on_total', 'stats.shoots_off_total',
       'stats.shoots_on_percentage', 'stats.corners_total', 'stats.red_cards_total',
       'stats.goals_total']

    
    df_transformed= df_transformed[features]
    
    df_transformed.columns = ['goal_teamA', 'possession_teamA', 'penalties_teamA', 'corners_teamA',
       'substitutions_teamA', 'injuries_teamA', 'attacks.n_teamA',
       'attacks.d_teamA', 'shoots.t_teamA', 'shoots.on_teamA',
       'shoots.off_teamA', 'shoots.g_a_teamA', 'fouls.t_teamA',
       'fouls.y_c_teamA', 'fouls.y_t_r_c_teamA', 'fouls.r_c_teamA',
       'dominance.avg_2_5_teamA', 'goal_teamB', 'possession_teamB',
       'penalties_teamB', 'corners_teamB', 'substitutions_teamB',
       'injuries_teamB', 'attacks.n_teamB', 'attacks.d_teamB',
       'shoots.t_teamB', 'shoots.on_teamB', 'shoots.off_teamB',
       'shoots.g_a_teamB', 'fouls.t_teamB', 'fouls.y_c_teamB',
       'fouls.y_t_r_c_teamB', 'fouls.r_c_teamB', 'dominance.avg_2_5_teamB',
       'shoots_total', 'shoots_on_total', 'shoots_off_total',
       'shoots_on_percentage', 'corners_total', 'red_cards_total',
       'goals_total']

    return df_transformed
