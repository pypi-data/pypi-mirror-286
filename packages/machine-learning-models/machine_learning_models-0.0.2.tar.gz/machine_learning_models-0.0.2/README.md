# About this repo
This repository contains my own implementations of the most popular machine learning models. It also has scripts for data preproccessing (datasets titanic and GaltonFamilies). For classification, I implemented my own class for nested cross validation. There are functions to evaluate model using confusion matrix (calculating accurancy, sensitivity, specificity, precision etc.) as well as to draw ROC curve.

# Note
All of the models and validation were implemented by myslef, without using sklearn library. They were done for learning purposes. There is a seperate file named sklearn.py, in which I focused on exploring sklearn library

# Models in this repo
1) Linear models
- Linear Regression
- Logistic Regression
2) Trees
- Regression Tree
- Decision Tree
- Random Forest
3) Boosting
- Adaboost
- Gradient boosting
- Extreme Gradient Boosting
4) SVM
- SVM primal bez jądra
- SVM dual z jądrem
5) Naive Bayes
6) K-nearest-neighbours

# Python package
This repo can be installed as a package via command
```python
pip install machine-learning-models
```
1) Using only models
```python
# Adaboost
from machine_learning.src.Adaboost.AdaboostModel import Adaboost
# XGBoost
from machine_learning.src.ExtremeGradinetBoost.XGBoostModel import XGBoost
# Gboost
from machine_learning.src.GradientBoosting.GradientBoostingModel import GBoost
# KNN
from machine_learning.src.KNearestNeighbours.KNearestNeighboursModel import KNearestNeighbours
# Linear Regression
from machine_learning.src.LinearRegression.LinearRegressionModel import LinearRegressionModel
# Logistic Regression
from machine_learning.src.LogisticRegression.LogisticRegressionModel import LogisticRegression
# Naive Bayes
from machine_learning.src.NaiveBayes.NaiveBayesModel import NaiveBayes
# Random Forest
from machine_learning.src.RandomForest.RandomForestModel import RandomForest
# DEcision and Regression Tree
from machine_learning.src.RandomForest.Tree import DecisionTree
from machine_learning.src.RegressionTree.RegressionTreeModel import RegressionTree
# SVM
from machine_learning.src.SVM.SvmModel import SVM
from machine_learning.src.SVM.SvmModel import PrimalSVM
```
#### Author
Małgorzata Grzanka
