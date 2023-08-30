import pandas as pd
import requests
import os
import numpy as np

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data is now loaded to the Data folder.

    """
    # # # STAGE 1 # # #
    """
    # write your code here
    a = pd.read_xml('../Data/A_office_data.xml')
    b = pd.read_xml('../Data/B_office_data.xml')
    hr = pd.read_xml('../Data/hr_data.xml')

    # Reindex all three datasets using employee_office_id and employee_id as the index
    a = a.set_index(a['employee_office_id'].apply(lambda x: 'A' + str(x)), drop=True)
    b = b.set_index(b['employee_office_id'].apply(lambda x: 'B' + str(x)), drop=True)
    hr = hr.set_index('employee_id', drop=False)

    # # Explore the data
    # print("Office A data:")
    # print(a.head())
    # print("\nOffice B data:")
    # print(b.head())
    # print("\nHR data:")
    # print(hr.head())

    # Concatenate the data from offices A and B into one comprehensive dataset
    offices_ab = pd.concat([a, b], axis=0)

    # Merge the unified office dataset with HR's dataset using left merging by index
    merged_data = offices_ab.merge(hr, left_index=True, right_index=True, how='left', indicator=True)

    # Keep only the employees' records present in both datasets
    merged_data = merged_data[merged_data['_merge'] == 'both']

    # Drop unnecessary columns from the final dataset
    merged_data.drop(columns=['employee_office_id', 'employee_id', '_merge'], inplace=True)

    # Sort the final dataset by index
    merged_data.sort_index(inplace=True)

    """
    # # # STAGE 2 # # #
    """
    # # Print the final DataFrame index and column names
    # print(list(merged_data.index))
    # print(list(merged_data.columns))

    """
    # # # STAGE 3 # # #
    """
    # # question 1
    most_hours_dept = merged_data.sort_values('average_monthly_hours', ascending=False).iloc[:10, :][
        'Department'].to_list()

    # # question 2
    num_of_projects = merged_data[(merged_data.salary == 'low') & (merged_data.Department == 'IT')].number_project.sum()

    # # question 3
    employees = ['A4', 'B7064', 'A3033']
    scores = []
    for employee in employees:
        scores.append(merged_data.loc[employee, ['last_evaluation', 'satisfaction_level']].to_list())

    # print(most_hours_dept)
    # print(num_of_projects)
    # print(scores)

    """
    # # # STAGE 4 # # #
    """

    # def count_bigger_5(x):
    #     return sum(x > 5)
    #
    #
    # working_status = merged_data.groupby('left').agg(
    #     {
    #         'number_project': ['median', ('count_bigger_5', lambda x: count_bigger_5(x))],
    #         'time_spend_company': ['mean', 'median'],
    #         'Work_accident': ['mean'],
    #         'last_evaluation': ['mean', 'std'],
    #     }
    # )
    #
    # working_status.index.name = 'left'
    # working_status = working_status.round(2)
    #
    # print(working_status.to_dict())

    """
    # # # STAGE 5 # # #
    """

    # First pivot
    first_pivot = merged_data.pivot_table(index='Department',
                                          columns=['left', 'salary'],
                                          values='average_monthly_hours',
                                          aggfunc=np.median).round(1)

    first_pivot = first_pivot.loc[(first_pivot[(0.0, 'high')] < first_pivot[(0.0, 'medium')]) | (
            first_pivot[(1.0, 'high')] > first_pivot[(1.0, 'low')])]

    first_pivot = first_pivot.round(2)

    print(first_pivot.to_dict())

    # Second pivot
    second_pivot = merged_data.pivot_table(index='time_spend_company',
                                           columns='promotion_last_5years',
                                           values=['satisfaction_level', 'last_evaluation'],
                                           aggfunc=[np.max, np.mean, np.min])

    second_pivot = second_pivot.loc[
        (second_pivot[('mean', 'last_evaluation', 0)] > second_pivot[('mean', 'last_evaluation', 1)])]

    second_pivot = second_pivot.round(2)

    print(second_pivot.to_dict())
