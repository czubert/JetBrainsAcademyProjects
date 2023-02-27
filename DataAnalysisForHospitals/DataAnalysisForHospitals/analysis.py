import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 8)

# Imports
df_general = pd.read_csv('test/general.csv')
df_prenatal = pd.read_csv('test/prenatal.csv')
df_sports = pd.read_csv('test/sports.csv')

datasets = [df_general, df_prenatal, df_sports]


# # Unifying columns names
def unifying_col_names(data):
    """
    Unifying column names.
    :param data: pandas DataFrame
    :return: pandas DataFrame
    """
    cols = data.columns[1:3]
    return data.rename({cols[0]: 'hospital', cols[1]: 'gender'}, axis=1)


for i, dataset in enumerate(datasets):
    datasets[i] = unifying_col_names(dataset)

# Merging datasets, getting rid of irrelevant column 'Unnamed: 0'
df = pd.concat(datasets, ignore_index=True).drop('Unnamed: 0', axis=1)

# Getting rid of empty rows
df = df.dropna(how='all')

# Unifying gender column
df.gender = df.gender.map({'male': 'm', 'man': 'm', 'female': 'f', 'woman': 'f'})
df.loc[df['hospital'] == 'prenatal', 'gender'] = 'f'

# Dealing with NaNs in other columns
selected_cols = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
df[selected_cols] = df[selected_cols].fillna(0)

# 1
hospital_with_most_patients = df.hospital.value_counts().idxmax()

# 2
general_hosp = df[df.hospital == 'general']
stomach_issues = round(general_hosp['diagnosis'].value_counts()['stomach'] / general_hosp['diagnosis'].shape[0], 3)

# 3
sport_hosp = df[df.hospital == 'sports']
dislocation_issues = round(sport_hosp['diagnosis'].value_counts()['dislocation'] / sport_hosp['diagnosis'].shape[0], 3)

# 4
age_diff = abs(sport_hosp.age.median() - general_hosp.age.median())

# 5

hosp_test = df[df.blood_test == 't'].pivot_table(index='hospital', values='blood_test', aggfunc='count')

# stage 4
# print(f'The answer to the 1st question is {hospital_with_most_patients}')
# print(f'The answer to the 2nd question is {stomach_issues}')
# print(f'The answer to the 3rd question is {dislocation_issues}')
# print(f'The answer to the 4th question is {age_diff}')
# print(f'The answer to the 5th question is {hosp_test.idxmax()[0]}, {hosp_test.max()[0]} blood tests')

# 5
# alternatively with value counts instead of pivot_table
# hosp_test = df.loc[:, ['hospital', 'blood_test']]
# hosp_test = hosp_test[hosp_test.blood_test == 't']
# print(f'The answer to the 5th question is {hosp_test.value_counts().idxmax()[0]}, '
#       f'{hosp_test.value_counts().max()} blood tests')


# stage 5

# Q1
plt.figure(1)
plt.hist(df['age'], bins=[0, 15, 35, 55, 70, 80], color="r", edgecolor="white", )
plt.title("Patient age")
plt.ylabel("Number of people")
plt.xlabel("Age")

# Q2
plt.figure(2)
explode = [0.01] * len(df['diagnosis'].value_counts())
plt.pie(df['diagnosis'].value_counts(), labels=df['diagnosis'].value_counts().index, autopct='%.1f%%', explode = explode)


# Q3
data_general = df.loc[df.hospital == 'general', 'height']

data_sports = df.loc[df.hospital == 'sports', 'height']

data_prenatal = df.loc[df.hospital == 'prenatal', 'height']
data_list = [data_general, data_sports, data_prenatal]

fig, axes = plt.subplots()

axes.set_xticks((1, 2, 3))
axes.set_xticklabels(("General", "Sports", "Prenatal"))

plt.violinplot(data_list)

plt.show()




# answers
print("The answer to the 1st question: 15-35")
print("The answer to the 2nd question: pregnancy")
print("The answer to the 3rd question: It's because some hospitals measure patients' height in feet, "
      "while some hospitals measure it in meters")