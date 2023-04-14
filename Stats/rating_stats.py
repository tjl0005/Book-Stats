import numpy as np
import pandas as pd
from collections import Counter

ratings = pd.read_csv("../Data/Cleaned/ratings.csv", encoding="cp1252", on_bad_lines="skip")
users = pd.read_csv("../Data/Cleaned/users.csv", on_bad_lines="skip")

no_ratings, avg_ages, mode_countries, mode_states = [], [], [], []
counter = 0

# Only get required ISBNs to reduce processing time
known_valid = pd.read_csv("../Data/Processed/books_rated.csv", encoding="cp1252", on_bad_lines="skip")
isbns = known_valid["ISBN"].unique()

for isbn in isbns:
    # Given ISBN get all relevant users from ratings.csv
    isbn_ratings = ratings.loc[ratings['ISBN'] == isbn]
    user_ids = isbn_ratings["User"].values
    rating_count = 0
    countries, states, ages = [], [], []

    for user in user_ids:
        user_details = users.loc[users['User'] == user]
        ages.append(user_details["Age"].values[0])

        full_location = user_details["Location"].values[0].split(", ")
        countries.append(full_location[-1])
        states.append(full_location[-2])

        rating_count += 1

    avg_ages.append(np.nanmean(ages).round())
    mode_countries.append(Counter(countries).most_common(5))
    mode_states.append(Counter(states).most_common(5))
    no_ratings.append(rating_count)

    counter += 1
    print("{} out of {}".format(counter, len(isbns)))


details_df = pd.DataFrame(
    {"ISBN": isbns, "No.": no_ratings, "Avg_Age": avg_ages, "Countries": mode_countries, "States": mode_states})
details_df.to_csv("../Data/Processed/rating_details.csv", index=False)
