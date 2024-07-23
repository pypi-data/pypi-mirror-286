import numpy as np
from .Tree import Tree, Node


class GBoost:
    def __init__(self, models_number: int, learning_rate: float, max_depth: int, max_samples: int):
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.max_samples = max_samples
        self.models_number = models_number
        self.classification = False
        self.models = list()

    def set_hiperaparameters(self, models_number=None, learning_rate=None, max_depth=None, max_samples=None):
        if models_number is not None:
            self.models_number = models_number
        if learning_rate is not None:
            self.learning_rate = learning_rate
        if max_depth is not None:
            self.max_depth = max_depth
        if max_samples is not None:
            self.max_samples = max_samples
        self.models = list()

    def calculate_pseudo_residuals(self, X: np.ndarray, y: np.ndarray):
        prediction = self.predict(X, final_prediction=False)
        return y - prediction, prediction

    def create_new_model(self, X: np.ndarray, target: np.ndarray, previous_prediction: np.ndarray, first=False):
        model = Tree(self.max_depth, self.max_samples, self.classification)
        if not first:
            model.fit(X, target, previous_prediction)
        else:
            if not self.classification:
                value = np.mean(target)
            else:
                y_values, y_counts = np.unique(target, return_counts=True)
                value = np.log(y_counts[1]/y_counts[0])
            model.root = Node(value=value, is_leaf=True)

        self.models.append(model)

    def fit(self, X: np.ndarray, y: np.ndarray, print_progress=True):
        if len(np.unique(y)) <= 5:
            self.classification = True

        self.create_new_model(X, y, None, first=True)
        if print_progress:
            print(f"1/{self.models_number} model trained")

        for iter in range(int(self.models_number)-1):
            residuals, prediction = self.calculate_pseudo_residuals(X, y)
            self.create_new_model(X, residuals, prediction)
            if print_progress:
                print(f"{iter+2}/{self.models_number} model trained")

        self.models = np.array(self.models)

    def predict(self, X: np.ndarray, decision_treshold=0.5, final_prediction=True):
        first_model = self.models[0]
        total_prediction = first_model.predict(X)
        for model in self.models[1:]:
            total_prediction += self.learning_rate * model.predict(X)

        if self.classification:
            percentage = np.exp(total_prediction)/(1+np.exp(total_prediction))  # change log(odds) to probability
            return percentage if not final_prediction else percentage > decision_treshold
        else:
            return total_prediction
