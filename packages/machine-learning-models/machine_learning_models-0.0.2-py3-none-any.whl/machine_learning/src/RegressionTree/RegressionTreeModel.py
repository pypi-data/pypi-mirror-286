from .Node import Node
import numpy as np


class RegressionTree:
    def __init__(self, max_depth, max_samples):
        self.max_depth = max_depth
        self.max_samples = max_samples
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
            right_x_data = node.x_data[right_child_indices]
            right_y_data = node.y_data[right_child_indices]

            node.left_child = Node(x_data=left_x_data, y_data=left_y_data, depth=node.depth+1)
            node.right_child = Node(x_data=right_x_data, y_data=right_y_data, depth=node.depth+1)
            node.split_feature = split_feature_index
            node.split_value = split_value

    def create_leaf(self, node: Node):
        node.value = np.mean(node.y_data)
        node.is_leaf = True

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

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.root = Node(x_data=X, y_data=y, depth=1)
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

    def prune(self, X: np.ndarray, y: np.ndarray):
        self._prune(self.root, X, y)

    def _prune(self, node: Node, X: np.ndarray, y: np.ndarray):
        if node.is_leaf or y.size == 0 or X.size == 0:
            return node
        else:
            mask_left = X[:, node.split_feature] <= node.split_value
            mask_right = X[:, node.split_feature] > node.split_value
            if node.left_child:
                node.left_child = self._prune(node.left_child, X[mask_left], y[mask_left])
            if node.right_child:
                node.right_child = self._prune(node.right_child, X[mask_right], y[mask_right])

            if node.left_child.is_leaf and node.right_child.is_leaf:
                prediction_without_split = np.mean(y)
                error_without_split = np.mean((y - prediction_without_split) ** 2)

                y_left = y[mask_left] if len(y[mask_left]) > 0 else np.zeros(1)
                y_right = y[mask_right] if len(y[mask_right]) > 0 else np.zeros(1)

                prediction_with_split = len(y_left)/len(y) * np.mean((y_left-node.left_child.value)**2) +\
                    len(y_right)/len(y) * np.mean((y_right-node.right_child.value)**2)
                error_with_split = np.mean((y - prediction_with_split) ** 2)

                if error_without_split < error_with_split:
                    node.is_leaf = True
                    node.value = prediction_without_split
                    node.left_child = None
                    node.right_child = None

        return node
