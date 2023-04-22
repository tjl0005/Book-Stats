"""
Using the cleaned user data the overall demographics for the dataset are compiled. This includes the following figures
for each country: Under_17, Under_30, Under_45, Under_60, Over_60, Total (For Country) as well as the totals for each
age group and the dataset overall.

These figures can be found at Data/Processed/user_demographics.csv
"""
import pandas as pd
import numpy as np

users = pd.read_csv("../Data/Cleaned/users.csv", encoding="cp1252", on_bad_lines="skip")
user_ids = users["User"].unique()

# Contents for all the rows (Countries) of the new dataframe
rows = [["USA", 0, 0, 0, 0, 0], ["United_Kingdom", 0, 0, 0, 0, 0], ["Australia", 0, 0, 0, 0, 0],
        ["New_Zealand", 0, 0, 0, 0, 0], ["Canada", 0, 0, 0, 0, 0], ["Other", 0, 0, 0, 0, 0]]

total = len(user_ids)
count = 0

for user in user_ids:
    user_details = users.loc[users['User'] == user]

    full_location = user_details["Location"].values[0].split(", ")
    age = user_details["Age"].values[0]

    if not np.isnan(age):
        country = full_location[-1]

        # Country represents index within the rows 2D array
        if country == "usa":
            country_index = 0
        elif country == "united kingdom":
            country_index = 1
        elif country == "new zealand":
            country_index = 2
        elif country == "australia":
            country_index = 3
        elif country == "canada":
            country_index = 4
        else:
            country_index = 5

        # Using relevant index can access the relevant age count and increment it
        if age < 17:
            rows[country_index][1] += 1
        elif age < 30:
            rows[country_index][2] += 1
        elif age < 45:
            rows[country_index][3] += 1
        elif age < 60:
            rows[country_index][4] += 1
        else:
            rows[country_index][5] += 1

    count += 1
    print("{} out of {}".format(count, total))

user_stats = pd.DataFrame(rows, columns=["Country", "Under_17", "Under_30", "Under_45", "Under_60", "Over_60"])

# Add totals for age groups and countries
user_stats['Total'] = user_stats[["Under_17", "Under_30", "Under_45", "Under_60", "Over_60"]].sum(axis=1)
age_totals = ["Total"] + user_stats[["Under_17", "Under_30", "Under_45", "Under_60", "Over_60", "Total"]].sum(axis=0)\
    .tolist()
# Append row
user_stats.loc[len(user_stats)] = age_totals

user_stats.to_csv("../Data/Processed/Part/user_demographics.csv", index=False)
