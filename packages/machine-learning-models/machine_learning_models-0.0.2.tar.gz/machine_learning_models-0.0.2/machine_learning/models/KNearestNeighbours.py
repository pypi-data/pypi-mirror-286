from machine_learning.src.KNearestNeighbours.KNearestNeighboursModel import KNearestNeighbours
from machine_learning.TitanicDatasetPreprocessing import get_data
from machine_learning.scores.get_scores import (get_classification_accurancy, get_mcc, get_sensitivity,
                                                get_specificity, get_precision, get_negative_predictive_value,
                                                display_confusion_matrix, ROC_plot)


def test_knn():
    X_train, X_test, y_train, y_test = get_data()
    model = KNearestNeighbours(10)
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
    print(f"Sensitivity with K-nearest-neighbours: {sensitivity}")
    print(f"Specificity with K-nearest-neighbours: {specificity}")
    print(f"Precision with K-nearest-neighbours: {precision}")
    print(f"Negative prediction value with K-nearest-neighbours: {negative_predictive_value}")
    print(f"Mcc with K-nearest-neighbours: {mcc}")
    print(f"Accurancy with K-nearest-neighbours: {accurancy}")
    ROC_plot(model, "K-nearest-neighbours", X_test, y_test)
