from dataclasses import dataclass
import numpy as np


@dataclass
class Node:
    value: int = None
    is_leaf: bool = False

    left_child: 'Node' = None
    right_child: 'Node' = None
    split_feature: int = None
    split_value: float = None

    x_data: np.ndarray = None
    y_data: np.ndarray = None


class Stump:
    def __init__(self):
        self.root = self.amount_of_say = None

    def calculate_gini(self, node: Node, treshold: float, feature_index: int):
        left_indexes = node.x_data[:, feature_index] <= treshold
        right_indexes = node.x_data[:, feature_index] > treshold
        y_left = node.y_data[left_indexes]
        y_right = node.y_data[right_indexes]
        if len(y_left) == 0 or len(y_right) == 0:
            return None

        left_y_values, left_y_counts = np.unique(y_left, return_counts=True)
        right_y_values, right_y_counts = np.unique(y_right, return_counts=True)

        left_gini = 1 - np.sum((left_y_counts/len(y_left))**2)
        left_weight = len(y_left)/len(node.y_data)
        right_gini = 1 - np.sum((right_y_counts/len(y_right))**2)
        right_weight = len(y_right)/len(node.y_data)

        return left_weight*left_gini + right_weight*right_gini

    def get_tresholds(self, node: Node, feature_index: int):
        X = node.x_data[:, feature_index]
        start = np.min(X)
        stop = np.max(X)
        n = (len(np.unique(X)) // 100) + 1
        return np.linspace(start, stop, int(len(np.unique(X))/n))

    def get_split_feature(self, node: Node):
        n_samples, n_features = node.x_data.shape
        the_best_value = the_best_feature = None
        the_best_gini = float("inf")
        for feature_index in range(n_features):
            tresholds = self.get_tresholds(node, feature_index)
            for treshold in tresholds:
                gini_impurity = self.calculate_gini(node, treshold, feature_index)
                if not gini_impurity:
                    continue
                elif gini_impurity < the_best_gini:
                    the_best_gini = gini_impurity
                    the_best_feature = feature_index
                    the_best_value = treshold
        return the_best_value, the_best_feature

    def get_node_value(self, node_y: np.ndarray):
        counts = np.bincount(node_y, minlength=2)
        return counts[1] / len(node_y)

    def split_node(self, node: Node):
        split_value, split_feature_index = self.get_split_feature(node)
        left_indexes = node.x_data[:, split_feature_index] <= split_value
        right_indexes = node.x_data[:, split_feature_index] > split_value

        left_y = node.y_data[left_indexes]
        left_y_prediction = self.get_node_value(left_y)

        right_y = node.y_data[right_indexes]
        right_y_prediction = self.get_node_value(right_y)

        node.left_child = Node(value=left_y_prediction, is_leaf=True)
        node.right_child = Node(value=right_y_prediction, is_leaf=True)
        node.split_feature = split_feature_index
        node.split_value = split_value

    def train(self, X: np.ndarray, y: np.ndarray):
        self.root = Node(x_data=X, y_data=y)
        self.split_node(self.root)

    def predict(self, x: np.ndarray, decision_treshold):
        if x[self.root.split_feature] <= self.root.split_value:
            return self.root.left_child.value > decision_treshold
        else:
            return self.root.right_child.value > decision_treshold
