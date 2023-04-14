import os.path
import pandas as pd


def clean(filename, delete):
    # All cleaned files are saved to Data/Cleaned/
    if not os.path.isfile('../data/Cleaned/{}.csv'.format(filename)):
        if filename == "books":
            books_file = pd.read_csv('../data/Unprocessed/{}.csv'.format(filename), encoding='cp1252',
                                     on_bad_lines='skip', sep=";")
            # Removing irrelevant columns and standardising names
            books_file.drop(columns=books_file.columns[[4, 5, 6, 7]], axis=1, inplace=True)
            books_file.rename({'Book-Title': 'Title', 'Book-Author': 'Author', "Year-Of-Publication": "Year"}, axis=1,
                              inplace=True)
            books_file = books_file[['ISBN', 'Title', 'Author', 'Year']]  # Changing order

            books_file.to_csv('../data/Cleaned/{}.csv'.format(filename), index=False)
            print("{}.csv contains: {}".format(filename, books_file.columns.values))

        elif filename == "ratings":
            ratings_file = pd.read_csv('../data/Unprocessed/{}.csv'.format(filename), encoding='cp1252',
                                       on_bad_lines='skip', sep=";")

            ratings_file.rename({"User-ID": "User", 'Book-Rating': 'Rating'}, axis=1, inplace=True)
            ratings_file = ratings_file[['ISBN', 'Rating', 'User']]

            # Remove rows with no usable rating
            ratings_file = ratings_file[ratings_file.Rating != 0]

            ratings_file.to_csv('../data/Cleaned/{}.csv'.format(filename), header=True, index=False)
            print("{}.csv contains: {}".format(filename, ratings_file.columns.values))

        elif filename == "users":
            users_file = pd.read_csv('../data/Unprocessed/{}.csv'.format(filename), encoding='cp1252',
                                     on_bad_lines='skip', sep=";")

            users_file.rename({"User-ID": "User"}, axis=1, inplace=True)
            users_file = users_file[['User', 'Location', 'Age']]

            users_file.to_csv('../data/Cleaned/{}.csv'.format(filename), header=True, index=False)
            print("{}.csv contains: {}".format(filename, users_file.columns.values))

    if delete:  # For testing purposes
        os.remove('../data/Cleaned/{}.csv'.format(filename))

# clean("books", False)
# clean("ratings", False)
# clean("users", False)
