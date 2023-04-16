import re
import numpy as np
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords


rating_details = pd.read_csv("../Data/Processed/Part/rating_details.csv", encoding="cp1252", on_bad_lines="skip")
book_details = pd.read_csv("../Data/Processed/books_complete_details.csv")

age_cols = ["Under_17", "Under_30", "Under_45", "Over_45"]
countries = ["USA", "United Kingdom", "Australia", "New Zealand", "Canada"]

# Expanded stopwords with own observations
irrelevant_words = ["story" + "new", "quot", "story", "new", "york", "book", "times", "one", "author", "bestselling",
                    "life", "world", "first", "year", "author", "edition", "published", "novel", "school", "come",
                    "bestseller", "unforgettable"]
stop_words = set(stopwords.words('english') + irrelevant_words)


def stats(group, secondary, sample_size):
    if secondary:
        group_stats = rating_details.loc[rating_details[secondary] > 0]
        group_stats = group_stats[["ISBN", group]].sort_values(by=[group], ascending=False).head(sample_size)
    else:
        group_stats = rating_details[["ISBN", group]].sort_values(by=[group], ascending=False).head(sample_size)

    page_counts, categories, titles, all_synopsis = [], [], [], []

    for isbn in group_stats["ISBN"]:
        isbn_details = book_details.loc[book_details['ISBN'] == isbn]

        # NOTE: Temporary limitation due to isbn_details being incomplete
        if len(isbn_details) > 0:
            # Modified for easier processing later
            category = str(isbn_details["Categories"].values[0])
            category = category.translate(str.maketrans('', '', "[']"))  # Removing redundant characters
            synopsis_split = isbn_details["Summary"].values[0].split()  # Synopsis is used for most common words

            page_counts.append(isbn_details["Page_Count"])
            categories.append(category)
            all_synopsis += synopsis_split
            titles.append(isbn_details["Title"].values[0])

    categories = [x for x in categories if str(x) not in ['nan', "Fiction"]]  # Removing irrelevant categories
    all_synopsis = [word.capitalize() for word in all_synopsis]  # Ensuring all words start with capital letter

    avg_page_count = np.nanmean(page_counts).round()
    common_categories = Counter(categories).most_common(5)
    common_words = Counter(all_synopsis).most_common(5)
    common_titles = Counter(titles).most_common(5)

    return avg_page_count, common_categories, common_words, common_titles


def process_summary(summaries):
    count = 0
    total = len(summaries.index)
    new_summaries = []

    for summary in summaries:
        if str(summary) != "nan":
            standardised_summary = re.sub("\'", "", summary)
            standardised_summary = re.sub("[^a-zA-Z]", " ", standardised_summary)
            standardised_summary = ' '.join(standardised_summary.split())
            standardised_summary = standardised_summary.lower()

            cleaned_summary = [w for w in standardised_summary.split() if w not in stop_words]

            new_summaries.append(' '.join(cleaned_summary))
            count += 1
            print("{} out of {}".format(count, total))
        else:
            new_summaries.append("")

    return new_summaries


# NOTE: Required while still completing details
book_details["Summary"] = process_summary(book_details["Summary"])
