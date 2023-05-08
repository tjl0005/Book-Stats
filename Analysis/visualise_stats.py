"""
This file is used for producing visualisations showcasing stats compiled throughout this project as well as some figures
for the user details of the user base being explored.

All saved figure are stored within the Visualisations folder.
"""
from ast import literal_eval
from os import path
from get_item_stats import stats
from textwrap import wrap
from copy import copy
import matplotlib.pyplot as plt
import pandas as pd


USER_DEMOGRAPHICS = pd.read_csv("../Data/Stats/user_demographics.csv", index_col=False)
RATING_DEMOGRAPHICS = pd.read_csv("../Data/Processed/Part/rating_details.csv", index_col=False)
MAX_SAMPLE_SIZE = len(RATING_DEMOGRAPHICS.index)

COUNTRIES = ["USA", "United_Kingdom", "Australia", "New_Zealand", "Canada"]
AGES = ["Under_17", "Under_30", "Under_45", "Under_60", "Over_60"]

# True to generate new stat csvs and False to use existing files
GENERATING_STATS_CSV = False
# Used for pie charts
CENTRE_CIRCLE = plt.Circle((0, 0), 0.70, fc="white")


def plot_user_demographics():
    """
    Using user_demographics.csv plot the total number of users within each age group and country as a pie chart
    both groups are plotted within the same figure on separate pie charts.
    """
    # Getting last row which contains the total for each age group (Column)
    age_totals = USER_DEMOGRAPHICS.tail(1)
    age_totals = age_totals[["Under_17", "Under_30", "Under_45", "Under_60", "Over_60"]].values[0].tolist()
    # Getting final column which contains the totals for each country (Row)
    country_totals = USER_DEMOGRAPHICS[["Total"]]
    country_totals = country_totals[:-1].squeeze().tolist()

    plt.subplot(211)
    plt.pie(age_totals, pctdistance=1.3, autopct="%1.1f%%", explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.gca().add_artist(copy(CENTRE_CIRCLE))
    plt.legend(bbox_to_anchor=(1.30, 1), loc="upper left", labels=AGES, fancybox=True)
    plt.ylabel("Age Group", labelpad=30)

    plt.subplot(212)
    plt.pie(country_totals, pctdistance=1.3, autopct="%1.1f%%")
    plt.gca().add_artist(copy(CENTRE_CIRCLE))
    plt.legend(bbox_to_anchor=(1.30, 1), loc="upper left", labels=COUNTRIES + ["Other"], fancybox=True)
    plt.ylabel("Countries", labelpad=30)

    plt.suptitle("User Demographics")
    plt.savefig("../Visualisations/Demographics/User Demographics.png", dpi=300)


def plot_grouped_page_counts(sample_size):
    """
    Produces a grouped bar chart containing all COUNTRIES and age groups, showing for each of these groups (grouped by
    country) the average page counts for each reader.

    :param sample_size: The number of records to base the statistics of, can be set to None to poll entire dataset
    """
    if GENERATING_STATS_CSV:
        average_country_pages = {"USA": [], "United_Kingdom": [], "Australia": [], "New_Zealand": [], "Canada": []}

        for country in COUNTRIES:
            for age_group in AGES:
                page_count = stats(age_group, country, sample_size)[0]
                average_country_pages[country].append(page_count)

        average_country_pages_df = pd.DataFrame.from_dict(average_country_pages, orient="index", columns=AGES)
        average_country_pages_df.to_csv("../Data/Stats/grouped_page_counts.csv")
    else:
        average_country_pages_df = pd.read_csv("../Data/Stats/grouped_page_counts.csv", usecols=AGES)

    # Bars
    ax = average_country_pages_df.plot.bar(rot=0, xlabel="Age Group", ylabel="Page Count")
    # Average line
    average_country_pages_df.mean().plot(ax=ax, color="brown", linestyle="--", linewidth=3, label="Overall Average")

    ax.set_axisbelow(True)
    ax.yaxis.grid(color="gray", linestyle="dashed")
    plt.ylim(200, 375)  # Limits selected so all bars still visible whist maximising difference between bars
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=3, fancybox=True)
    # Remove spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.savefig("../Visualisations/Countries and Ages/Average Page Counts by Countries and Age.png", dpi=300)


