import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

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
#Encoding Team Names
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
df['AwayTeam_encoded'] = le.fit_transform(df['AwayTeam'])
df['HomeTeam_encoded'] = le.transform(df['HomeTeam'])

df.drop(['AwayTeam', 'HomeTeam'], axis = 1, inplace = True)

df.dropna(inplace = True)

trainset, testset = train_test_split(df)

#Preping the df 
def prep(df):
    X = df.drop('Full Time Result', axis = 1)
    y= df['Full Time Result']
    
    return X,y

X_train, y_train = prep(trainset)
X_test, y_test = prep(testset)

"""
#Scalling 
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""
#Model evaluation 

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.linear_model import RidgeClassifierCV
from sklearn.metrics import f1_score
import sklearn.metrics

models = [RandomForestClassifier(max_depth=2, random_state=0), DecisionTreeClassifier(random_state = 0),
          ExtraTreeClassifier(random_state = 0),KNeighborsClassifier(n_neighbors=3),
          MLPClassifier(random_state=0, max_iter=300),
          RidgeClassifierCV()
          ]
model_names = ['RFC', 'DTC', 'ETC']

def evaluation(model):
    clf = model
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    scores = cross_val_score(clf, X_train, y_train, cv= 3, scoring = 'f1_micro')
    print('The f1-score is {}'.format(scores.mean()))


for model in models:

    evaluation(model)


clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X_train,y_train)
clf.score(X_train,y_train)
pred = clf.predict(X_test)


f1 = f1_score(y_test, pred, average = 'micro')

clf.get_params()

#SelectFromModel
from sklearn.feature_selection import SelectFromModel

model = SelectFromModel(clf, prefit=True)
X_train_new = model.transform(X_train)
X_test_new = model.transform(X_test)


#GridSearchCV
  
from sklearn.model_selection import GridSearchCV  
parameters = {
    'n_estimators'      : [410],
    'max_depth'         : [8,9,10],
    'random_state'      : [4],
    #'max_features': ['auto'],
    #'criterion' :['gini']
}

clf = GridSearchCV(RandomForestClassifier(), parameters, cv=10, n_jobs=-1)
clf.fit(X_train_new, y_train)

print(clf.score(X_train_new, y_train))
print(clf.best_params_)




#Prediction of the 2019-2020 calendar

to_pred = pd.read_csv('data/to_predict.csv')
final = to_pred.copy()
to_pred['AwayTeam_encoded'] = le.fit_transform(to_pred['AwayTeam'])
to_pred['HomeTeam_encoded'] = le.transform(to_pred['HomeTeam'])
to_pred.drop(['AwayTeam', 'HomeTeam'], axis = 1, inplace = True)

to_pred = model.transform(to_pred)

prediction = clf.predict(to_pred)

final = final[['Date','HomeTeam', 'AwayTeam']]

final['Result'] = prediction


