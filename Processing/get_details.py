import json
import os
import time
import urllib.request
import pandas as pd
from urllib.error import HTTPError


# Ensure only necessary ISBNs are having data retrieved
def remaining_isbns():
    books_with_ratings = pd.read_csv("../Data/Processed/books_rated.csv", encoding="cp1252", on_bad_lines="skip")

    # Some ISBNs have already been processed so need to exclude them from the list
    if os.path.isfile('../Data/Processed/Part/isbn_details.csv'):
        details_data = pd.read_csv("../Data/Processed/Part/isbn_details.csv", on_bad_lines="skip")

        # Get common ISBNs between datasets
        common_isbns = pd.merge(books_with_ratings, details_data, how='inner', left_on='ISBN', right_on='ISBN')
        common_isbns = common_isbns["ISBN"]

        # Remove the common ISBNs from the list so only required ones remain
        remaining = books_with_ratings[~books_with_ratings['ISBN'].isin(common_isbns)]

        print("Remaining ISBNs: {}".format(len(remaining["ISBN"].index)))
        return remaining["ISBN"].values
    # First run so all ISBNs required
    else:
        print("Remaining ISBNs: {}".format(len(books_with_ratings["ISBN"].index)))
        return books_with_ratings["ISBN"].values


def get_details(all_isbns):
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    # Request only specific fields to save time
    fields = "&fields=items(volumeInfo(categories,%20pageCount),searchInfo(textSnippet))"
    # All relevant columns to be used
    stored_isbns, summaries, categories, page_counts = [], [], [], []
    # Used to show progress in console
    count = 0
    total = len(all_isbns)

    for isbn in all_isbns:
        count += 1
        try:
            # Get relevant data from API with a request
            with urllib.request.urlopen(api + isbn + fields) as f:
                content = f.read()

            obj = json.loads(content.decode("utf-8"))
            items = obj["items"][0]
            # Selecting relevant fields
            page_count = items["volumeInfo"]["pageCount"]
            category = items["volumeInfo"]["categories"]
            summary = items["searchInfo"]["textSnippet"]

            stored_isbns.append(isbn)
            summaries.append(summary)
            categories.append(category)
            page_counts.append(page_count)

        except KeyError as e:  # Error will occur if any required details not available so catch them and continue
            print("ISBN missing details {}".format(e))
            # Still add to dataframe to avoid going over them again, and so they can be flagged for deletion when merged
            stored_isbns.append(isbn)
            summaries.append(None)
            categories.append(None)
            page_counts.append(None)
        except HTTPError as e:  # Server timed out so temporarily pause
            print(e)
            time.sleep(10)

        except Exception as e:  # Quota reached, save current progress
            print(e)
            details_df = pd.DataFrame(
                {"ISBN": stored_isbns, "Summary": summaries, "Categories": categories, "Page_Count": page_counts})

            if os.path.isfile('../Data/Processed/Part/isbn_details.csv'):
                print("Appending save")
                current_details = pd.read_csv('../Data/Processed/Part/isbn_details.csv', on_bad_lines='skip')
                combined = pd.concat([current_details, details_df], axis=0)
                combined.drop_duplicates(subset="ISBN", inplace=True)
                combined.to_csv("../Data/Processed/Part/isbn_details.csv", index=False)

            else:
                print("New save")
                details_df.to_csv("../Data/Processed/Part/isbn_details.csv", index=False)

            print("Exiting and saving {} records".format(len(details_df.index)))

        print(isbn)
        print("{} out of {}".format(count, total))


isbns = remaining_isbns()
get_details(isbns)
