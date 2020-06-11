import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_row', 111)
pd.set_option('display.max_column', 111)

df = pd.read_csv('data/ligue1_0919.csv').drop('Unnamed: 0', axis = 1)

df.drop('Div', axis = 1, inplace = True)

#On drop les lignes avec des NaN

df.drop([2985,818,931], inplace = True)

dates1 = df.Date.iloc[0:379].str.split('-')

dates2 = df.Date.iloc[380:].str.split('/')

#Colonnes Year, Month et Day

#Year
years1 = dates1.apply(lambda x: x[0])

dictyears = {}
for year in list(range(10,19)):
    key = str(year)
    value = '20'+str(year)
    dictyears.update({key :value})

years2 = dates2.apply(lambda x : x[-1]).replace(dictyears)

years = pd.concat([years1,years2])

#Month
month1 = dates1.apply(lambda x : x[1])
month2 = dates2.apply(lambda x : x[1])

months = pd.concat([month1, month2])

#Day 
days1 = dates1.apply(lambda x : x[-1])
days2 = dates2.apply(lambda x : x[0])

days = pd.concat([days1,days2])

df['Year'] = years
df['Month'] = months
df['Day'] = days

df.drop('Date', axis = 1, inplace = True)

#How many matches by team 

teams = df['HomeTeam'].unique()

matches_played = pd.DataFrame(index = teams, columns = ['Matches Played'])


for team in teams:
    x1 = df[df['HomeTeam'] == team]
    x2 = df[df['AwayTeam'] == team]
    xsum = x1.shape[0] + x2.shape[0]
    matches_played.loc[team, "Matches Played"] = xsum

matches_played = matches_played.apply(pd.to_numeric)
    
#Home wins, away wins, home losses, away losses, home draws, away losses

columns = ['home_wins', 'home_losses', 'home_draws', 'away_wins', 'away_losses', "away_draws",
           'half_home_wins','half_home_losses', 'half_home_draws',
           'half_away_wins', 'half_away_losses', 'half_away_draws']

df1 = pd.DataFrame(index = teams, columns = columns)


for team in teams:
    x1 = df[df['HomeTeam'] == team]
    x2 = df[df['AwayTeam'] == team]
    
    df1.loc[team, 'home_wins'] = x1[x1['Full Time Result'] == "H"].shape[0]
    df1.loc[team, 'home_losses'] = x1[x1['Full Time Result'] == "A"].shape[0]
    df1.loc[team, 'home_draws'] = x1[x1['Full Time Result'] == "D"].shape[0]
    df1.loc[team, 'away_wins'] = x2[x2['Full Time Result'] == 'A'].shape[0]
    df1.loc[team, 'away_losses'] = x2[x2['Full Time Result'] == 'H'].shape[0]
    df1.loc[team, 'away_draws'] = x2[x2['Full Time Result'] == "D"].shape[0]
    


df1 = df1.apply(pd.to_numeric)


df1 = df1.merge(matches_played, left_index = True, right_index = True, how = 'left')

#adding total wins, total losses and total draws

df1['total_wins'] = df1['home_wins'] + df1['away_wins']
df1['total_losses'] = df1['home_losses'] + df1['away_losses']
df1['total_draws'] = df1['home_draws'] + df1['away_draws']

#% wins, % losses, % draws
df1['% wins'] = 100*df1['total_wins']/df1['Matches Played']
df1['% losses'] = 100*df1['total_losses']/df1['Matches Played']
df1['% draws'] = 100*df1['total_draws']/df1['Matches Played']


#Same thing but with half time results

for team in teams:
    x1 = df[df['HomeTeam'] == team]
    x2 = df[df['AwayTeam'] == team]
    
    df1.loc[team, 'half_home_wins'] = x1[x1['Half Time Result'] == "H"].shape[0]
    df1.loc[team, 'half_home_losses'] = x1[x1['Half Time Result'] == "A"].shape[0]
    df1.loc[team, 'half_home_draws'] = x1[x1['Half Time Result'] == "D"].shape[0]
    df1.loc[team, 'half_away_wins'] = x2[x2['Half Time Result'] == 'A'].shape[0]
    df1.loc[team, 'half_away_losses'] = x2[x2['Half Time Result'] == 'H'].shape[0]
    df1.loc[team, 'half_away_draws'] = x2[x2['Half Time Result'] == "D"].shape[0]
    
