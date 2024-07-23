import numpy as np
import matplotlib.pyplot as plt


def get_regression_error(preds, Y):
    n = len(preds)
    return sum([(pred-y)**2 for pred, y in zip(preds, Y)])/n


def confusion_matrix(preds: np.ndarray, y: np.ndarray):
    preds = np.array(preds)
    tp = np.sum((y == 1) & (preds == 1))
    fp = np.sum((y == 0) & (preds == 1))
    tn = np.sum((y == 0) & (preds == 0))
    fn = np.sum((y == 1) & (preds == 0))
    return tp, fp, tn, fn


def get_sensitivity(preds, y):
    """what percentage of posivites was correctly classified"""
    tp, fp, tn, fn = confusion_matrix(preds, y)
    return tp/(tp+fn)


def get_specificity(preds, y):
    """what percentage of negatives was correctly classified"""
    tp, fp, tn, fn = confusion_matrix(preds, y)
    return tn / (tn + fp)


def get_precision(preds, y):
    """what percentage of predicted positives are really positives"""
    tp, fp, tn, fn = confusion_matrix(preds, y)
    return tp / (tp + fp)


def get_negative_predictive_value(preds, y):
    """what percentage of predicted negatives are really negatives"""
    tp, fp, tn, fn = confusion_matrix(preds, y)
    return tn / (tn + fn)


def get_classification_accurancy(preds, y):
    """what percentage of samples were correctly classified"""
    tp, fp, tn, fn = confusion_matrix(preds, y)
    return (tp + tn) / (tp + fp + tn + fn)


def get_mcc(preds, y):
    """Matthews Correlation Coefficient"""
    tp, fp, tn, fn = confusion_matrix(preds, y)
    numerator = (tp*tn) - (fp*fn)
    denominator = ((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))**0.5
    return numerator / denominator


def display_confusion_matrix(preds, y):
    tp, fp, tn, fn = confusion_matrix(preds, y)
    print(f"|tp: {tp}|fp: {fp}|\n|fn: {fn}|tn: {tn}|")


def ROC_plot(model, model_name: str, X_test: np.ndarray, y_test: np.ndarray, X_train=None, y_train=None):
    tresholds = np.arange(0.0, 1.1, 0.1)
    sensitivities = np.zeros(len(tresholds))
    FPRs = np.zeros(len(tresholds))
    for indx, treshold in enumerate(tresholds):
        if model_name == "Adaboost":
            model.fit(X_train, y_train, treshold, print_progress=False)
        preds = model.predict(X_test, treshold)
        tp, fp, tn, fn = confusion_matrix(preds, y_test)
        sensitivities[indx] = tp/(tp + fn)
        FPRs[indx] = fp / (fp + tn)
    sorted_indices = np.argsort(FPRs)
    sorted_FPRs = FPRs[sorted_indices]
    sorted_sensitivities = sensitivities[sorted_indices]
    auc = np.trapz(y=sorted_sensitivities, x=sorted_FPRs)
    plt.plot(FPRs, sensitivities, label=f"{model_name} AUC: {auc:.2f}")
    plt.title("ROC graph")
    plt.ylabel("Sensitivity (true positive rate)")
    plt.xlabel("FPR (false positive rate)")
    plt.legend()
    plt.show()
