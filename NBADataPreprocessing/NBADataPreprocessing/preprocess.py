import numpy as np
import pandas as pd
import os
import requests
from dateutil.relativedelta import relativedelta
import utils

# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)


def clean_data(path):
    df = pd.read_csv(path)
    df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
    df.draft_year = df.draft_year.astype('int32')
    df['draft_year'] = pd.to_datetime(df.draft_year, format='%Y')

    df['team'] = df['team'].fillna('No Team')

    df['height'] = df['height'].replace(r'.*\/ ', '', regex=True)

    df['weight'] = df['weight'].replace(r'.*\/ ', '', regex=True)
    df['weight'] = df['weight'].replace(r' kg.', '', regex=True)

    df['salary'] = df['salary'].replace(r'\$', '', regex=True)

    df[['height', 'weight', 'salary']] = df[['height', 'weight', 'salary']].round(
        {'height': 2, 'weight': 1, 'salary': 1}).astype(float)

    df.loc[df['country'] != 'USA', 'country'] = 'Not-USA'

    df.loc[df['draft_round'] == 'Undrafted', 'draft_round'] = '0'
    return df


def feature_data(df):
    # version 2020 or 2022
    df['version'] = df['version'].apply(lambda x: '2020' if '20' in x else '2021')
    df['version'] = pd.to_datetime(df['version'])

    # Age
    df['age'] = df['version'].dt.to_period('Y') - df['b_day'].dt.to_period('Y')
    df['age'] = df.loc[:, 'age'].apply(lambda x: x.n)

    # Experience
    df['experience'] = df['version'].dt.to_period('Y') - df['draft_year'].dt.to_period('Y')
    df['experience'] = df.loc[:, 'experience'].apply(lambda x: x.n)

    # BMI
    df['bmi'] = df['weight'] / df['height'] ** 2

    # Dropping irrelevant columns
    df.drop(['version', 'draft_year', 'weight', 'height'], inplace=True, axis=1)

    # Dropping hight cardinality features
    cols = []
    for col in df.columns:
        if df[col].dtype == "object" or df[col].dtype == 'datetime64[ns]':
            cols.append(col)
    df.drop(df.loc[:, cols].loc[:, df.nunique() > 50], axis=1, inplace=True)

    return df


# def multicol_data(features):
#     df_num = features.select_dtypes(include='number')
#     df_no_salary = df_num.drop(columns='salary')
#
#     mult_coll = utils.ReduceVIF(thresh=150)
#     df_nomulti = mult_coll.fit_transform(df_no_salary)
#
#     df_with_salary = pd.concat((df_nomulti, df_num['salary']), axis=1)
#     return df_with_salary


# # OR

def multicol_data(df):
    corr = df.select_dtypes('number').drop(columns='salary').corr()
    correlated_features = []
    for i in range(corr.shape[0]):
        for j in range(0, i):
            if corr.iloc[i, j] > 0.5 or corr.iloc[i, j] < -0.5:
                correlated_features.append([corr.columns[i], corr.index[j]])

    for feature1, feature2 in correlated_features:
        if df[[feature1, 'salary']].corr().iloc[1, 0] > df[[feature2, 'salary']].corr().iloc[1, 0]:
            df.drop(columns=feature2, inplace=True)
        else:
            df.drop(columns=feature1, inplace=True)

    return df


from sklearn.preprocessing import StandardScaler, OneHotEncoder


def transform_numerical(df):
    df_num = df.select_dtypes('number')
    scaler = StandardScaler()
    x = scaler.fit_transform(df_num)
    data = utils.BackToDf(df_num.columns)
    return data.fit_transform(x)


def MyOneHot(df):
    categorical_features = ['team', 'position', 'country', 'draft_round']
    x = df.loc[:, categorical_features]
    onehot = utils.MyOneHotEncoder()
    onehot.fit(x)
    return onehot.transform(x)


def transform_categorical(df):
    categorical_features = ['team', 'position', 'country', 'draft_round']
    x = df.loc[:, categorical_features]
    onehot = OneHotEncoder()
    onehot.fit(x)
    return pd.DataFrame.sparse.from_spmatrix(onehot.transform(x), columns=np.concatenate(onehot.categories_))


def transform_data(multicol):
    X_num = transform_numerical(multicol)
    X_onehot = transform_categorical(multicol)
    X1 = pd.concat([X_num, X_onehot], axis=1).drop(columns='salary')
    y1 = X_num['salary']
    y1.name = 'y'
    return X1, y1


data_path = "../Data/nba2k-full.csv"
df_cleaned = clean_data(data_path)
df_featured = feature_data(df_cleaned)
df_multicol = multicol_data(df_featured)
X, y = transform_data(df_multicol)


answer = {
    'shape': [X.shape, y.shape],
    'features': list(X.columns),
}
print(answer)
