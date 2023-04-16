from matplotlib import pyplot as plt
from item_stats import stats
import pandas as pd

# TODO:
#  -> Visualise descriptors for age groups and countries in one plot -> 5 age groups and 5 countries
#  -> Add sample sizes, lines, extra details (e.g. pie explode)
#  -> Update sample size implementation -> Allow use of "None" to do max samples


age_cols = ["Under_17", "Under_30", "Under_45", "Under_60", "Over_60"]
countries = ["USA", "United_Kingdom", "Australia", "New_Zealand", "Canada"]


def plot_grouped_page_counts(sample_size):
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

    plt.ylim(250, 450)  # Limits selected so all bars still visible whist maximising difference between bars
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=3)
    plt.show()


def plot_descriptors_for_group(group, country, descriptor, sample_size):
    if descriptor == "Categories":
        i = 1
    elif descriptor == "Words":
        i = 2
    else:
        i = 3

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

    plt.pie(counts, labels=stat_labels, autopct='%1.2f%%')

    plt.show()


def plot_user_demographics():
    rating_details = pd.read_csv("../Data/Processed/Part/user_stats.csv", on_bad_lines="skip")

    user_ages = rating_details[age_cols]
    user_countries = rating_details[countries + ["Other"]]

    plt.subplot(211)
    plt.title('User Demographics', y=1.08)
    user_ages.sum().plot.pie(pctdistance=1.35, autopct='%1.2f%%', labels=None)
    plt.legend(bbox_to_anchor=(1.30, 1), loc="upper left", labels=age_cols)
    plt.ylabel('Age Group', labelpad=30)

    plt.subplot(212)
    user_countries.sum().plot.pie(pctdistance=1.3, autopct='%1.2f%%', labels=None)
    plt.legend(bbox_to_anchor=(1.30, 1), loc="upper left", labels=countries + ["Other"])
    plt.ylabel('Country', labelpad=30)

    plt.show()


# plot_grouped_page_counts(50)
# plot_descriptors_for_group("Under_30", None, "Categories", 50)
# plot_descriptors_for_group("Under_45", "United_Kingdom", "Title", 50)
# plot_user_demographics()
