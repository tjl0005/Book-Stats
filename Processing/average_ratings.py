import pandas as pd

# Data cleaned in cleaning.py
rating_data = pd.read_csv('../data/Cleaned/ratings.csv', encoding='cp1252', on_bad_lines='skip')
book_data = pd.read_csv('../data/Cleaned/books.csv', encoding='cp1252', on_bad_lines='skip')

# Store average ratings to be appended to book_data
rating_list, isbn_list = [], []
counter = 0

# Get all ISBNs in dataset
unique_isbn = rating_data['ISBN'].unique()

# Go through each ISBN and get their average rating
for isbn in unique_isbn:
    counter += 1
    print("\r{} out of {}\r".format(counter, len(unique_isbn)))

    # Select all rows with current ISBN
    isbn_data = rating_data.loc[rating_data['ISBN'] == isbn]
    # Get average rating and round it to 1 decimal place
    isbn_rating = isbn_data.loc[:, 'Rating'].mean().round(1)

    # A rating of 0 is invalid
    if isbn_rating == 0:
        rating_list.append("N/A")
    else:
        # Dividing by two because it will be merged with other ratings out of 5
        rating_list.append(isbn_rating / 2)

# Add ISBNs and their average ratings to new dataframe
average_rating_df = pd.DataFrame(unique_isbn, columns=["ISBN"])
average_rating_df["Rating"] = rating_list

# Save dataframe, this is merged with book data in data_merging.py
average_rating_df.to_csv('../data/Processed/Part/isbn_ratings', header=True, index=False)
