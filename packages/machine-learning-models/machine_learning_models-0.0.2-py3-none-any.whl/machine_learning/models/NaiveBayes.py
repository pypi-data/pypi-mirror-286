from machine_learning.src.NaiveBayes.NaiveBayesModel import NaiveBayes
from machine_learning.scores.get_scores import (get_classification_accurancy, get_mcc, get_sensitivity,
                                                get_specificity, get_precision, get_negative_predictive_value,
                                                display_confusion_matrix, ROC_plot)
from machine_learning.TitanicDatasetPreprocessing import get_data


def test_naive_bayes():
    X_train, X_test, y_train, y_test = get_data()
    model = NaiveBayes()
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
    print(f"Sensitivity with Naive Bayes: {sensitivity}")
    print(f"Specificity with Naive Bayes: {specificity}")
    print(f"Precision with Naive Bayes: {precision}")
    print(f"Negative prediction value with Naive Bayes: {negative_predictive_value}")
    print(f"Mcc with Naive Bayes: {mcc}")
    print(f"Accurancy with Naive Bayes: {accurancy}")
    ROC_plot(model, "Naive Bayes", X_test, y_test)
