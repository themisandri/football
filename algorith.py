import pandas as ps


def algorithm(df):

    matches = []

    for i in range(0, len(df)):
        if df['timer'][i]<="75:00" and df['timer'][i] >= "55:00" \
        and df['shoots_total'][i]>22 and df['shoots_on_percentage'][i]>0.35 \
        and df['corners_total'][i]>=7 and df['red_cards_total'][i]==0:
            print(df['name_teamA'][i], "-" ,df['name_teamB'][i], df['timer'][i], df['shoots_total'][i])
            matches.append(df['name_teamA'][i] + " - " + df['name_teamB'][i])
    
    return matches