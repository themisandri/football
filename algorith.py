import pandas as pd
import pickle



def algorithm(df):

    matches = []

    for i in range(0, len(df)):
        if df['timer'][i]<="75:00" and df['timer'][i] >= "55:00" \
        and df['shoots_total'][i]>22 and df['shoots_on_percentage'][i]>0.35 \
        and df['corners_total'][i]>=7 and df['red_cards_total'][i]==0:
            print(df['name_teamA'][i], "-" ,df['name_teamB'][i], df['timer'][i], df['shoots_total'][i])
            matches.append(df['name_teamA'][i] + " - " + df['name_teamB'][i])
    
    return matches

def model_predict(data,transformed_data):
    df = pd.DataFrame(data)
    transform_data = transformed_data
    #expand json data from teamA column to dataframe
    df_teamA = pd.json_normalize(df['teamA'])

    df_teamB = pd.json_normalize(df['teamB'])


    df_teamA = df_teamA.add_suffix('_teamA')
    df_teamB = df_teamB.add_suffix('_teamB')


    #add df_teamA and df_teamB to df_transformed
    df_names = pd.concat([df, df_teamA, df_teamB], axis=1)
    #delete teamA and teamB and odds columns
    df_names = df_names.drop(['teamA', 'teamB'], axis=1)
    #keep only timer > 50:00
    df_names = df_names[df_names['timer'] > '50:00']
    
    df_names= df_names[['timer','name_teamA','score.f_teamA','score.f_teamB','name_teamB']]

    filename = 'finalized_model.sav'
    
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))

    df_names['prediction'] = loaded_model.predict(transform_data)
    df_names.reset_index(drop=True, inplace=True)
    matches = []

    for i in range(0, len(df_names)):
        if df_names['prediction'][i]==1:
            print(df_names['name_teamA'][i], "-" ,df_names['name_teamB'][i], df_names['timer'][i])
            matches.append(df_names['name_teamA'][i] + " - " + df_names['name_teamB'][i])
    
    match_to_bet = df_names[df_names['prediction'] == 1]

    return matches, match_to_bet