import pandas as pd
import numpy as np


#Df source : https://raw.githubusercontent.com/footballcsv/france/master/2019-20/fr.1.csv

df = pd.read_csv('data/season-1920.csv', encoding = "ISO-8859-1").drop('Round', axis = 1)

df_team = pd.read_csv('data/df_final.csv')

#Date + Cleaning team names 
df['Date'] = (df['Date'].apply(lambda x : x.replace(x[:5], '' )).apply(lambda x: x.replace(x[-5:], ''))
                                                                       .apply(lambda x: x.strip()))
df['Date'] = pd.to_datetime(df['Date'])

df['Team 1'] = (df['Team 1']).apply(lambda x: x.replace(x[-4:], '')).apply(lambda x: x.strip())

df['Team 2'] = (df['Team 2']).apply(lambda x: x.replace(x[-4:], '')).apply(lambda x: x.strip())



#Replacing the names by the ones used in the df

df['Team 1'].unique()

sorted(df_team['HomeTeam'].unique())

sorted(df['Team 1'].unique())

dict_team = {'AS Monaco': 'Monaco', 'Olympique de Marseille': 'Marseille', 'Angers SCO': 'Angers',
       'Stade Brestois 29': 'Brest', 'Dijon FCO':'Dijon', 'Montpellier HSC': 'Montpellier', 'OGC Nice':'Nice',
       'Lille OSC':'Lille', 'RC Strasbourg':'Strasbourg', 'Paris Saint-Germain': 'Paris SG',
       'Olympique Lyonnais':'Lyon', 'FC Nantes':'Nantes', 'Amiens SC':'Amiens',
       'Girondins de Bordeaux':'Bordeaux', 'FC Metz':'Metz', 'Nîmes Olympique':'Nimes',
       'Toulouse FC':'Toulouse', 'AS Saint-Étienne':'St Etienne', 'Stade de Reims':'Reims',
       'Stade Rennais FC':'Rennes'}

df['Team 1'] = df['Team 1'].replace(dict_team)
df['Team 2'] = df['Team 2'].replace(dict_team)

#Extracting month and day 

df['Year'] = 2019

#Month
df['Month'] = pd.DatetimeIndex(df['Date']).month

#Integrating the data of the df 
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

df_home = pd.read_csv('data/df1_home.csv').set_index('Unnamed: 0')
df_away = pd.read_csv('data/df1_away.csv').set_index('Unnamed: 0')

calendar = df.copy()

df = df.merge(df_home, right_index = True, left_on='Team 1', how='right')
df = df.merge(df_away, right_index = True, left_on='Team 2', how='right')


df.dropna(inplace = True)
df.drop(['FT', 'HT'], axis= 1, inplace = True)
df = df.rename(columns={'Team 1': 'HomeTeam', "Team 2": 'AwayTeam'})

df.to_csv('data/to_predict.csv', index= False)
