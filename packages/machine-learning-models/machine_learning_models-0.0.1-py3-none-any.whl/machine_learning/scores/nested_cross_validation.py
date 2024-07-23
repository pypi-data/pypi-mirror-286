import numpy as np
from abc import ABC, abstractmethod
from itertools import product
from random import sample

from machine_learning.scores.get_scores import get_classification_accurancy
from machine_learning.TitanicDatasetPreprocessing import get_data
from machine_learning.src.Adaboost.AdaboostModel import Adaboost
from machine_learning.src.ExtremeGradientBoost.XGBoostModel import XGboost
from machine_learning.src.GradientBoosting.GradientBoostingModel import GBoost
from machine_learning.src.KNearestNeighbours.KNearestNeighboursModel import KNearestNeighbours
from machine_learning.src.LogisticRegression.LogisticRegressionModel import LogisticRegression
from machine_learning.src.RandomForest.RandomForestModel import RandomForest
from machine_learning.src.SVM.SvmModel import SVM


# Test below class implementation
class NestedCrossValidation(ABC):
    def __init__(self, k=5, m=2, n_possible_hiperparams=None):
        self.k = k
        self.m = m
        self.n = n_possible_hiperparams

    def outer_loop(self, X: np.ndarray, y: np.ndarray):
        test_size = len(y)//self.k
        models_accurancies = {}
        for i in range(self.k):
            print(f"{i+1}/{self.k} outer cross validation iteration:")
            start = i * test_size
            end = start + test_size

            X_test = X[start:end]
            y_test = y[start:end]
            X_train = np.concatenate((X[:start], X[end:]), axis=0)
            y_train = np.concatenate((y[:start], y[end:]), axis=0)

            hiperparameters = self.inner_loop(X_train, y_train)
            preds = self.model.predict(X_test)
            accurancy = get_classification_accurancy(preds, y_test)
            if hiperparameters not in models_accurancies.keys():
                models_accurancies[hiperparameters] = []
            models_accurancies[hiperparameters].append(accurancy)

        return models_accurancies

    def inner_loop(self, X: np.ndarray, y: np.ndarray):
        test_size = len(y)//self.m
        results = {}

        for i in range(self.m):
            print(f"{i}/{self.m} inner cross validation iteration:")
            all_hiperparameters = self.get_hiperparameters()
            start = i * test_size
            end = start + test_size
            X_test = X[start:end]
            y_test = y[start:end]
            X_train = np.concatenate((X[:start], X[end:]), axis=0)
            y_train = np.concatenate((y[:start], y[end:]), axis=0)

            indx = 1
            for hiperparameters in all_hiperparameters:
                self.model.set_hiperaparameters(*hiperparameters)
                self.model.fit(X_train, y_train, print_progress=False)
                preds = self.model.predict(X_test)
                accurancy = get_classification_accurancy(preds, y_test)
                results[hiperparameters] = results.get(hiperparameters, 0) + accurancy
                print(f"{indx}/{len(all_hiperparameters)} hiperparameters checked")
                indx += 1

        results = {hip: acc/self.m for hip, acc in results.items()}
        the_best_hiperaparameters = max(results, key=results.get)
        return the_best_hiperaparameters

    def get_the_best_model(self, X: np.ndarray, y: np.ndarray):
        models_accurancies = self.outer_loop(X, y)
        the_best_acc = 0.0
        the_biggest_lenght = 0.0
        the_best_hip = None
        for hip, accs in models_accurancies.items():
            length = len(accs)
            average_acc = sum(accs)/len(accs)
            if length > the_biggest_lenght:
                the_best_acc = average_acc
                the_biggest_lenght = length
                the_best_hip = hip
            elif length == the_biggest_lenght:
                if average_acc > the_best_acc:
                    the_best_acc = average_acc
                    the_best_hip = hip
        self.model.set_hiperaparameters(*the_best_hip)
        self.model.fit(X, y)
        return self.model, the_best_acc

    @abstractmethod
    def get_hiperparameters(self):
        pass


class AdaboostCV(NestedCrossValidation):
    def __init__(self, k=5, m=2, n_possible_hiperparams=None):
        super().__init__(k, m, n_possible_hiperparams)
        self.model = Adaboost(0)

    def get_hiperparameters(self):
        hiperparameters = []
        for indx in range(2, 102, 4):
            hiperparameters.append((indx,))
        if not self.n or len(hiperparameters) <= self.n:
            return hiperparameters
        else:
            return sample(hiperparameters, self.n)


