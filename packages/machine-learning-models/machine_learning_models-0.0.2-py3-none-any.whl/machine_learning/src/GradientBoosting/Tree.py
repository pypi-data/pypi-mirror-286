from dataclasses import dataclass
import numpy as np


@dataclass
class Node:
    value: float = None
    is_leaf: bool = False
    depth: int = None

    left_child: 'Node' = None
    right_child: 'Node' = None

    split_feature: str = None
    split_value: float = None
    x_data: np.ndarray = None
    y_data: np.ndarray = None
    predictions: np.ndarray = None


class Tree:
    def __init__(self, max_depth, max_samples, classification: bool):
        self.max_depth = max_depth
        self.max_samples = max_samples
        self.classification = classification
        self.root = None

    def get_tresholds(self, x: np.ndarray):
        number_of_tresholds = min(len(np.unique(x)), 50)
        return np.linspace(np.min(x), np.max(x), number_of_tresholds)

    def get_error(self, node: Node, feature_index: int, treshold: float):
        left_child_indices = node.x_data[:, feature_index] <= treshold
        right_child_indices = node.x_data[:, feature_index] > treshold
        y_left = node.y_data[left_child_indices]
        y_right = node.y_data[right_child_indices]

        if len(y_left) == 0 or len(y_right) == 0:
            return None
        else:
            if self.classification:
                left_predictions = node.predictions[left_child_indices]
                right_predictions = node.predictions[right_child_indices]
                epsilon = 1e-8
                error_left = -np.mean(y_left * np.log(left_predictions + epsilon) + (1 - y_left) * np.log(1 - left_predictions + epsilon))
                error_right = -np.mean(y_right * np.log(right_predictions + epsilon) + (1 - y_right) * np.log(1 - right_predictions + epsilon))
            else:
                error_left = np.mean((y_left - np.mean(y_left))**2)
                error_right = np.mean((y_right - np.mean(y_right))**2)
            return len(y_left)/len(node.y_data) * error_left + len(y_right)/len(node.y_data) * error_right

    def get_split_features(self, node: Node):
        n_samples, n_features = node.x_data.shape
        the_smallest_error = float("inf")
        the_best_feature = the_best_value = None
        for feature_index in range(n_features):
            tresholds = self.get_tresholds(node.x_data[:, feature_index])
            for treshold in tresholds:
                error = self.get_error(node, feature_index, treshold)
                if not error:
                    continue
                elif error < the_smallest_error:
                    the_smallest_error = error
                    the_best_feature = feature_index
                    the_best_value = treshold
        return the_best_feature, the_best_value

    def split_node(self, node: Node):
        split_feature_index, split_value = self.get_split_features(node)
        if split_feature_index is None or split_value is None:
            self.create_leaf(node)
        else:
            left_child_indices = node.x_data[:, split_feature_index] <= split_value
            right_child_indices = node.x_data[:, split_feature_index] > split_value

            left_x_data = node.x_data[left_child_indices]
            left_y_data = node.y_data[left_child_indices]
            left_predictions = node.predictions[left_child_indices]
            right_x_data = node.x_data[right_child_indices]
            right_y_data = node.y_data[right_child_indices]
            right_predictions = node.predictions[right_child_indices]

            node.left_child = Node(x_data=left_x_data, y_data=left_y_data, depth=node.depth+1, predictions=left_predictions)
            node.right_child = Node(x_data=right_x_data, y_data=right_y_data, depth=node.depth+1, predictions=right_predictions)
            node.split_feature = split_feature_index
            node.split_value = split_value

    def create_leaf(self, node: Node):
        node.is_leaf = True
        if not self.classification:
            node.value = np.mean(node.y_data)
        else:
            numerator = np.sum(node.y_data)
            denumerator = np.sum(node.predictions * (1-node.predictions))
            if denumerator == 0:
                node.value = 0.0
            else:
                node.value = numerator/denumerator

    def stop_coditions(self, node: Node):
        return np.unique(node.y_data).size == 1 or node.depth > self.max_depth or len(node.y_data) < self.max_samples

    def train(self, node: Node):
        if not self.stop_coditions(node):
            self.split_node(node)
            if node.is_leaf:
                return
            self.train(node.left_child)
            self.train(node.right_child)
        else:
            self.create_leaf(node)

    def fit(self, X: np.ndarray, y: np.ndarray, previous_predictions: np.ndarray):
        self.root = Node(x_data=X, y_data=y, depth=1, predictions=previous_predictions)
        self.train(self.root)

    def predict(self, X: np.ndarray):
        predictions = []
        for x in X:
            node = self.root
            while not node.is_leaf:
                if x[node.split_feature] <= node.split_value:
                    node = node.left_child
                else:
                    node = node.right_child
            predictions.append(node.value)
        return np.array(predictions)
