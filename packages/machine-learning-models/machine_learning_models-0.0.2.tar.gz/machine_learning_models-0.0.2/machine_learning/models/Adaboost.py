from machine_learning.src.Adaboost.AdaboostModel import Adaboost
from machine_learning.scores.get_scores import (get_classification_accurancy, get_mcc, get_sensitivity,
                                                get_specificity, get_precision, get_negative_predictive_value,
                                                display_confusion_matrix, ROC_plot)
from machine_learning.TitanicDatasetPreprocessing import get_data


def test_adaboost():
    X_train, X_test, y_train, y_test = get_data()
    model = Adaboost(100)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    # Evaluation
    accurancy = get_classification_accurancy(preds, y_test)
    mcc = get_mcc(preds, y_test)
    sensitivity = get_sensitivity(preds, y_test)
    specificity = get_specificity(preds, y_test)
    precision = get_precision(preds, y_test)
    negative_predictive_value = get_negative_predictive_value(preds, y_test)
    display_confusion_matrix(preds, y_test)
    print(f"Sensitivity with Adaboost: {sensitivity}")
    print(f"Specificity with Adaboost: {specificity}")
    print(f"Precision with Adaboost: {precision}")
    print(f"Negative prediction value with Adaboost: {negative_predictive_value}")
    print(f"Mcc with Adaboost: {mcc}")
    print(f"Accurancy with Adaboost: {accurancy}")
    ROC_plot(model, "Adaboost", X_test, y_test, X_train, y_train)