def plot_country_demographics():
    """
    For each country plot a pie chart representing the breakdown of ages for all users within that country, this results
    in 5 pie charts (one for each country) and a legend showing colours for age groups as all colours are shared
    """
    age_totals = USER_DEMOGRAPHICS[["Under_17", "Under_30", "Under_45", "Under_60", "Over_60"]].drop([5, 6])
    # Colour dictionary for labels so legend is universal
    colours = {"Under_17": "tab:blue", "Under_30": "tab:orange", "Under_45": "tab:green", "Under_60": "tab:red",
               "Over_60": "tab:purple"}

    plt.figure(figsize=(20, 10), dpi=200)

    ax1 = plt.subplot2grid(shape=(2, 6), loc=(0, 0), colspan=2)
    ax1.pie(age_totals.loc[0].values.tolist(), autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in AGES],  # Applying colour dictionary
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(COUNTRIES[0], fontsize=15)  # This represents the title for this sub-chart
    plt.gca().add_artist(copy(CENTRE_CIRCLE))  # Aesthetic choice to have blank centre

    ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
    ax2.pie(age_totals.loc[1].values.tolist(), autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in AGES],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(COUNTRIES[1], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))

    ax3 = plt.subplot2grid((2, 6), (0, 4), colspan=2)
    ax3.pie(age_totals.loc[2].values.tolist(), autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in AGES],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(COUNTRIES[2], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))

    ax4 = plt.subplot2grid((2, 6), (1, 0), colspan=2)
    ax4.pie(age_totals.loc[3].values.tolist(), autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in AGES],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(COUNTRIES[3], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))

    ax5 = plt.subplot2grid((2, 6), (1, 2), colspan=2)
    ax5.pie(age_totals.loc[4].values.tolist(), autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in AGES],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(COUNTRIES[4], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))

    # Universal legend due to colour dictionary
    ax5.legend(colours, prop={"size": 20}, loc="center left", bbox_to_anchor=(1.6, 0.5), fancybox=True)

    plt.suptitle("Countries Demographics", fontsize=20)
    plt.savefig("../Visualisations/Demographics/Countries Demographics.png", dpi=300)


def plot_descriptors_for_group(primary_group, secondary_group, descriptor, sample_size):
    """
    Given a group and country (both optional) plot a descriptor (category or words) for that given subset
    :param primary_group: Primary age group or country
    :param secondary_group: Secondary age group or country
    :param descriptor: Main statistic, either most common word or country
    :param sample_size: The number of records to base the statistics of, can be set to None to poll entire dataset
    """
    if descriptor == "Categories":
        i = 1
    elif descriptor == "Words":
        i = 2
    else:
        i = 3

    fig1, ax1 = plt.subplots()

    # Figure out the title and directory for the final figure
    if primary_group:
        title = "Most Common {} for {}".format(descriptor, primary_group)

        if primary_group == AGES:
            directory = "Ages"
        else:
            directory = "Countries"
    elif secondary_group:
        title = "Most Common {} for {} in {}".format(descriptor, primary_group, secondary_group)
        directory = "Countries and Ages"
    else:
        title = "Most Common {} For All Groups".format(descriptor)
        directory = "Countries and Ages"

    if GENERATING_STATS_CSV:
        # New dataframe with columns named uniquely
        current_descriptor_df = pd.DataFrame(stats(primary_group, secondary_group, sample_size)[i],
                                             columns=[descriptor, "{}_Count".format(descriptor)])

        # Check if stats already exist, if so append to this file
        if path.isfile("../data/Stats/{}/most_common_descriptors.csv".format(directory)):
            try:
                current_stats = pd.read_csv("../data/Stats/{}/most_common_descriptors.csv".format(directory))
                current_stats = current_stats.join(current_descriptor_df)
                current_stats.to_csv("../data/Stats/{}/most_common_descriptors.csv".format(directory), index=False)
            except ValueError:
                print("Unable to append to file, it may already be populated with requested data. No changes made.")
        else:  # Initial save
            current_descriptor_df.to_csv("../Data/Stats/{}/most_common_descriptors.csv".format(directory),
                                         index=False)

    # Open stored stats and retrieve relevant descriptor and their counts
    stat_details = pd.read_csv("../data/Stats/{}/most_common_descriptors.csv".format(directory))
    stat_labels = stat_details[descriptor]
    counts = stat_details["{}_Count".format(descriptor)]

    ax1.pie(counts, labels=stat_labels, autopct="%1.1f%%", pctdistance=0.8, startangle=90, explode=(0.05, 0.05, 0.05,
                                                                                                    0.05, 0.05))
    fig = plt.gcf()
    fig.gca().add_artist(copy(CENTRE_CIRCLE))

    plt.title(title)
    plt.savefig("../Visualisations/{}/{}.png".format(directory, title), dpi=300)


