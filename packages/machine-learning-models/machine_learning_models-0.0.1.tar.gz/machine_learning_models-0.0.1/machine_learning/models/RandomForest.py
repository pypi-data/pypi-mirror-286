from machine_learning.src.RandomForest.Tree import DecisionTree
from machine_learning.src.RandomForest.RandomForestModel import RandomForest
from machine_learning.scores.get_scores import (get_classification_accurancy, get_mcc, get_sensitivity,
                                                get_specificity, get_precision, get_negative_predictive_value,
                                                display_confusion_matrix, ROC_plot)
from TitanicDatasetPreprocessing import get_data


X_train, X_test, y_train, y_test = get_data()
n_samples, n_features = X_train.shape
n = int(n_features**0.5)
num_trees = 150
max_samples = 10
max_depth = 4


def test_forest():
    forest = RandomForest(num_trees, n, max_samples, max_depth)
    forest.fit(X_train, y_train)
    preds = forest.predict(X_test)
    # Evaluation
    accurancy = get_classification_accurancy(preds, y_test)
    mcc = get_mcc(preds, y_test)
    sensitivity = get_sensitivity(preds, y_test)
    specificity = get_specificity(preds, y_test)
    precision = get_precision(preds, y_test)
    negative_predictive_value = get_negative_predictive_value(preds, y_test)
    print("Random Forest")
    display_confusion_matrix(preds, y_test)
    print(f"Sensitivity with Random Forest: {sensitivity}")
    print(f"Specificity with Random Forest: {specificity}")
    print(f"Precision with Random Forest: {precision}")
    print(f"Negative prediction value with Random Forest: {negative_predictive_value}")
    print(f"Mcc with Random Forest: {mcc}")
    print(f"Accurancy with Random Forest: {accurancy}")
    ROC_plot(forest, "Random Forest", X_test, y_test)


def test_tree():
    model = DecisionTree(n_features, max_samples, max_depth, single=True)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    # Evaluation
    accurancy = get_classification_accurancy(preds, y_test)
    mcc = get_mcc(preds, y_test)
    sensitivity = get_sensitivity(preds, y_test)
    specificity = get_specificity(preds, y_test)
    precision = get_precision(preds, y_test)
    negative_predictive_value = get_negative_predictive_value(preds, y_test)
    print("Decision Tree")
    display_confusion_matrix(preds, y_test)
    print(f"Sensitivity with Decision Tree: {sensitivity}")
    print(f"Specificity with Decision Tree: {specificity}")
    print(f"Precision with Decision Tree: {precision}")
    print(f"Negative prediction value with Decision Tree: {negative_predictive_value}")
    print(f"Mcc with Decision Tree: {mcc}")
    print(f"Accurancy with Decision Tree: {accurancy}")
    ROC_plot(model, "Decision Tree", X_test, y_test)
