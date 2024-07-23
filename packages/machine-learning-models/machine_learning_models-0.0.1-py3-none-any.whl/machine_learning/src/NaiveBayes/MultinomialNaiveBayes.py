import numpy as np


class MultinomialNaiveBayes:
    def __init__(self):
        self.columns_probabilities = []
        self.classes_probabilities = None
        self.classes = None

    def get_columns_probabilities(self, X: np.ndarray):
        n_samples, n_features = X.shape
        columns_probabilities = []
        for column_index in range(n_features):
            values, counts = np.unique(X[:, column_index], return_counts=True)
            columns_probabilities.append({value: count/n_samples for value, count in zip(values, counts)})
        return np.array(columns_probabilities)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.classes, classes_counts = np.unique(y, return_counts=True)
        self.classes_probabilities = classes_counts/len(y)

        for cls in self.classes:
            self.columns_probabilities.append(self.get_columns_probabilities(X[y == cls]))

    def single_predict(self, x: np.ndarray):
        probabilities = {}
        for class_indx, cls in enumerate(self.classes):
            class_probability = self.classes_probabilities[class_indx]
            log_probability = np.log(class_probability)
            for feature_indx, xi in enumerate(x):
                feature_probability = self.columns_probabilities[class_indx][feature_indx].get(xi, 0) + 1e-8
                log_probability += np.log(feature_probability)
            probabilities[cls] = log_probability
        return probabilities
