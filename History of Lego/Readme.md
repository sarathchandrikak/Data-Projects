# 📍 Exploring the Evolution of Lego 

## ♦️ Case Study Description 

You are a Data Analyst at Lego working with the Sales/Customer Success teams. 
The Account Executive responsible for the Star Wars partnership has asked for specific information in preparation for their meeting with the Star Wars team. 
Although Star Wars was critical to the survival of the brand, Lego has since introduced a wide variety of licensed sets over subsequent years.

## ♦️ Questions to be addressed

1. What percentage of all licensed sets ever released were Star Wars themed? Save your answer as a variable the_force in the form of an integer (e.g. 25).

2. In which year was Star Wars not the most popular licensed theme (in terms of number of sets released that year)? Save your answer as a variable new_era in the form of an integer (e.g. 2012).

## ♦️ Dataset 

The Rebrickable database includes data on every LEGO set that has ever been sold; the names of the sets, what bricks they contain, what color the bricks are, etc. 

### 1. lego_sets.csv

set_num: A code that is unique to each set in the dataset. This column is critical, and a missing value indicates the set is a duplicate or invalid!\
set_name: A name for every set in the dataset (note that this can be the same for different sets).\
year: The date the set was released.\
num_parts: The number of parts contained in the set. This column is not central to our analyses, so missing values are acceptable.\
theme_name: The name of the sub-theme of the set.\
parent_theme: The name of the parent theme the set belongs to. Matches the name column of the parent_themes csv file.

### 2. parent_themes.csv

id: A code that is unique to every theme.\
name: The name of the parent theme.\
is_licensed: A Boolean column specifying whether the theme is a licensed theme.
