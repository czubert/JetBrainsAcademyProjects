# write your code here
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import GridSearchCV

from tensorflow import keras
from sklearn.model_selection import train_test_split
import numpy as np

(x_train_cut, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_train_cut = x_train_cut[:6000]
y_train = y_train[:6000]

X_train, X_test, y_train, y_test = train_test_split(x_train_cut, y_train, test_size=0.3, random_state=40)

X_train = np.reshape(X_train, (X_train.shape[0], (X_train.shape[1] * X_train.shape[2])))
X_test = np.reshape(X_test, (X_test.shape[0], (X_test.shape[1] * X_test.shape[2])))

nor = Normalizer()
X_test_norm = nor.fit_transform(X_test)
nor = Normalizer()
X_train_norm = nor.fit_transform(X_train)

best_score = {'model': None, 'score': 0}
sec_best_score = {'model': None, 'score': 0}

# the function
def fit_predict_eval(model, features_train, features_test, target_train, target_test):
    clf = model
    # here you fit the model
    clf = clf.fit(features_train, target_train)
    # make a prediction
    y_pred = clf.predict(features_test)
    # calculate accuracy and save it to score
    score = clf.score(features_test, target_test)

    if score > best_score['score']:
        best_score['model'] = model
        best_score['score'] = score
    elif score > sec_best_score['score']:
        sec_best_score['model'] = model
        sec_best_score['score'] = score

    # print(f'Model: {model}\nAccuracy: {score}\n')


estimators = [
    KNeighborsClassifier(),
    DecisionTreeClassifier(),
    LogisticRegression(),
    RandomForestClassifier(),
]

for est in estimators:
    fit_predict_eval(
        model=est,
        features_train=X_train_norm,
        features_test=X_test_norm,
        target_train=y_train,
        target_test=y_test
    )
# print(f"The answer to the 1st question: yes")
# print(f"The answer to the 2nd question: {best_score['model'].__class__.__name__}-{round(best_score['score'], 3)}, "
#       f"{sec_best_score['model'].__class__.__name__}-{round(sec_best_score['score'], 3)}")


best_models = [best_score, sec_best_score]

param_grid = {
    'KNN': {
        'n_neighbors': [3, 4],
        'weights': ['uniform', 'distance'],
        'algorithm': ['auto', 'brute']
        },
    'RF': {
        'n_estimators': [300, 500],
        'max_features': ['auto', 'log2'],
        'class_weight': ['balanced', 'balanced_subsample'],
        'random_state': [40]
        }
    }

for el in best_models:
    if el['model'].__class__.__name__ == 'KNeighborsClassifier':
        params = param_grid['KNN']
    elif el['model'].__class__.__name__ == 'RandomForestClassifier':
        params = param_grid['RF']
    else:
        print('Something went wrong with params')
    grid = GridSearchCV(estimator=el['model'], param_grid=params, scoring='accuracy')
    grid = grid.fit(X_train_norm, y_train)
    print("K-nearest neighbours algorithm")
    print(f'best estimator: {grid.best_estimator_}')
    print(f'accuracy: {grid.score(X_test_norm, y_test)}')
