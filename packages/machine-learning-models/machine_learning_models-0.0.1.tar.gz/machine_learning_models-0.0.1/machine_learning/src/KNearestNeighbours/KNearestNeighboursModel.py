import numpy as np


class KNearestNeighbours:
    def __init__(self, k):
        self.k = k
        self.data = None
        self.mean_X = self.std_X = None

    def set_hiperaparameters(self, k=None):
        if k is not None:
            self.k = k

    def calculate_distance(self, training_sample: np.ndarray, to_predict: np.ndarray):
        return (np.sum((training_sample-to_predict)**2))**0.5

    def fit(self, X: np.ndarray, y: np.ndarray, print_progress=False):
        self.data = list(zip(self.scale_data(X), y))

    def predict(self, X: np.ndarray, decision_treshold=0.5):
        X = (X-self.mean_X)/self.std_X
        predictions = []
        for x in X:
            sorted_data = sorted(self.data, key=lambda data: self.calculate_distance(data[0], x))
            y_counts = np.bincount(list(map(lambda row: row[1], sorted_data))[:self.k], minlength=2)
            predictions.append(y_counts[1]/np.sum(y_counts))
        return np.array(predictions) > decision_treshold

    def scale_data(self, X: np.ndarray):
        self.mean_X = np.mean(X, axis=0)
        self.std_X = np.std(X, axis=0)
        return (X-self.mean_X)/self.std_X
