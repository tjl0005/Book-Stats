"""
This file contains the code used to merge incomplete data together to result in a complete dataset
"""
import pandas as pd


def merge_books_with_ratings():
    """
    Uses the cleaned books dataset and the processed partial dataset "isbn_ratings.csv" and merges them together to
    produce a dataset containing all books their ratings. Incomplete data is also removed before merging.

    The final output is located within Data/Processed/Part/isbn_details.csv
    """
    book_data = pd.read_csv("../Data/Cleaned/books.csv", encoding="cp1252")
    isbn_ratings = pd.read_csv("../Data/Processed/Part/isbn_ratings.csv", encoding="cp1252")

    # Removing any entries missing data
    isbn_ratings.dropna(inplace=True)

    # Merge book data with average ratings using ISBN, using inner so only entries with ratings kept
    books_with_ratings = book_data.merge(isbn_ratings, left_on="ISBN", right_on="ISBN")
    books_with_ratings.to_csv("../data/Processed/books_rated.csv", header=True, index=False)


def merge_books_and_ratings_with_details():
    """
    Uses the processed dataset containing all books with their ratings and the dataset containing summaries, categories,
    page counts for all ISBNs. Before merging some standardisation is performed on the categories column in which
    very similar categories are merged.

    The final output is located within Data/Processed/books_complete_details.csv
    """
    books_with_ratings = pd.read_csv("../Data/Processed/books_rated.csv", encoding="cp1252")
    isbn_details = pd.read_csv("../Data/Processed/Part/isbn_details.csv")

    # Some categories overlap, so they are combined here
    isbn_details.loc[isbn_details['Categories'].str.contains('biography', na=False), 'Categories'] = "['Biography']"
    isbn_details.loc[isbn_details['Categories'].str.contains('Autobiography', na=False), 'Categories'] = "['Biography']"
    isbn_details.loc[isbn_details['Categories'].str.contains('Adventure', na=False), 'Categories'] = "['Adventure']"

    # Tidying strings
    isbn_details["Categories"] = isbn_details["Categories"].str.replace("'", "")
    isbn_details["Categories"] = isbn_details["Categories"].str.replace("stories", "")
    books_with_ratings["Title"] = books_with_ratings["Title"].str.replace("&amp;", "and")
    books_with_ratings["Title"] = books_with_ratings["Title"].str.replace(": A Novel", "")

    # Dropping all rows with missing data
    isbn_details.dropna(inplace=True)

    # Merge book data with average ratings using ISBN, using inner as only keeping complete records
    books_with_complete_details = books_with_ratings.merge(isbn_details, left_on="ISBN", right_on="ISBN")
    # Adding shortened summaries
    books_with_complete_details.to_csv("../data/Processed/books_complete_details.csv", header=True, index=False)
