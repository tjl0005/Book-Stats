import pandas as pd
import numpy as np

users = pd.read_csv("../Data/Cleaned/users.csv", encoding="cp1252", on_bad_lines="skip")
user_ids = users["User"].unique()

columns = {"Under_17": 0, "Under_30": 0, "Under_45": 0, "Under_60": 0, "Over_60": 0, "USA": 0, "United_Kingdom": 0,
           "Australia": 0, "New_Zealand": 0, "Canada": 0, "Other": 0}

other_countries = []
total = len(user_ids)
count = 0

for user in user_ids:
    user_details = users.loc[users['User'] == user]

    full_location = user_details["Location"].values[0].split(", ")
    age = user_details["Age"].values[0]

    if not np.isnan(age):
        if age < 17:
            columns["Under_17"] += 1
        elif age < 30:
            columns["Under_30"] += 1
        elif age < 45:
            columns["Under_45"] += 1
        elif age < 60:
            columns["Under_60"] += 1
        else:
            columns["Over_60"] += 1

        country = full_location[-1]

        if country == "usa":
            columns["USA"] += 1
        elif country == "united kingdom":
            columns["United_Kingdom"] += 1
        elif country == "new zealand":
            columns["New_Zealand"] += 1
        elif country == "australia":
            columns["Australia"] += 1
        elif country == "canada":
            columns["Canada"] += 1
        else:
            columns["Other_Country"] += 1
            other_countries.append(country)

    count += 1
    print("{} out of {}".format(count, total))

user_stats = pd.DataFrame([columns])
user_stats.to_csv("../Data/Processed/Part/user_stats.csv", index=False)
