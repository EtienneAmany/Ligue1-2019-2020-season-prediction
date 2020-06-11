
df1 = pd.read_csv('data/season-0910_csv.csv')
df2 = pd.read_csv('data/season-1011_csv.csv')
df3 = pd.read_csv('data/season-1112_csv.csv')
df4 = pd.read_csv('data/season-1213_csv.csv')
df5 = pd.read_csv('data/season-1314_csv.csv')
df6 = pd.read_csv('data/season-1415_csv.csv')
df7 = pd.read_csv('data/season-1516_csv.csv')
df8 = pd.read_csv('data/season-1617_csv.csv')
df9 = pd.read_csv('data/season-1718_csv.csv')
df10 = pd.read_csv('data/season-1819_csv.csv')

dfs = [df2, df3, df4, df5, df6, df7, df8, df9, df10]
df = pd.DataFrame(df1)

for dfi in dfs: 
    df = pd.concat([df, dfi])
    

columns = ['Div', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 
           'HTAG', 'HTR','HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY',
           'AY', 'HR', 'AR']

df = df[columns]

df.columns
ColumnsName = {'FTHG': 'Full Time Home Team Goals',
               'FTAG': 'Full Time Away Team Goals',
               'FTR': 'Full Time Result',
               'HTHG' : 'Half Time Home Team Goals',
               'HTAG' : 'Half Time Away Team Goals',
               'HTR': 'Half Time Result',
               'HS': 'Home Team Shots',
               'AS': 'Away Team Shots',
               'HST': 'Home Team Shots on Target',
               'AST' : 'Away Team Shots on Target',
               'HF':'Home Team Fouls Committed',
               'AF':'Away Team Fouls Committed',
               'HC':'Home Team Corners',
               'AC':'Away Team Corners',
               'HY':'Home Team Yellow Cards',
               'AY':'Away Team Yellow Cards',
               'HR':'Home Team Red Cards',
               'AR':'Away Team Red Cards'               
                   }

df = df.rename(ColumnsName, axis = 1)

df.to_csv('ligue1_0919.csv', index = False)

