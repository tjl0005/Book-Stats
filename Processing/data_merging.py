import pandas as pd


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)


def merge_books_with_ratings():
    book_data = pd.read_csv("../Data/Cleaned/books.csv", encoding="cp1252", on_bad_lines="skip")
    rating_data = pd.read_csv("../Data/Processed/Part/isbn_ratings.csv", encoding="cp1252", on_bad_lines="skip")

    # Removing any entries without useful data
    rating_data.dropna(inplace=True)

    # Merge book data with average ratings using ISBN, using inner so only entries with ratings kept
    books_with_ratings = book_data.merge(rating_data, how='inner', left_on='ISBN', right_on='ISBN')
    books_with_ratings.to_csv('../data/Processed/books_rated.csv', header=True, index=False)


def merge_books_and_ratings_with_details():
    books_with_ratings = pd.read_csv("../Data/Processed/books_rated.csv", encoding="cp1252", on_bad_lines="skip")
    details_data = pd.read_csv("../Data/Processed/Part/isbn_details.csv", on_bad_lines="skip")

    # Merge book data with average ratings using ISBN, using inner as only keeping complete records
    books_with_complete_details = books_with_ratings.merge(details_data, how='inner', left_on='ISBN', right_on='ISBN')
    books_with_complete_details.to_csv('../data/Processed/books_complete_details.csv', header=True, index=False)
