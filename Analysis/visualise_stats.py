"""
This file is used for producing visualisations showcasing stats compiled throughout this project as well as some figures
for the demographics of the user base being explored.

All saved figure are stored within the Visualisations folder.
"""
import matplotlib.pyplot as plt
from item_stats import stats
from copy import copy
import pandas as pd


age_cols = ["Under_17", "Under_30", "Under_45", "Under_60", "Over_60"]
countries = ["USA", "United_Kingdom", "Australia", "New_Zealand", "Canada"]

centre_circle = plt.Circle((0, 0), 0.70, fc='white')


def plot_grouped_page_counts(sample_size):
    """
    Produces a grouped bar chart containing all countries and age groups, showing for each of these groups (grouped by
    country) the average page counts for each reader.

    :param sample_size: The number of records to base the statistics of, can be set to None to poll entire dataset
    """
    country_ages = {"USA": [], "United_Kingdom": [], "Australia": [], "New_Zealand": [], "Canada": []}
    average_pages = {"Under_17": [], "Under_30": [], "Under_45": [], "Under_60": [], "Over_60": []}

    for country in countries:
        for age_group in age_cols:
            page_count = stats(age_group, country, sample_size)[0]

            country_ages[country].append(page_count)
            average_pages[age_group].append(page_count)

    country_pages_df = pd.DataFrame(country_ages)
    age_pages_df = pd.DataFrame(average_pages)

    ax = country_pages_df.plot.bar(rot=0, xlabel="Age Group", ylabel="Page Count")
    # Average line
    age_pages_df.mean().plot(ax=ax, color='brown', linestyle='--', linewidth=3, label='Overall Average')

    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    plt.ylim(250, 450)  # Limits selected so all bars still visible whist maximising difference between bars
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=3)

    # plt.savefig("../Visualisations/page_counts_by_age_and_country.png")
    plt.show()


