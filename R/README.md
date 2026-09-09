# Data Analysis and Machine Learning in R

A collection of university projects exploring data analysis, visualization, clustering, classification, and regression in R. Each project combines code, plots, and written interpretations in a Quarto document.

The original reports and exercise descriptions are in Polish. This README provides an English overview of the collection.

## Files

Each project includes a `.qmd` source file and a rendered `.html` report containing the analysis and its outputs.

| Project | Source | Report | Focus |
| --- | --- | --- | --- |
| Movie data analysis | [Analiza Danych.qmd](Analiza%20Danych.qmd) | [Analiza Danych.html](Analiza%20Danych.html) | Data cleaning, exploratory queries, and visualization |
| Clustering | [R_Grupowanie.qmd](R_Grupowanie.qmd) | [R_Grupowanie.html](R_Grupowanie.html) | K-means and hierarchical clustering |
| Classification | [R_klasyfikacja.qmd](R_klasyfikacja.qmd) | [R_klasyfikacja.html](R_klasyfikacja.html) | Logistic regression and random forests |
| Regression | [R_regresja.qmd](R_regresja.qmd) | [R_regresja.html](R_regresja.html) | Linear regression, regression trees, and random forest tuning |

## Movie Data Analysis

An exploratory analysis of a Kaggle movie dataset, using **tidyverse** and **ggplot2** to investigate film characteristics and ratings.

- Inspects the dataset structure, summary statistics, and missing values.
- Removes records with missing runtime, score, or vote data.
- Finds the longest film, the highest-rated films within each genre, and highly rated Disney animated films.
- Visualizes movie runtimes with a histogram and rating distributions by genre with box plots.
- Explores the relationship between production budget and audience score using a scatter plot and fitted linear trend.

## Clustering

An unsupervised learning exercise grouping mammals by the composition of their milk. It uses the `all.mammals.milk.1956` dataset from **cluster.datasets**, supplemented with entries for humans, cows, goats, and cheetahs.

- Prepares and standardizes the numeric milk-composition variables.
- Applies **k-means clustering** with three clusters and multiple random starts.
- Examines cluster membership, including the group containing humans.
- Compares **hierarchical clustering** with complete, average, and single linkage using Euclidean distances.
- Visualizes the groups and dendrograms with **factoextra** and discusses similarities between mammals based on the selected features.

## Classification

A supervised learning project predicting credit status from the `credit_data` dataset in **modeldata**, using **tidymodels** to compare modeling workflows.

- Inspects missing data and the distribution of the target variable, `Status`.
- Creates a stratified 70/30 training and test split.
- Defines three preprocessing recipes: a baseline, mode imputation for selected categorical variables, and imputation followed by numeric normalization.
- Compares **logistic regression** and **random forest** models across the three recipes using five-fold cross-validation.
- Evaluates accuracy, ROC AUC, sensitivity, and specificity.
- Examines a selected model on the test set using a confusion matrix and performance metrics.
- Compares variable-importance plots for logistic regression and random forest models using **vip**.

## Regression

A study of sales prediction using the `Carseats` dataset from **ISLR2**, progressing from interpretable regression models to a tuned random forest.

- Plots sales against price with linear, quadratic, and cubic fitted curves.
- Fits a multiple linear regression model and interprets its coefficients and R².
- Builds and visualizes a **regression tree** using **rpart** and **rpart.plot**.
- Uses **tidymodels** and the **ranger** engine to tune a random forest on an 80/20 training and test split.
- Tests nine hyperparameter combinations: 100, 500, or 1,000 trees, paired with 3, 4, or 5 candidate predictors per split.
- Configures parallel processing with **future** and **doFuture** for tuning.
- Compares models using RMSE, MAE, and R², then evaluates the selected configuration on the held-out test set.

## Viewing and Running

To read the completed analyses, download the `.html` files and open them in a web browser. Running R is not required to view these reports.

To edit or rerun an analysis, open its `.qmd` file in an environment with **R** and **Quarto**, install the packages listed at the beginning of the document, and render it. 

The `movies.csf` dataset was downloaded from Kaggle website. The image that the `Clustering` file references was downloaded from internet.
