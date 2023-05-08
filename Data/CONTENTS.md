# Folder Contents
This file contains the source for each file, meaning where it was generated and the contents of the file, referring to
the columns. More details about this process are available in the README.

## /Processed/Complete/
### Books_Complete_Details, Source: data_merging.py
Contents: ISBN, Title, Author, Year, Average Rating, Summary, Categories and Page Count

### Books_Rated, Source: data_merging.py
Contents: ISBN, Title, Author, Year, Average Rating

### User Demographics, Source: user_demographics.py
Contents: Country, Under 17, Under 30, Under 45, Under 60, Over 60, Total

## /Processed/Part/
### ISBN_Details, Source: get_details.py
Contents: ISBN, Summary, Categories and Page Count

### ISBN_Ratings, Source: average_ratings.py
Contents: ISBN, Average Rating

### Rating Details, Source: rating_stats.py
Contents: ISBN, Total_Users, Average Age, Countries

### Shortened Summaries, Source: item_stats.py
Contents: Summary

## /Stats/
Source for all these files is visualise_stats.py
### grouped_page_counts
Contents: Average page count per user for countries and age groups

### user_demographics
Contents: The total number of users belonging to an age group and country within the dataset

### /Stats/Ages/ and /Countries/
Contents: Both directories contain the most common authors, categories, titles and words for each group of their respective 
country/age

### /Stats/Countries and Ages/
Contents: The most common descriptors for all groups overall and the same statistics for each country and age group