def plot_descriptors_for_group(group, country, descriptor, sample_size):
    """
    Given a group and country (latter is optional) plot a descriptor (category or words) for that given subset

    :param group: Primary age group or country
    :param country: Secondary age group or country
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

    if country:
        stat_details = stats(group, country, sample_size)[i]
        plt.title("Most Common {} for {} in {}".format(descriptor, group, country))
    else:
        stat_details = stats(group, None, sample_size)[i]
        plt.title("Most Common {} for {}".format(descriptor, group))

    stat_labels = []
    counts = []

    for details in stat_details:
        stat_label = details[0]
        count = details[1]

        stat_labels.append(stat_label)
        counts.append(count)

    ax1.pie(counts, labels=stat_labels, autopct='%1.1f%%', pctdistance=0.8, startangle=90, explode=(0.05, 0.05, 0.05,
                                                                                                    0.05, 0.05))
    fig = plt.gcf()
    fig.gca().add_artist(copy(centre_circle))

    plt.show()


def plot_descriptors_for_all_groups(groups, descriptor, sample_size):
    """
    Given a list of groups e.g. Ages, plot all the most common given descriptors for each element of that group

    :param groups: Ages or Countries to be used
    :param descriptor: Main statistic, either most common word or country
    :param sample_size: The number of records to base the statistics of, can be set to None to poll entire dataset
    """
    # Potentially share colours for common labels
    if descriptor == "Categories":
        i = 1
    elif descriptor == "Words":
        i = 2
    else:
        i = 3

    group_labels = []
    group_counts = []

    for group in groups:
        stat_labels = []
        counts = []
        stat_details = stats(group, None, sample_size)[i]

        for details in stat_details:
            stat_label = details[0]
            count = details[1]

            stat_labels.append(stat_label)
            counts.append(count)

        group_labels.append(stat_labels)
        group_counts.append(counts)

    plt.figure(figsize=(20, 10), dpi=200)

    ax1 = plt.subplot2grid(shape=(2, 6), loc=(0, 0), colspan=2)
    ax1.pie(group_counts[0], labels=group_labels[0], autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(groups[0])
    plt.gca().add_artist(copy(centre_circle))

    ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
    ax2.pie(group_counts[1], labels=group_labels[1], autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(groups[1])
    plt.gca().add_artist(copy(centre_circle))

    ax3 = plt.subplot2grid((2, 6), (0, 4), colspan=2)
    ax3.pie(group_counts[2], labels=group_labels[2], autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(groups[2])
    plt.gca().add_artist(copy(centre_circle))

    ax4 = plt.subplot2grid((2, 6), (1, 1), colspan=2)
    ax4.pie(group_counts[3], labels=group_labels[3], autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(groups[3])
    plt.gca().add_artist(copy(centre_circle))

    ax5 = plt.subplot2grid((2, 6), (1, 3), colspan=2)
    ax5.pie(group_counts[4], labels=group_labels[4], autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(groups[4])
    plt.gca().add_artist(copy(centre_circle))
    plt.tight_layout()

    if groups == age_cols:
        plt.suptitle("Most Common {} by Age Group".format(descriptor))
        # plt.savefig("Most_Common_{}_by_Age Group".format(descriptor))

    else:
        plt.suptitle("Most Common {} by Country".format(descriptor))
        # plt.savefig("Most_Common_{}_by_Country".format(descriptor))

    plt.show()


def plot_user_demographics():
    """
    Using the file user_demographics.csv plot the total number of users within each age group and country as a pie chart
    both groups are plotted within the same figure on separate pie charts.
    """
    rating_details = pd.read_csv("../Data/Processed/user_demographics.csv", on_bad_lines="skip", index_col=False)

    age_totals = rating_details.tail(1)
    age_totals = age_totals[["Under_17", "Under_30", "Under_45", "Under_60", "Over_60"]].values[0].tolist()

    country_totals = rating_details[["Total"]]
    country_totals = country_totals[:-1].squeeze().tolist()

    plt.subplot(211)
    plt.title('User Demographics', y=1.08)
    plt.pie(age_totals, pctdistance=1.3, autopct='%1.1f%%', explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.gca().add_artist(copy(centre_circle))
    plt.legend(bbox_to_anchor=(1.30, 1), loc="upper left", labels=age_cols)
    plt.ylabel('Age Group', labelpad=30)

    plt.subplot(212)
    plt.pie(country_totals, pctdistance=1.3, autopct='%1.1f%%')
    plt.gca().add_artist(copy(centre_circle))
    plt.legend(bbox_to_anchor=(1.30, 1), loc="upper left", labels=countries + ["Other"])
    plt.ylabel('Country', labelpad=30)

    plt.show()
    # plt.savefig("../Visualisations/user_demographics.png")


def plot_age_demographics():
    """
    For each country plot a pie chart representing the breakdown of ages for all users within that country, this results
    in 5 pie charts (one for each country) and a legend showing colours for age groups as all colours are shared
    """
    rating_details = pd.read_csv("../Data/Processed/user_demographics.csv", on_bad_lines="skip", index_col=False)
    age_totals = rating_details[["Under_17", "Under_30", "Under_45", "Under_60", "Over_60"]].drop([5, 6])

    colours = {"Under_17": "tab:blue", "Under_30": "tab:orange", "Under_45": "tab:green", "Under_60": "tab:red",
               "Over_60": "tab:purple"}

    plt.figure(figsize=(20, 10), dpi=200)

    ax1 = plt.subplot2grid(shape=(2, 6), loc=(0, 0), colspan=2)
    ax1.pie(age_totals.loc[0].values.tolist(), autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in age_cols],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(countries[0])
    plt.gca().add_artist(copy(centre_circle))

    ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
    ax2.pie(age_totals.loc[1].values.tolist(), autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in age_cols],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(countries[1])
    plt.gca().add_artist(copy(centre_circle))

    ax3 = plt.subplot2grid((2, 6), (0, 4), colspan=2)
    ax3.pie(age_totals.loc[2].values.tolist(), autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in age_cols],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(countries[2])
    plt.gca().add_artist(copy(centre_circle))

    ax4 = plt.subplot2grid((2, 6), (1, 0), colspan=2)
    ax4.pie(age_totals.loc[3].values.tolist(), autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in age_cols],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(countries[3])
    plt.gca().add_artist(copy(centre_circle))

    ax5 = plt.subplot2grid((2, 6), (1, 2), colspan=2)
    ax5.pie(age_totals.loc[4].values.tolist(), autopct='%1.1f%%', pctdistance=0.8, startangle=90,
            colors=[colours[key] for key in age_cols],
            explode=(0.05, 0.05, 0.05, 0.05, 0.05))
    plt.xlabel(countries[4])
    plt.gca().add_artist(copy(centre_circle))

    ax5.legend(colours, prop={'size': 20}, loc='center left', bbox_to_anchor=(1.6, 0.5))

    plt.suptitle("Country Demographics")
    plt.show()
    # plt.savefig("../Visualisations/country_demographics.png")


# plot_grouped_page_counts(50)
# plot_descriptors_for_group("Under_30", None, "Categories", 50)
# plot_descriptors_for_group("Under_45", "United_Kingdom", "Title", 50)
# plot_descriptors_for_all_groups(age_cols, "Categories", 50)
# plot_user_demographics()
# plot_age_demographics()