class XGBoostCV(NestedCrossValidation):
    def __init__(self, k=5, m=2, n_possible_hiperparams=None):
        super().__init__(k, m, n_possible_hiperparams)
        self.model = XGboost(0, 0, 0, 0, 0, 0)

    def get_hiperparameters(self):
        trees_numbers = np.arange(5, 35, 5)
        learning_rates = np.arange(0.1, 0.9, 0.2)
        lambdas = np.array([1, 2])
        gammas = np.array([1, 5, 10])
        max_depths = np.array([2, 3, 4, 5, 6, 7, 8])
        covers = np.array([0.0, 0.5, 1])
        hiperparameters = list(product(trees_numbers, learning_rates, lambdas, gammas, max_depths, covers))
        if not self.n or len(hiperparameters) <= self.n:
            return hiperparameters
        else:
            return sample(hiperparameters, self.n)


class GBoostCV(NestedCrossValidation):
    def __init__(self, k=5, m=2, n_possible_hiperparams=None):
        super().__init__(k, m, n_possible_hiperparams)
        self.model = GBoost(0, 0, 0, 0)

    def get_hiperparameters(self):
        models_number = np.array([5, 10, 15, 30, 45, 85, 100])
        max_samples = np.array([5, 10, 15, 20])
        learning_rates = np.arange(0.1, 0.9, 0.2)
        max_depths = np.array([3, 4, 5, 6, 7, 8])
        hiperparameters = list(product(models_number, learning_rates, max_samples, max_depths))
        if not self.n or len(hiperparameters) <= self.n:
            return hiperparameters
        else:
            return sample(hiperparameters, self.n)


class KNearestNeighboursCV(NestedCrossValidation):
    def __init__(self, k=5, m=2, n_possible_hiperparams=None):
        super().__init__(k, m, n_possible_hiperparams)
        self.model = KNearestNeighbours(3)

    def get_hiperparameters(self):
        hiperparameters = []
        for indx in range(1, 20):
            hiperparameters.append((indx,))
        if not self.n or len(hiperparameters) <= self.n:
            return hiperparameters
        else:
            return sample(hiperparameters, self.n)


class LogisticRegressionCV(NestedCrossValidation):
    def __init__(self, k=5, m=2, n_possible_hiperparams=None):
        super().__init__(k, m, n_possible_hiperparams)
        self.model = LogisticRegression(0, 0)

    def get_hiperparameters(self):
        learning_rates = np.array([0.01, 0.05, 0.1, 0.2, 0.3])
        iterations_numbers = np.arange(50, 1050, 100)
        hiperparameters = list(product(learning_rates, iterations_numbers))
        if not self.n or len(hiperparameters) <= self.n:
            return hiperparameters
        else:
            return sample(hiperparameters, self.n)


class RandomForestCV(NestedCrossValidation):
    def __init__(self, k=5, m=2, n_possible_hiperparams=None):
        super().__init__(k, m, n_possible_hiperparams)
        self.model = RandomForest(0, 0, 0, 0)

    def get_hiperparameters(self):
        n_trees = np.arange(5, 105, 5)
        n_features = np.array([2])  # always using sqrt(n_features)
        max_samples = np.array([5, 10, 15, 20])
        max_depths = np.array([2, 3, 4, 5, 6, 7, 8])
        hiperparameters = list(product(n_trees, n_features, max_samples, max_depths))
        if not self.n or len(hiperparameters) <= self.n:
            return hiperparameters
        else:
            return sample(hiperparameters, self.n)


class SVMCV(NestedCrossValidation):
    def __init__(self, k=5, m=2, n_possible_hiperparams=None):
        super().__init__(k, m, n_possible_hiperparams)
        self.model = SVM(0, 0, 0, 0, "linear")

    def get_hiperparameters(self):
        rs = np.arange(1, 10, 2)
        ds = np.arange(2, 8, 1)
        sigmas = np.arange(1, 10, 2)
        lambdas = np.array([1, 2, 3, 4])
        kernels = np.array(["linear", "polynomial", "gaussian"])
        hiperparameters = list(product(rs, ds, sigmas, lambdas, kernels))
        if not self.n or len(hiperparameters) <= self.n:
            return hiperparameters
        else:
            return sample(hiperparameters, self.n)


if __name__ == '__main__':
    ncv = SVMCV(k=5, m=2, n_possible_hiperparams=20)
    X_train, X_test, y_train, y_test = get_data()
    model, accurancy = ncv.get_the_best_model(X_train, y_train)
    preds = model.predict(X_test)
    acc = get_classification_accurancy(preds, y_test)
    print(acc)
