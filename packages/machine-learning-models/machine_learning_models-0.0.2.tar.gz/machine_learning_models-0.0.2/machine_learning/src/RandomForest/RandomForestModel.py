from .Tree import DecisionTree
import numpy as np


class RandomForest:
    def __init__(self, number_of_trees, number_of_features, max_samples, max_depth):
        self.number_of_trees = number_of_trees
        self.trees = np.array([DecisionTree(number_of_features, max_samples, max_depth) for _ in range(number_of_trees)])

    def set_hiperaparameters(self, number_of_trees=None, number_of_features=None, max_samples=None, max_depth=None):
        if number_of_features is not None and number_of_features is not None and max_samples is not None and max_depth is not None:
            self.trees = np.array([DecisionTree(number_of_features, max_samples, max_depth) for _ in range(number_of_trees)])

    def bootstrap(self, X: np.ndarray, y: np.ndarray):
        n_samples = X.shape[0]
        indexes = np.random.choice(n_samples, size=(n_samples,), replace=True)
        return X[indexes], y[indexes]

    def fit(self, X: np.ndarray, y: np.ndarray, print_progress=True):
        self.trees[0].fit(X, y)
        if print_progress:
            print(f"1/{self.number_of_trees} tree created")
        for indx, tree in enumerate(self.trees[1:]):
            data_x, data_y = self.bootstrap(X, y)
            tree.fit(data_x, data_y)
            if print_progress:
                print(f"{indx+2}/{self.number_of_trees} tree created")

    def predict(self, X: np.ndarray, decision_treshold=0.5):
        predictions = []
        for x in X:
            x_preds = [model.single_predict(x, decision_treshold) for model in self.trees]
            predictions.append(np.mean(x_preds) > decision_treshold)
            # y_counts = np.bincount(x_preds, minlength=2)
            # predictions.append(y_counts[1]/np.sum(y_counts))
        return np.array(predictions) > decision_treshold
