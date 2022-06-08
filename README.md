Used Car price prediction on the Hungarian used car database in python with a tkinter interface

1.	Scraping the used car market database
First of all, I needed to actually get the database, which I wanted to work with. This was scraped from the following website: https://www.hasznaltauto.hu/  with python and it’s scrapy library. 
the database consists around the data of 70000 car. 

2.	Pre-processing
The database has 22 explaining variable for each car, so it required a lot of pre-processing. Mainly just manipulating the data so it is usable for regression, also I dropped two columns one had all missing values, the other one was the price variable in Forint, which is redundant, because I wanted to work with the Euro price variable.

3.	 The regression
I am using multiple linear regression only (it is the plan to try it with different machine learning techniques such as neural network, random forests). In this analysis I am focusing solely on the predictive power of the model, so I tried a few different setups, but I got the best predictive model (without overfitting), if I just almost put the raw data into the regression, the only adjustments that I made was transforming the price variable with log transformation, because it had a significant right skew, also for now I dropped all of the rows with missing values, I tried filling up them with mode or median but it reduced the predictive power, and the case was similar with  the outliers. 
The results on the test data were an R_squared of 94,8%.

4.	The interface
Next part of the project was making an interface, where you can write in your car’s details and it will tell you it’s worth and also it will tell you some other interesting facts, such as how many similar*cars is on the Hungarian used car market, also how much of those average price, furthermore it can tell you interesting facts about the explaining variables which you have given.
I made this interface with python’s tkinter library



Important notes:
-	The prices were predicted based on the Hungarian market and it’s prices, so it may not be accurate for other countries
-	In the code the variable names are mainly written in Hungarian, 

Currently working on:
-	Handling the missing values differently
-	Making the prediction with other machine learning models
-	making the code and interface full English
-	documenting the code more
Balázs Zupkó, 2022. 06. 08.
