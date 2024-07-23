from .GaussianNaiveBayes import GaussionNaiveBayes
from .MultinomialNaiveBayes import MultinomialNaiveBayes
import numpy as np


class NaiveBayes:
    def __init__(self):
        self.gausian = GaussionNaiveBayes()
        self.multinomial = MultinomialNaiveBayes()
        self.classes = None
        self.discreet_indices = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.classes = np.unique(y)
        self.discreet_indices = np.apply_along_axis(lambda feature: len(np.unique(feature)), 0, X) < 10
        self.multinomial.fit(X[:, self.discreet_indices], y)
        self.gausian.fit(X[:, ~self.discreet_indices], y)

    def predict(self, X: np.ndarray, decision_treshold=0.5):
        probabilities = []
        for x in X:
            prediction_discreet = self.multinomial.single_predict(x[self.discreet_indices])
            prediction_continous = self.gausian.single_predict(x[~self.discreet_indices])
            total_prediction = {cls: prediction_discreet[cls] + prediction_continous[cls] for cls in self.classes}
            exp_total_prediction = {cls: np.exp(total_prediction[cls]) for cls in self.classes}

            probability = exp_total_prediction[1] / sum(exp_total_prediction.values())
            probabilities.append(probability)

        return np.array(probabilities) > decision_treshold
