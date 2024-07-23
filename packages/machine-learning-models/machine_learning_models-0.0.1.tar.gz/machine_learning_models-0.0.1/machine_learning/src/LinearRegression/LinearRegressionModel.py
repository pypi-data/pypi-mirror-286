import numpy as np


class LinearRegressionModel:
    """
    Code for linear regression model

    :param learning_rate: coefficient for gradient descend algorithm
    :param iterations: how many iterations should model be trained

    Run fit to train the model. Then, use predict to make a prediction for given sample
    """
    def __init__(self, learning_rate, iterations) -> None:
        self.min_X = self.max_X = None
        self.learning_rate = learning_rate
        self.t_max = iterations
        self.coefficients = None

    def set_hiperaparameters(self, learning_rate=None, iterations=None):
        if learning_rate is not None:
            self.learning_rate = learning_rate
        if iterations is not None:
            self.t_max = iterations

    def one_sample_loss_gradient(self, x: np.ndarray, y: float) -> np.ndarray:
        x = np.append(x, 1)
        y_pred = np.dot(self.coefficients, x)
        return (y_pred - y) * x

    def fit(self, X: np.ndarray, y: np.ndarray, print_progress=True):
        n = len(X[0]) + 1
        self.coefficients = np.zeros(shape=(n,))
        X = self._scale_data(X)

        for t in range(self.t_max):
            gradient = np.zeros(shape=(n,))
            for sample, target in zip(X, y):
                gradient += self.one_sample_loss_gradient(sample, target)/len(X)
            self.coefficients -= self.learning_rate * gradient
            if any(abs(self.learning_rate * gradient) > 100):
                raise ValueError("Learning rate is too high for LR to work")

            if print_progress:
                print(f"{t+1}/{self.t_max} learning iteration ended")

    def predict(self, X: np.ndarray):
        X = (X-self.min_X)/(self.max_X-self.min_X)
        predictions = []
        for x in X:
            x = np.append(x, 1)
            predictions.append(np.dot(self.coefficients, x))
        return predictions

    def _scale_data(self, X: np.ndarray):
        new_X = np.zeros(shape=X.shape)
        index = 0
        self.min_X = X.min(axis=0)
        self.max_X = X.max(axis=0)
        for x in X:
            new_X[index] = (x-self.min_X)/(self.max_X-self.min_X+0.01)
            index += 1
        return new_X
