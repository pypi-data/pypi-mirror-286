from machine_learning.src.ExtremeGradientBoost.XGBoostModel import XGboost
from machine_learning.scores.get_scores import (get_classification_accurancy, get_mcc, get_sensitivity,
                                                get_specificity, get_precision, get_negative_predictive_value,
                                                display_confusion_matrix, get_regression_error, ROC_plot)
from machine_learning.GaltonFamiliesPreprocessing import get_regression_data
from machine_learning.TitanicDatasetPreprocessing import get_data


def test_xgboost_regression():
    # Regression
    X_train, X_test, y_train, y_test = get_regression_data()
    model = XGboost(trees_number=10, learning_rate=0.9, regularization_param=1,
                    prune_constant=1, max_depth=3)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    error = get_regression_error(preds, y_test)
    print("XGBoost with regression error: " + str(error))


def test_xgboost_classification():
    # Classification
    model = XGboost(trees_number=10, learning_rate=0.5, regularization_param=1, prune_constant=1,
                    max_depth=4, min_cover=0.5)
    X_train, X_test, y_train, y_test = get_data()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    # Evaluation
    accurancy = get_classification_accurancy(preds, y_test)
    mcc = get_mcc(preds, y_test)
    sensitivity = get_sensitivity(preds, y_test)
    specificity = get_specificity(preds, y_test)
    precision = get_precision(preds, y_test)
    negative_predictive_value = get_negative_predictive_value(preds, y_test)
    print("Classification:")
    display_confusion_matrix(preds, y_test)
    print(f"Sensitivity with XGBoost: {sensitivity}")
    print(f"Specificity with XGBoost: {specificity}")
    print(f"Precision with XGBoost: {precision}")
    print(f"Negative prediction value with XGBoost: {negative_predictive_value}")
    print(f"Mcc with XGBoost: {mcc}")
    print(f"Accurancy with XGBoost: {accurancy}")
    ROC_plot(model, "XGBoost", X_test, y_test)
