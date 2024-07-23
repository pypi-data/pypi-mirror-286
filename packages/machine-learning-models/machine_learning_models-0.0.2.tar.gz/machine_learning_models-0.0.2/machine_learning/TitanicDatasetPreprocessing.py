import pandas as pd
import numpy as np
import os
from importlib import resources
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.model_selection import train_test_split


def fill_missing_data(df: pd.DataFrame):
    num_imputer = KNNImputer()
    df["Age"] = num_imputer.fit_transform(df[["Age"]])
    obj_imputer = SimpleImputer(strategy="most_frequent")
    df["Embarked"] = obj_imputer.fit_transform(df[["Embarked"]]).ravel()


def wisker(df_column: pd.Series):
    q1, q3 = np.percentile(df_column, [25, 75])
    return q1 - 1.5*(q3 - q1), q3 + 1.5*(q3 - q1)


def eliminate_outliers(df: pd.DataFrame):
    for column in ["Age", "Fare"]:
        lw, uw = wisker(df[column])
        df[column] = np.where(df[column] < lw, lw, df[column])
        df[column] = np.where(df[column] > uw, uw, df[column])


def encoding(df: pd.DataFrame):
    map_dict_sex = {"male": 0, "female": 1}
    df["Sex"] = df["Sex"].map(lambda x: map_dict_sex[x])
    map_dict_embarked = {"S": 0, "C": 2, "Q": 3}
    df["Embarked"] = df["Embarked"].map(lambda x: map_dict_embarked[x])
    map_dict_ticket = {}
    count = 0
    for value in df["Ticket"].unique():
        map_dict_ticket[value] = count
        count += 1
    df["Ticket"] = df["Ticket"].map(lambda x: map_dict_ticket[x])


def get_data():
    df = load_csv_data()
    # df = pd.read_csv(os.path.join("machine_learning", "data", "train.csv"))
    fill_missing_data(df)
    eliminate_outliers(df)
    df = df.drop(columns=["PassengerId", "Name", "Fare", "Cabin"])
    encoding(df)
    y = df["Survived"].to_numpy()
    X = df.drop(columns=["Survived"]).to_numpy()
    return train_test_split(X, y, test_size=0.2, random_state=42)


def load_csv_data():
    with resources.open_text('machine_learning.data', 'train.csv') as file:
        df = pd.read_csv(file)
    return df