"""
This file is used to compile various stats about the books within the dataset. The main function of this file simply
takes upto 2 groups (Countries/Age) with a sample size to find the average page counts, common categories and more. To
ensure relevance with summary data for the stats the summaries are cleaned, so all disallowed characters, stop words
(i.e. "The") and irrelevant words are removed.
"""
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import re


# Expanded stopwords with own observations
STOP_WORDS = set(
    stopwords.words("english") + ["story" + "new", "quot", "story", "new", "york", "book", "times", "one", "author",
                                  "bestselling", "life", "world", "first", "year", "author", "edition", "published",
                                  "novel", "school", "come", "bestseller", "unforgettable", "many", "stories"])

RATINGS = pd.read_csv("../Data/Processed/Part/rating_details.csv", encoding="cp1252")
books = pd.read_csv("../Data/Processed/books_complete_details.csv")


def stats(group, secondary, sample_size):
    """
    This function compiles various statistics (see return values) for the books dataset using upto to groups as subsets,
    which are provided by the user.

    :param group: First subset to be used, this is required and can be an age group or country
    :param secondary: Second subset to be used, this is not required (Can pass None if so), usually a country
    :param sample_size: The number of records to base the statistics of, mainly used for testing
    :return: average page counts, common categories, common words and common titles for the given group
    """
    if secondary:
        group_stats = RATINGS.loc[RATINGS[group] > 0]
        group_stats = group_stats.loc[RATINGS[secondary] > 0]
        group_stats = group_stats[["ISBN", group]].sort_values(by=[group], ascending=False).head(sample_size)
    elif group:
        group_stats = RATINGS.loc[RATINGS[group] > 0]
        group_stats = group_stats[["ISBN", group]].sort_values(by=[group], ascending=False).head(sample_size)
    else:
        group_stats = RATINGS[["ISBN"]].head(sample_size)

    # Store all statistics
    page_counts, authors, categories, titles, all_synopsis = [], [], [], [], []

    for isbn in group_stats["ISBN"]:
        isbn_details = books.loc[books["ISBN"] == isbn]

        # Not all ISBNs in rating details have complete details available
        if len(isbn_details) > 0:
            # Modified for easier processing later
            category = str(isbn_details["Categories"].values[0])
            category = category.translate(str.maketrans("", "", "[']"))  # Removing redundant characters

            synopsis_split = isbn_details["Short_Summary"].values[0].split()  # Synopsis is used for most common words
            page_counts.append(isbn_details["Page_Count"])
            authors.append(isbn_details["Author"].values[0])

            categories.append(category)
            all_synopsis += synopsis_split
            titles.append(isbn_details["Title"].values[0])

    categories = [x for x in categories if str(x) not in ["nan", "Fiction"]]  # Removing irrelevant categories
    all_synopsis = [word.capitalize() for word in all_synopsis]  # Ensuring all words start with capital letter

    avg_page_count = np.nanmean(page_counts).round()
    common_categories = Counter(categories).most_common(5)
    common_words = Counter(all_synopsis).most_common(5)
    common_titles = Counter(titles).most_common(5)
    common_authors = Counter(authors).most_common(5)

    return avg_page_count, common_categories, common_words, common_titles, common_authors


def process_summary():
    """
    This is used to improve the usability of all summaries given by removing stop words, illegal characters and
    irrelevant words (I.E. "Edition"), usability is improved for statistics.

    These summaries are saved to Data/Processed/Part/shortened_summaries.csv

    :return: an array containing processed summaries
    """
    books["Summary"] = books["Summary"]
    count = 0
    total = len(books["Summary"].index)
    new_summaries = []

    for summary in books["Summary"]:
        if str(summary) != "nan":
            standardised_summary = re.sub("\"", "", summary)
            standardised_summary = re.sub("[^a-zA-Z]", " ", standardised_summary)
            standardised_summary = " ".join(standardised_summary.split())
            standardised_summary = standardised_summary.lower()

            cleaned_summary = [w for w in standardised_summary.split() if w not in STOP_WORDS]

            new_summaries.append(" ".join(cleaned_summary))
        else:
            new_summaries.append("")

        count += 1
        print("{} out of {}".format(count, total))

    pd.DataFrame({"Summary": new_summaries}).to_csv("../data/Processed/Part/shortened_summaries.csv", header=True,
                                                    index=False)


books["Short_Summary"] = pd.read_csv("../Data/Processed/Part/shortened_summaries.csv")
books["Short_Summary"].replace("", np.nan, inplace=True)
books.dropna(inplace=True)
