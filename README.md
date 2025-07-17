# U.S. Bereau of Labor Statistics API Project

## About

The prompt for this project as assigned was: "In any language you prefer, pull down at least two data sets from the Bureau of Labor Statistics API and visualize a compelling theory."

## Fearures and Scope

As I feel I have previously demonstarted some degree of ability to interface with and utilize API integration and navigation in previous use cases, I set out to add a small degree of complexity to the original prompt for the project. 
I have set out to create a Python visualizer in PowerBI that allows for a customized list of data sources form the BLS to be selected and populate a graph for visual comparison between Consumer Price Index data and Consumer Expenditure Survey data.
because of the different scale of data in the availabe series, all data metrics have been normalized to start at a '100' baseline, and the line graph visuals will demonstrate percentage based change in the series data for the time frame displayed.

## Notes on the project files

The Python script in the repo is a copy of the power BI python visualizer script. It does not serve the same dynamic function as a standalone script but it includes instructions to create a small graph as a demonstartion of the function.
Originally I had intentnions of comparing CPI data from the BLS to some internal data helpfully provided by the R&A team but the data sets were not as conducive as I had envisioned - thus the pivot to the CPI and CX data comparison. This is why the CPI data is focused on a Philadelphia based area specifically.

## Theory and Findings

The aim of comparing the CPI and CX survey data was to consider if there was a point where an **increase** in consumer costs for a product would manifest a **decrease** in customer expenditure, if a point of high cost would no longer be sustainable by the market. 
I was not able to find any data sets that supported this theory strongly, though I did not exhaustively compare all available data sets in the dataframe available inside this project.
