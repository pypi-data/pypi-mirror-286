import numpy as np
from cvxopt import matrix, solvers


class PrimalSVM:
    def __init__(self, regularization_param: float, iterations: int, learning_rate: float):
        self.C = regularization_param
        self.iters = iterations
        self.lr = learning_rate
        self.weights = None
        self.bias = None
        self.mean_X = self.std_X = None

    def prepare_data(self, X: np.ndarray, y: np.ndarray):
        y_values = np.unique(y)
        if len(y_values) != 2:
            raise ValueError("Number of unique values in y should be equal to 2")
        y_mapping = {y_values[0]: -1, y_values[1]: 1}
        new_y = np.array([y_mapping[y_value] for y_value in y])

        self.mean_X = np.mean(X, axis=0)
        self.std_X = np.std(X, axis=0)
        new_X = (X - self.mean_X) / self.std_X

        return new_X, new_y

    def get_dw(self, x: np.ndarray, y: int):
        condition = 1 - y * (np.dot(self.weights, x) + self.bias) > 0
        if condition:
            return self.weights - self.C * y * x
        else:
            return self.weights

    def get_db(self, x: np.ndarray, y: int):
        condition = 1 - y * (np.dot(self.weights, x) + self.bias) > 0
        if condition:
            return -self.C * y
        else:
            return 0

    def fit(self, X: np.ndarray, y: np.ndarray):
        X, y = self.prepare_data(X, y)
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        for t in range(self.iters):
            grad_w = np.sum([self.get_dw(x, target) for x, target in zip(X, y)], axis=0)
            grad_b = np.sum([self.get_db(x, target) for x, target in zip(X, y)])
            self.weights -= self.lr * grad_w / n_samples
            self.bias -= self.lr * grad_b / n_samples

    def predict(self, X: np.ndarray):
        X = (X - self.mean_X) / self.std_X
        predictions = []
        for x in X:
            prediction = np.sign(np.dot(self.weights, x) + self.bias)
            predictions.append(prediction)
        return np.array(predictions)


class SVM:
    def __init__(self, r=1, d=2, sigma=1, regularization_param=1, kernel="linear"):
        self.support_vectors_alpha = self.bias = None
        self.support_vectors_x = self.support_vectors_y = None
        self.min_X = self.max_X = None
        if kernel not in ["linear", "polynomial", "gaussian"]:
            raise ValueError("Wrong kernel name!")
        self.kernel = kernel
        self.C = regularization_param
        self.r = r
        self.d = d
        self.sigma = sigma

    def set_hiperaparameters(self, r=None, d=None, sigma=None, regularization_param=None, kernel=""):
        if r is not None:
            self.r = r
        if d is not None:
            self.d = d
        if sigma is not None:
            self.sigma = sigma
        if regularization_param is not None:
            self.C = regularization_param
        if kernel:
            self.kernel = kernel

    def lineal_kernel(self, X1: np.ndarray, X2: np.ndarray):
        return np.dot(X1, X2.T)

    def polynomial_kernel(self, X1: np.ndarray, X2: np.ndarray):
        return np.power(np.dot(X1, X2.T)+self.r, self.d)

    def gauss_kernel(self, X1, X2):
        X1 = np.atleast_2d(X1)
        X2 = np.atleast_2d(X2)
        distances = np.sum((X1[:, np.newaxis, :] - X2[np.newaxis, :, :])**2, axis=2)
        kernel_values = np.exp(-distances / (2 * self.sigma**2))
        return kernel_values

    def kernel_function(self, X1: np.ndarray, X2: np.ndarray):
        if self.kernel == "linear":
            return self.lineal_kernel(X1, X2)
        elif self.kernel == "polynomial":
            return self.polynomial_kernel(X1, X2)
        else:
            return self.gauss_kernel(X1, X2)

    def QP_optimization(self, X: np.ndarray, Y: np.ndarray):
        n_samples, n_features = X.shape

        K = self.kernel_function(X, X)
        P = matrix(np.outer(Y, Y) * K)
        q = matrix(np.ones(shape=(n_samples, 1)) * -1.0)

        G_std = np.eye(n_samples) * -1.0
        h_std = np.zeros(shape=(n_samples, 1))
        G_slack = np.eye(n_samples)
        h_slack = np.full(shape=(n_samples, 1), fill_value=self.C)
        G = matrix(np.vstack((G_std, G_slack)))
        h = matrix(np.vstack((h_std, h_slack)))

        A = matrix(Y.astype(np.float64), (1, n_samples))
        b = matrix(0.0)

        solvers.options["show_progress"] = False
        solution = solvers.qp(P, q, G, h, A, b)
        best_alpha = np.array(solution['x']).flatten()
        return best_alpha

    def get_support_vectors(self, X: np.ndarray, Y: np.ndarray, alpha: np.ndarray):
        support_vectors = (alpha > 1e-5) & (alpha < self.C)
        return X[support_vectors], Y[support_vectors], alpha[support_vectors]

    def get_bias(self, X: np.ndarray, Y: np.ndarray, alpha: np.ndarray):
        sum_b = 0
        for x, y in zip(self.support_vectors_x, self.support_vectors_y):
            sum_b += y - np.sum(alpha * Y * self.kernel_function(x, X))
        return sum_b/len(self.support_vectors_y)

    def fit(self, X: np.ndarray, y: np.ndarray, print_progress=False):
        Y = np.where(y <= 0, -1, 1)
        X = self.scale_data(X)

        alpha = self.QP_optimization(X, Y)
        self.support_vectors_x, self.support_vectors_y, self.support_vectors_alpha = self.get_support_vectors(X, Y, alpha)
        self.bias = self.get_bias(X, Y, alpha)

    def predict(self, X: np.ndarray):
        predictions = []
        for x in X:
            x = (x-self.min_X)/(self.max_X-self.min_X+1e-8)
            prediction_value = np.sum(self.support_vectors_alpha*self.support_vectors_y*self.kernel_function(x, self.support_vectors_x)) + self.bias
            predictions.append(np.sign(prediction_value))
        return np.array(predictions)

    def scale_data(self, X: np.ndarray):
        self.min_X = np.min(X, axis=0)
        self.max_X = np.max(X, axis=0)
        return (X-self.min_X)/(self.max_X-self.min_X+1e-8)
