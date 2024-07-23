import numpy as np
from dataclasses import dataclass


@dataclass
class Node:
    value: int = None
    is_leaf: bool = False
    depth: int = None

    left_child: 'Node' = None
    right_child: 'Node' = None
    split_feature: int = None
    split_value: float = None

    x_data: np.ndarray = None
    y_data: np.ndarray = None


class DecisionTree:
    def __init__(self, n_split_features, max_samples, max_depth, single=False):
        self.n_split_features = n_split_features
        self.max_samples = max_samples
        self.max_depth = max_depth
        self.single = single
        self.root = None

    def stop_conditions(self, node: Node):
        return len(np.unique(node.y_data)) == 1 or \
            len(node.y_data) < self.max_samples or \
            node.depth > self.max_depth

    def get_tresholds(self, X: np.ndarray, feature_index: int):
        feature_values = X[:, feature_index]
        start = np.min(feature_values)
        stop = np.max(feature_values)
        n = (len(np.unique(feature_values)) // 100) + 1
        return np.linspace(start, stop, int(len(X)/n))

    def get_gini_impurity(self, treshold: np.ndarray, feature_index: int, node: Node):
        left_indexes = node.x_data[:, feature_index] <= treshold
        right_indexes = node.x_data[:, feature_index] > treshold
        y_left = node.y_data[left_indexes]
        y_right = node.y_data[right_indexes]

        if len(y_left) == 0 or len(y_right) == 0:
            return None

        y_left_counts = np.unique(y_left, return_counts=True)[1]
        y_right_counts = np.unique(y_right, return_counts=True)[1]

        left_component = 1 - np.sum((y_left_counts/len(y_left))**2)
        left_weight = len(y_left) / len(node.y_data)
        right_component = 1 - np.sum((y_right_counts/len(y_right))**2)
        right_weight = len(y_right) / len(node.y_data)
        return left_weight * left_component + right_weight * right_component

    def get_split(self, node: Node):
        X = node.x_data
        best_split_value = best_split_feature = None
        best_gini_impurity = float("inf")
        n_samples, n_features = X.shape

        if not self.single:
            possible_indexes = np.random.choice(np.arange(stop=n_features, step=1), size=(self.n_split_features,))
        else:
            possible_indexes = np.arange(stop=n_features, step=1)
        for feature_index in possible_indexes:
            tresholds = self.get_tresholds(X, feature_index)
            for treshhold in tresholds:
                gini_impurity = self.get_gini_impurity(treshhold, feature_index, node)
                if not gini_impurity:
                    continue
                elif gini_impurity < best_gini_impurity:
                    best_gini_impurity = gini_impurity
                    best_split_value = treshhold
                    best_split_feature = feature_index

        return best_split_feature, best_split_value

    def create_children(self, node: Node):
        best_split_feature, best_split_value = self.get_split(node)
        if not best_split_feature and not best_split_value:
            self.create_leaf(node)
        else:
            indexes_left = node.x_data[:, best_split_feature] <= best_split_value
            indexes_right = node.x_data[:, best_split_feature] > best_split_value

            X_left = node.x_data[indexes_left]
            y_left = node.y_data[indexes_left]
            X_right = node.x_data[indexes_right]
            y_right = node.y_data[indexes_right]

            node.split_feature = best_split_feature
            node.split_value = best_split_value
            node.left_child = Node(x_data=X_left, y_data=y_left, depth=node.depth+1)
            node.right_child = Node(x_data=X_right, y_data=y_right, depth=node.depth+1)

    def create_leaf(self, node: Node):
        node.is_leaf = True
        y_counts = np.bincount(node.y_data, minlength=2)
        node.value = y_counts[1]/np.sum(y_counts)

    def train(self, node: Node):
        if not self.stop_conditions(node):
            self.create_children(node)
            if node.is_leaf:
                return
            self.train(node.left_child)
            self.train(node.right_child)
        else:
            self.create_leaf(node)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.root = Node(x_data=X, y_data=y, depth=1)
        self.train(self.root)

    def single_predict(self, x: np.ndarray, decision_treshold: float):
        node = self.root
        while not node.is_leaf:
            if x[node.split_feature] <= node.split_value:
                node = node.left_child
            else:
                node = node.right_child
        return node.value > decision_treshold

    def predict(self, X: np.ndarray, decision_treshold=0.5):
        predictions = []
        for x in X:
            predictions.append(self.single_predict(x, decision_treshold))
        return predictions
