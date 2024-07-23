from machine_learning.src.GradientBoosting.GradientBoostingModel import GBoost
from machine_learning.TitanicDatasetPreprocessing import get_data
from machine_learning.GaltonFamiliesPreprocessing import get_regression_data
from machine_learning.scores.get_scores import (get_classification_accurancy, get_mcc, get_sensitivity,
                                                get_specificity, get_precision, get_negative_predictive_value,
                                                display_confusion_matrix, get_regression_error, ROC_plot)


def test_gboost_classification():
    # Classification
    X_train, X_test, y_train, y_test = get_data()
    model = GBoost(100, 0.1, 7, 10)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    # Model evaluation
    accurancy = get_classification_accurancy(preds, y_test)
    mcc = get_mcc(preds, y_test)
    sensitivity = get_sensitivity(preds, y_test)
    specificity = get_specificity(preds, y_test)
    precision = get_precision(preds, y_test)
    negative_predictive_value = get_negative_predictive_value(preds, y_test)
    print("Classification problem with GBoost:")
    display_confusion_matrix(preds, y_test)
    print(f"Sensitivity with GBoost: {sensitivity}")
    print(f"Specificity with GBoost: {specificity}")
    print(f"Precision with GBoost: {precision}")
    print(f"Negative prediction value with GBoost: {negative_predictive_value}")
    print(f"Mcc with GBoost: {mcc}")
    print("Classification problem with GBoost: " + str(accurancy) + " accurancy")
    ROC_plot(model, "GBoost", X_test, y_test)


def test_gboost_regression():
    # Regression
    X_train, X_test, y_train, y_test = get_regression_data()
    model = GBoost(10, 0.1, 5, 10)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    error = get_regression_error(preds, y_test)
    print("Regression problem with GBoost: " + str(error) + " error")
