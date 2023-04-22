"""
Using the cleaned rating and users datasets a new dataset is created containing all the user and rating figures for each
ISBN. Meaning each ISBN has a count for each country and age group, to be used for data analysis.

This file is saved to Data/Processed/Part/rating_details.csv
"""
import numpy as np
import pandas as pd

ratings = pd.read_csv("../Data/Cleaned/ratings.csv", encoding="cp1252", on_bad_lines="skip")
users = pd.read_csv("../Data/Cleaned/users.csv", on_bad_lines="skip")

# Number of ratings and average ages
no_ratings, avg_ages = [], []

# These are the groups which of which the occurrences are counted per ISBN for data analysis
u_17_groups, u_30_groups, u_45_groups, u_60_groups, o_60_groups = [], [], [], [], []
usa_groups, uk_groups, australia_groups, new_zealand_groups, canada_groups, other_groups = [], [], [], [], [], []

# Only get required ISBNs to reduce already long processing time
known_valid = pd.read_csv("../Data/Processed/books_rated.csv", encoding="cp1252", on_bad_lines="skip")
isbns = known_valid["ISBN"].unique()

counter = 0

for isbn in isbns:
    # Given ISBN get all relevant users from ratings.csv
    isbn_ratings = ratings.loc[ratings['ISBN'] == isbn]
    user_ids = isbn_ratings["User"]

    # Analysis for this ISBN
    rating_count = 0
    ages = []
    u_17, u_30, u_45, u_60, o_60 = 0, 0, 0, 0, 0
    usa, united_kingdom, australia, new_zealand, canada, other = 0, 0, 0, 0, 0, 0

    for user in user_ids:
        user_details = users.loc[users['User'] == user]
        full_location = user_details["Location"].values[0].split(", ")

        age = user_details["Age"].values[0]
        ages.append(age)

        if not np.isnan(age):
            if age < 17:
                u_17 += 1
            elif age < 30:
                u_30 += 1
            elif age < 45:
                u_45 += 1
            elif age < 60:
                u_60 += 1
            else:
                o_60 += 1

        country = full_location[-1]

        if country == "usa":
            usa += 1
        elif country == "united kingdom":
            united_kingdom += 1
        elif country == "new zealand":
            new_zealand += 1
        elif country == "australia":
            australia += 1
        elif country == "canada":
            canada += 1
        else:
            other += 1

        rating_count += 1

    avg_ages.append(np.nanmean(ages).round())
    no_ratings.append(rating_count)

    u_17_groups.append(u_17)
    u_30_groups.append(u_30)
    u_45_groups.append(u_45)
    u_60_groups.append(u_60)
    o_60_groups.append(o_60)

    usa_groups.append(usa)
    uk_groups.append(united_kingdom)
    new_zealand_groups.append(new_zealand)
    australia_groups.append(australia)
    canada_groups.append(canada)
    other_groups.append(other)

    counter += 1
    print("{} out of {}".format(counter, len(user_ids)))

# Store all the details in a dataframe and then save the dataframe into processed files
details_df = pd.DataFrame(
    {"ISBN": isbns, "No.": no_ratings, "Avg_Age": avg_ages,
     "Under_17": u_17_groups, "Under_30": u_30_groups, "Under_45": u_45_groups, "Under_60": u_60_groups,
     "Over_60": o_60_groups, "USA": usa_groups, "United_Kingdom": uk_groups,
     "Australia": australia_groups, "New_Zealand": new_zealand_groups, "Canada": canada_groups, "Other": other_groups})

details_df.to_csv("../Data/Processed/Part/rating_details.csv", index=False)