df1['half_total_wins'] = df1['half_home_wins'] + df1['half_away_wins']
df1['half_total_losses'] = df1['half_home_losses'] + df1['half_away_losses']
df1['half_total_draws'] = df1['half_home_draws'] + df1['half_away_draws']

#% wins, % losses, % draws
df1['% half wins'] = 100*df1['half_total_wins']/df1['Matches Played']
df1['% half losses'] = 100*df1['half_total_losses']/df1['Matches Played']
df1['% half draws'] = 100*df1['half_total_draws']/df1['Matches Played']

#Regarding the rest of the columns, we want : the total at home, away, the mean by match for every team

df.columns 
cols_home = ['Full Time Home Team Goals', 'Half Time Home Team Goals', 
             'Home Team Shots', 'Home Team Shots on Target',
             'Home Team Fouls Committed', 'Home Team Corners',
             'Home Team Yellow Cards','Home Team Red Cards'] 

cols_away = ['Full Time Away Team Goals','Half Time Away Team Goals',
             'Away Team Shots', 'Away Team Shots on Target',
             'Away Team Fouls Committed','Away Team Corners',
             'Away Team Yellow Cards', 'Away Team Red Cards']

#Home
for col in cols_home:

        ft1 = 'Total ' + col
        ft2 = col + ' mean'
        df1[ft1] = float('NaN')
        df1[ft2] = float("NaN")
        for team in teams:
            x1 = df[df['HomeTeam'] == team]
            df1.loc[team, ft1] = x1[col].sum()
            df1.loc[team, ft2] = x1[col].mean()
    
#Away 
for col in cols_away:

        ft1 = 'Total ' + col
        ft2 = col + ' mean'
        df1[ft1] = float('NaN')
        df1[ft2] = float("NaN")
        for team in teams:
            x1 = df[df['AwayTeam'] == team]
            df1.loc[team, ft1] = x1[col].sum()
            df1.loc[team, ft2] = x1[col].mean()

df_test = pd.DataFrame(index = [1], columns=['HomeTeam', 'AwayTeam'])

df_test.loc[1,'HomeTeam'] = 'Lyon'
df_test.loc[1,'AwayTeam'] = 'Grenoble'



home = ['home_wins', 'home_losses', 'home_draws', 'half_home_wins', 'half_home_losses', 'half_home_draws',
       'Matches Played', 'total_wins', 'total_losses', 'total_draws', '% wins',
       '% losses', '% draws', 'half_total_wins', 'half_total_losses',
       'half_total_draws', '% half wins', '% half losses', '% half draws',
       'Total Full Time Home Team Goals', 'Full Time Home Team Goals mean',
       'Total Half Time Home Team Goals', 'Half Time Home Team Goals mean',
       'Total Home Team Shots', 'Home Team Shots mean',
       'Total Home Team Shots on Target', 'Home Team Shots on Target mean',
       'Total Home Team Fouls Committed', 'Home Team Fouls Committed mean',
       'Total Home Team Corners', 'Home Team Corners mean',
       'Total Home Team Yellow Cards', 'Home Team Yellow Cards mean',
       'Total Home Team Red Cards', 'Home Team Red Cards mean']

away = ['away_wins', 'away_losses',
       'away_draws', 'half_away_wins', 'half_away_losses', 'half_away_draws',
       'Matches Played', 'total_wins', 'total_losses', 'total_draws', '% wins',
       '% losses', '% draws', 'half_total_wins', 'half_total_losses',
       'half_total_draws', '% half wins', '% half losses', '% half draws',
       'Total Full Time Away Team Goals', 'Full Time Away Team Goals mean',
       'Total Half Time Away Team Goals', 'Half Time Away Team Goals mean',
       'Total Away Team Shots', 'Away Team Shots mean',
       'Total Away Team Shots on Target', 'Away Team Shots on Target mean',
       'Total Away Team Fouls Committed', 'Away Team Fouls Committed mean',
       'Total Away Team Corners', 'Away Team Corners mean',
       'Total Away Team Yellow Cards', 'Away Team Yellow Cards mean',
       'Total Away Team Red Cards', 'Away Team Red Cards mean']

#Merging the news features with the original dataframe

df1_home = df1[home]
df1_away = df1[away]

df_final = df.copy()

df_final = df_final.merge(df1_home, right_index = True, left_on='HomeTeam', how='right')
df_final = df_final.merge(df1_away, right_index = True, left_on='AwayTeam', how='right')

#df_final.reset_index(drop = True, inplace = True)


df_final.to_csv('df_final.csv', index = False)


