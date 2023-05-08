"""
This file is used to calculate the average ratings for all books in the available dataset.

The final can be located within Data/Processed/Part/isbn_ratings.csv
"""
import pandas as pd

RATING_DATA = pd.read_csv("../data/Cleaned/ratings.csv", encoding="cp1252", on_bad_lines="skip")

# Store average ratings to be appended to book_data
ratings = []
counter = 0

# Get all ISBNs in dataset
UNIQUE_ISBNS = RATING_DATA["ISBN"].unique()

# Go through each ISBN and get their average rating
for isbn in UNIQUE_ISBNS:
    counter += 1
    print("\r{} out of {}\r".format(counter, len(UNIQUE_ISBNS)))

    # Select all rows with current ISBN
    isbn_data = RATING_DATA.loc[RATING_DATA["ISBN"] == isbn]
    # Get average rating and round it to 1 decimal place
    isbn_rating = isbn_data.loc[:, "Rating"].mean().round(1)

    # A rating of 0 is invalid
    if isbn_rating == 0:
        ratings.append("N/A")
    else:
        # Dividing by two because it will be merged with other ratings out of 5
        ratings.append(isbn_rating / 2)

# Add ISBNs and their average ratings to new dataframe
average_ratings = pd.DataFrame(UNIQUE_ISBNS, columns=["ISBN"])
average_ratings["Rating"] = ratings

# Save dataframe, this is merged with book data in data_merging.py
average_ratings.to_csv("../data/Processed/Part/isbn_ratings", header=True, index=False)
