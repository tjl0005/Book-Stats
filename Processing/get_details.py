"""
The initial dataset does not include all desired details for the books, so using this file and Googles "Books" API, this
data is retrieved and stored for later merging within "data_merging.py" within the processing folder.
"""
import urllib.request
from json import loads
from os import path
from time import sleep
from urllib.error import HTTPError
import pandas as pd


def remaining_isbns():
    """
    Ensure only necessary ISBNs are having data retrieved

    :return: A list containing all the remaining ISBNs that are not completed yet.
    """
    books_with_ratings = pd.read_csv("../Data/Processed/books_rated.csv", encoding="cp1252", on_bad_lines="skip")

    # Some ISBNs have already been processed so need to exclude them from the list
    if path.isfile("../Data/Processed/Part/isbn_details.csv"):
        isbn_details = pd.read_csv("../Data/Processed/Part/isbn_details.csv", on_bad_lines="skip")

        # Get shared ISBNs
        shared_isbns = pd.merge(books_with_ratings, isbn_details, left_on="ISBN", right_on="ISBN")
        shared_isbns = shared_isbns["ISBN"]

        # Remove the common ISBNs from the list so only required ones remain
        remaining = books_with_ratings[~books_with_ratings["ISBN"].isin(shared_isbns)]

        print("Remaining ISBNs: {}".format(len(remaining["ISBN"].index)))
        return remaining["ISBN"].values
    # First run so all ISBNs required
    else:
        print("Remaining ISBNs: {}".format(len(books_with_ratings["ISBN"].index)))
        return books_with_ratings["ISBN"].values


def get_details(all_isbns):
    """
    Use the Google Books API to complete the known details for all possible ISBNs currently stored

    :param all_isbns: A list containing the ISBNs which are not yet completed
    """
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
        if len(isbn) > 10:
            isbn = isbn[-10:]
        try:
            # Get relevant data from API with a request
            with urllib.request.urlopen(api + isbn + fields) as f:
                content = f.read()

            obj = loads(content.decode("utf-8"))
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
            sleep(10)
        except Exception as e:  # Quota reached, save current progress
            print(e)
            save_details(stored_isbns, summaries, categories, page_counts)

        print("{} out of {}".format(count, total))

    save_details(stored_isbns, summaries, categories, page_counts)


def save_details(stored_isbns, summaries, categories, page_counts):
    """
    Save newly retrieved ISBNs details to their own csv file, this function can be called with a new batch of ISBN
    details and these details will appended to the existing file.

    :param stored_isbns: The isbns which have been completed within this batch
    :param summaries: All the summaries retrieved for the given ISBNs
    :param categories: All the categories retrieved for the given ISBNs
    :param page_counts: All the page counts retrieved for the given ISBNs
    """
    details_df = pd.DataFrame(
        {"ISBN": stored_isbns, "Summary": summaries, "Categories": categories, "Page_Count": page_counts})

    if path.isfile("../Data/Processed/Part/isbn_details.csv"):
        print("Appending save")
        current_details = pd.read_csv("../Data/Processed/Part/isbn_details.csv", on_bad_lines="skip")
        complete_details = pd.concat([current_details, details_df], axis=0)
        complete_details.drop_duplicates(subset="ISBN", inplace=True)
        complete_details.to_csv("../Data/Processed/Part/isbn_details.csv", index=False)
    else:
        print("New save")
        details_df.to_csv("../Data/Processed/Part/isbn_details.csv", index=False)


isbns = remaining_isbns()
get_details(isbns)
