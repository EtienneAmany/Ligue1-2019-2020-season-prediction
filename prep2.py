import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/df_final.csv')



todrop = ['Full Time Home Team Goals','Half Time Result',
       'Full Time Away Team Goals',
       'Half Time Home Team Goals', 'Half Time Away Team Goals',
       'Home Team Shots', 'Away Team Shots', 'Home Team Shots on Target',
       'Away Team Shots on Target', 'Home Team Fouls Committed',
       'Away Team Fouls Committed', 'Home Team Corners', 'Away Team Corners',
       'Home Team Yellow Cards', 'Away Team Yellow Cards',
       'Home Team Red Cards', 'Away Team Red Cards']

df.drop(todrop, axis = 1, inplace = True)


#We want to add a column with the name of the winning team
winners_away =[]
winners_home = []
draws = []

for winner in df['Full Time Result']:
    

    if winner == 'A':
        winners_away.append(df.index[df['Full Time Result'] == winner])
    elif winner == 'H':
        winners_home.append(df.index[df['Full Time Result'] == winner])            
    elif winner == 'D':
        draws.append(df.index[df['Full Time Result'] == winner])  
        
winners_away = winners_away[0]
winners_home = winners_home[0]
draws = draws[0]


