# Farmer's Market Expansion

You have been hired by a farming organisation that helps local farmers sell their products. They want to know whether they should open up a new farmers' market to sell dairy products from nearby farmers. They have supplied you with daily shopping data from a panel of local households from 2019 to 2020.

The organization will make their decision based on whether dairy products are popular in the area, and whether sales are trending in a positive direction. To answer these questions, they want three pieces of data:

What was the total number of purchases of dairy products for each month of 2020 (i.e., the total_sales)?
What was the total share of dairy products (out of all products purchased) for each month of 2020 (i.e., the market_share)?
For each month of 2020, what was the percentage increase or decrease in total monthly dairy purchases compared to the same month in 2019 (i.e., the year_change)?
The organization handles not only dairy farmers, but also those with chicken farms. As a result, they are only interested in these three categories (which they treat as dairy): ‘whole milk’, 'yogurt' and 'domestic eggs'.

The data you need is available in the tables shown in the database schema below.

Database Schema 

![farmerschema](https://user-images.githubusercontent.com/65502906/155457771-8ecb4af0-a832-4583-9b03-ac034cfc6fc3.png)

(In this table name is purchases_2020)

Order your query by month in ascending order. Both month and total_sales should be expressed as integers, and market_share and year_change should be percentages rounded to two decimal places (e.g., 27.95% becomes 27.95).