def plot_descriptors_for_all_groups(primary_groups, secondary_group, descriptor, sample_size):
    """
    Given a list of groups e.g. Ages, plot all the most common given descriptors for each element of that group

    :param primary_groups: Ages or Countries to be used
    :param secondary_group: Age or Countries to be used
    :param descriptor: Main statistic, either most common word, category or title
    :param sample_size: The number of records to base the statistics of, can be set to None to poll entire dataset
    """
    # Potentially share colours for common labels
    if descriptor == "Categories":
        i = 1
    elif descriptor == "Words":
        i = 2
    elif descriptor == "Titles":
        i = 3
    else:
        i = 4

    if secondary_group:
        title = "Most Common {} For {}".format(descriptor, secondary_group)
        directory = "Countries and Ages/{}".format(secondary_group.replace("_", " "))
    elif primary_groups == AGES:
        title = "Most Common {} by Age Group".format(descriptor)
        directory = "Ages"
    else:
        title = "Most Common {} by Countries".format(descriptor)
        directory = "Countries"

    group_labels, group_counts = [], []

    if GENERATING_STATS_CSV:
        for group in primary_groups:
            stat_labels, counts = [], []

            stat_details = stats(group, secondary_group, sample_size)[i]

            for details in stat_details:
                stat_label = details[0]
                count = details[1]

                stat_labels.append(stat_label)
                counts.append(count)

            stat_labels = ["\n".join(wrap(label, 20)) for label in stat_labels]
            group_labels.append(stat_labels)
            group_counts.append(counts)

        current_descriptor_df = pd.DataFrame([group_labels, group_counts], columns=primary_groups)
        current_descriptor_df.to_csv("../Data/Stats/{}/{}.csv".format(directory, title), index=False)
    else:
        df = pd.read_csv("../Data/Stats/{}/{}.csv".format(directory, title))

        for i in range(len(df.columns)):
            group_labels.append(literal_eval(df.iloc[0].values[i]))
            group_counts.append(literal_eval(df.iloc[1].values[i]))

    plt.figure(figsize=(20, 10), dpi=200)

    ax1 = plt.subplot2grid(shape=(2, 6), loc=(0, 0), colspan=2)
    ax1.pie(group_counts[0], labels=group_labels[0], autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(primary_groups[0], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))

    ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
    ax2.pie(group_counts[1], labels=group_labels[1], autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(primary_groups[1], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))

    ax3 = plt.subplot2grid((2, 6), (0, 4), colspan=2)
    ax3.pie(group_counts[2], labels=group_labels[2], autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(primary_groups[2], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))

    ax4 = plt.subplot2grid((2, 6), (1, 1), colspan=2)
    ax4.pie(group_counts[3], labels=group_labels[3], autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(primary_groups[3], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))

    ax5 = plt.subplot2grid((2, 6), (1, 3), colspan=2)
    ax5.pie(group_counts[4], labels=group_labels[4], autopct="%1.1f%%", pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(primary_groups[4], fontsize=15)
    plt.gca().add_artist(copy(CENTRE_CIRCLE))
    plt.tight_layout()

    plt.suptitle(title, fontsize=20)

    plt.savefig("../Visualisations/{}/{}.png".format(directory, title), dpi=300)


def plot_all():
    """
    Plot all potential plots
    """
    # Single call plots
    # plot_user_demographics()
    # plot_country_demographics()
    # print("O of 13")
    plot_grouped_page_counts(MAX_SAMPLE_SIZE)
    #
    # print("1 of 13")
    # plot_descriptors_for_group(None, None, "Titles", MAX_SAMPLE_SIZE)
    # print("2 of 13")
    # plot_descriptors_for_group(None, None, "Words", MAX_SAMPLE_SIZE)
    # print("3 of 13")
    # plot_descriptors_for_group(None, None, "Categories", MAX_SAMPLE_SIZE)
    # print("4 of 13")
    # plot_descriptors_for_group(None, None, "Authors", MAX_SAMPLE_SIZE)
    # print("5 of 13")
    #
    # plot_descriptors_for_all_groups(AGES, None, "Categories", MAX_SAMPLE_SIZE)
    # print("6 of 13")
    # plot_descriptors_for_all_groups(AGES, None, "Words", MAX_SAMPLE_SIZE)
    # print("7 of 13")
    # plot_descriptors_for_all_groups(AGES, None, "Titles", MAX_SAMPLE_SIZE)
    # print("8 of 13")
    # plot_descriptors_for_all_groups(AGES, None, "Authors", MAX_SAMPLE_SIZE)
    # print("9 of 13")
    # plot_descriptors_for_all_groups(COUNTRIES, None, "Categories", MAX_SAMPLE_SIZE)
    # print("10 of 13")
    # plot_descriptors_for_all_groups(COUNTRIES, None, "Words", MAX_SAMPLE_SIZE)
    # print("11 of 13")
    # plot_descriptors_for_all_groups(COUNTRIES, None, "Titles", MAX_SAMPLE_SIZE)
    # print("12 of 13")
    # plot_descriptors_for_all_groups(COUNTRIES, None, "Authors", MAX_SAMPLE_SIZE)
    # print("13 of 13")
    #
    # print("Single call plots completed.")
    #
    # # Multiple call plots
    # for country in COUNTRIES:
    #     plot_descriptors_for_all_groups(AGES, country, "Categories", MAX_SAMPLE_SIZE)
    #     plot_descriptors_for_all_groups(AGES, country, "Words", MAX_SAMPLE_SIZE)
    #     plot_descriptors_for_all_groups(AGES, country, "Titles", MAX_SAMPLE_SIZE)
    #     plot_descriptors_for_all_groups(AGES, country, "Authors", MAX_SAMPLE_SIZE)
    #     print("{} plots completed".format(country))
    #
    # print("Multiple call plots completed.")


plot_all()
