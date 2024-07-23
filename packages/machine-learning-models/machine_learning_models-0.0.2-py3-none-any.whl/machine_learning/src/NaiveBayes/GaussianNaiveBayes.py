import numpy as np
from scipy.stats import norm


class GaussionNaiveBayes:
    def __init__(self):
        self.stds = None
        self.means = None
        self.classes_probabilities = None
        self.classes = None

    def get_mean_std(self, X: np.ndarray):
        return np.mean(X, axis=0), np.std(X, axis=0)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.classes, classes_counts = np.unique(y, return_counts=True)
        self.classes_probabilities = classes_counts/len(y)

        self.means = np.zeros(shape=(len(self.classes), X.shape[1]))
        self.stds = np.zeros(shape=(len(self.classes), X.shape[1]))

        for indx, cls in enumerate(self.classes):
            self.means[indx], self.stds[indx] = self.get_mean_std(X[y == cls])

    def single_predict(self, x: np.ndarray):
        probabilities = {}
        for class_index, cls in enumerate(self.classes):
            class_probability = self.classes_probabilities[class_index]
            log_probability = np.log(class_probability)
            for feature_index, xi in enumerate(x):
                mean = self.means[class_index][feature_index]
                std = self.stds[class_index][feature_index]
                log_probability += np.log(norm.pdf(xi, mean, std))
            probabilities[cls] = log_probability
        return probabilities
