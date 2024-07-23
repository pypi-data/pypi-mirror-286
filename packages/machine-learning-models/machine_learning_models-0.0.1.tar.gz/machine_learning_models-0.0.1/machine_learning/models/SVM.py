from machine_learning.src.SVM.SvmModel import PrimalSVM, SVM
from machine_learning.scores.get_scores import (get_classification_accurancy, get_mcc, get_sensitivity,
                                                get_specificity, get_precision, get_negative_predictive_value,
                                                display_confusion_matrix)
from machine_learning.TitanicDatasetPreprocessing import get_data
import numpy as np


X_train, X_test, y_train, y_test = get_data()


def test_dual_svm():
    kernel = "polynomial"
    model = SVM(r=1, d=2, sigma=2, regularization_param=1, kernel=kernel)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    preds = np.where(preds == -1, 0, 1)
    # Evaluation
    accurancy = get_classification_accurancy(preds, y_test)
    mcc = get_mcc(preds, y_test)
    sensitivity = get_sensitivity(preds, y_test)
    specificity = get_specificity(preds, y_test)
    precision = get_precision(preds, y_test)
    negative_predictive_value = get_negative_predictive_value(preds, y_test)
    print(f"SVM in dual form with kernels (kernel is {kernel})")
    display_confusion_matrix(preds, y_test)
    print(f"Sensitivity with SVM: {sensitivity}")
    print(f"Specificity with SVM: {specificity}")
    print(f"Precision with SVM: {precision}")
    print(f"Negative prediction value with SVM: {negative_predictive_value}")
    print(f"Mcc with SVM: {mcc}")
    print(f"Accurancy with SVM: {accurancy}")


def test_primal_svm():
    model = PrimalSVM(2, 10, 0.1)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    preds = np.where(preds == -1, 0, 1)
    # Evaluation
    accurancy = get_classification_accurancy(preds, y_test)
    mcc = get_mcc(preds, y_test)
    sensitivity = get_sensitivity(preds, y_test)
    specificity = get_specificity(preds, y_test)
    precision = get_precision(preds, y_test)
    negative_predictive_value = get_negative_predictive_value(preds, y_test)
    print("SVM in primal form without kernels")
    display_confusion_matrix(preds, y_test)
    print(f"Sensitivity with SVM: {sensitivity}")
    print(f"Specificity with SVM: {specificity}")
    print(f"Precision with SVM: {precision}")
    print(f"Negative prediction value with SVM: {negative_predictive_value}")
    print(f"Mcc with SVM: {mcc}")
    print(f"Accurancy with SVM: {accurancy}")
