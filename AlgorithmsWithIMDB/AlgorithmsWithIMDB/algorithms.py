import csv

import pandas as pd

# Step 2: Read and store the data using pandas
df = pd.read_csv('movies.csv', encoding='UTF-8', header=None, names=['Title', 'Rating'])

# Step 3: Print the data
for index, row in df.iterrows():
    title = row['Title'].replace('"', '')  # Removing quotes from movie titles
    rating = row['Rating']
    # print(f'{title} - {rating}')

# Step 4: Linear search for movies with a rating of 6
for index, row in df.iterrows():
    title = row['Title'].replace('"', '')  # Removing quotes from movie titles
    rating = float(row['Rating'])
    # if rating == 6.0:
    #     print(f'{title} - {rating}')

# Step 4: Print the sorted data
movies_data = []
with open('movies.csv', encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        title, rating = row
        title = title.replace('"', '')
        movies_data.append({'Title': title, 'Rating': float(rating)})


# Step 3: Bubble Sort to sort the data by ratings in ascending order
def bubble_sort(data):
    n = len(data)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if data[j]['Rating'] > data[j + 1]['Rating']:
                data[j], data[j + 1] = data[j + 1], data[j]

def merge_sort(data):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i]['Rating'] < right_half[j]['Rating']:
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1


def binary_search_movies(data, target_rating):
    low = 0
    high = len(data) - 1

    while low <= high:
        middle = (low + high) // 2
        movie = data[middle]
        rating = movie['Rating']

        if rating == target_rating:
            print(f"{movie['Title']} - {rating}")

            # Check for other occurrences on the left side of the middle
            i = middle - 1
            while i >= low and data[i]['Rating'] == target_rating:
                print(f"{data[i]['Title']} - {data[i]['Rating']}")
                i -= 1

            # Check for other occurrences on the right side of the middle
            i = middle + 1
            while i <= high and data[i]['Rating'] == target_rating:
                print(f"{data[i]['Title']} - {data[i]['Rating']}")
                i += 1

            return

        if rating < target_rating:
            low = middle + 1
        else:
            high = middle - 1


merge_sort(movies_data)
binary_search_movies(movies_data, 6.0)

