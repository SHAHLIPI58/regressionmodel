# -*- coding: utf-8 -*-
"""
Created on Sat May 26 23:14:28 2018

@author: ll
"""



# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Importing the dataset
dataset = pd.read_csv('petrol1.csv')
y = dataset.iloc[:,0].values
X1 = dataset.iloc[:,2].values


from sklearn.preprocessing import Imputer
imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
X1 = X1.reshape(-1,1)
X1 = imp.fit_transform(X1)
dataset['horsepower'] = X1
X = dataset.iloc[:,1:5].values

import statsmodels.formula.api as sm
X2 = np.append(arr = np.ones((398,1)).astype(int), values = X, axis = 1)
X_opt= X2
#X_opt = X1[:,[0,1,2,3,4]]
regressor_OLS = sm.OLS(endog = y, exog = X_opt).fit()
regressor_OLS.summary()
X_opt= X2[:,[0,2,3,4]]
regressor_OLS = sm.OLS(endog = y, exog = X_opt).fit()
regressor_OLS.summary()

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_opt, y, test_size = 0.2, random_state = 0)
# Feature Scaling
"""from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
sc_y = StandardScaler()
y_train = sc_y.fit_transform(y_train)"""




# Fitting Random Forest Regression to the dataset
from sklearn.ensemble import RandomForestRegressor
#accu - 69.16 % regressor = RandomForestRegressor(max_depth =3,max_features = "log2",min_samples_split =2, n_estimators = 100, verbose = 0)
# accu - 69.33 %regressor = RandomForestRegressor(max_depth =3,max_features = "log2",min_samples_split =3, n_estimators = 40, verbose = 0)
# acc-> 69.47% regressor = RandomForestRegressor(max_depth =4,max_features = "log2",min_samples_split =3,n_estimators = 10, verbose = 0)
# accu ->69.48% regressor = RandomForestRegressor(max_depth =3,max_features = "sqrt", min_samples_split =2,n_estimators = 70, verbose = 0)
regressor = RandomForestRegressor(max_depth =3,max_features = "sqrt", 
                                  min_samples_split =2,n_estimators = 74, verbose = 0)
                                  
regressor.fit(X_train, y_train)
important_feature = regressor.feature_importances_
y_random_forest_pred = regressor.predict(X_test)
# Predicting a new result
y_pred = regressor.predict([[8,307,307,3504],[8,455,455,4425]])

from sklearn.metrics import mean_squared_error
from math import sqrt

rms_svr = sqrt(mean_squared_error(y_test , y_random_forest_pred))

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train, cv = 10)
accuracies_mean = accuracies.mean()
accuracies.std()

# Applying Grid Search to find the best model and the best parameters
from sklearn.model_selection import GridSearchCV
parameters = [{'min_samples_split':[2,3,4],'n_estimators': [70,71,72,73,74,75,76,77],'verbose':[0], 'max_features':["auto","log2","sqrt"],
               'max_depth':[2,3,4,5]}]
grid_search = GridSearchCV(estimator = regressor,
                           param_grid = parameters,
                           scoring = 'r2',
                           cv = 10)
grid_search = grid_search.fit(X_train, y_train)
best_r2 = grid_search.best_score_
best_parameters = grid_search.best_params_


# Visualising the Random Forest Regression results (higher resolution)
#X_grid = np.arange(min(X), max(X), 0.01)
#X_grid = X_grid.reshape((len(X_grid), 1))
#plt.scatter(X, y, color = 'red')
#plt.plot(X_grid, regressor.predict(X_grid), color = 'blue')
#plt.title('Truth or Bluff (Random Forest Regression)')
#plt.xlabel('Position level')
#plt.ylabel('Salary')
#plt.show()