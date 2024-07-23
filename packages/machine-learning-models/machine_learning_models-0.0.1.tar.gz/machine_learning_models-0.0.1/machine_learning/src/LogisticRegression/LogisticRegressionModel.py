import numpy as np


class LogisticRegression:
    def __init__(self, learning_rate: float, training_iterations: int):
        self.lr = learning_rate
        self.iters = training_iterations
        self.coeffs = None

        self.means = None
        self.stds = None

    def set_hiperaparameters(self, learning_rate=None, training_iterations=None):
        if learning_rate is not None:
            self.lr = learning_rate
        if training_iterations is not None:
            self.iters = training_iterations

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))

    def one_samples_gradient(self, x: np.ndarray, y: float):
        x = np.append(x, 1)
        p = self.sigmoid(np.dot(self.coeffs, x))
        return (p - y) * x

    def fit(self, X: np.ndarray, Y: np.ndarray, print_progress=True):
        n_samples, n_features = X.shape
        self.coeffs = np.zeros(n_features+1)
        X = self.scale_data(X)
        for t in range(self.iters):
            gradient = np.sum([self.one_samples_gradient(x, y) for x, y in zip(X, Y)], axis=0)
            self.coeffs -= self.lr * gradient/len(Y)
            if print_progress:
                print(f"{t+1}/{self.iters} training iteration ended")

    def predict(self, X: np.ndarray, decision_treshold=0.5):
        predictions = []
        for x in X:
            x = np.append((x-self.means)/self.stds, 1)
            predictions.append(self.sigmoid(np.dot(self.coeffs, x)))
        return np.array(predictions) > decision_treshold

    def scale_data(self, X: np.ndarray):
        self.means = np.mean(X, axis=0)
        self.stds = np.std(X, axis=0)
        self.stds[self.stds == 0] = 1
        return (X-self.means)/self.stds
