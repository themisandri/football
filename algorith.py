
def algorithm(df):

    matches = []

    for i in range(0, len(df)):
        if df['timer'][i]<="70:00" and df['timer'][i] >= "50:00" and df['shoots_total'][i]>5:
            print(df['name_teamA'][i], "-" ,df['name_teamB'][i], df['timer'][i], df['shoots_total'][i])
            matches.append(df['name_teamA'][i] + " - " + df['name_teamB'][i])
    
    return matches