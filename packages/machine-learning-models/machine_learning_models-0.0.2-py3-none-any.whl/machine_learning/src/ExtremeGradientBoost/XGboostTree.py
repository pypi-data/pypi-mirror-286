from dataclasses import dataclass
from abc import ABC, abstractmethod
import numpy as np


@dataclass
class Node:
    value: float = None
    is_leaf: bool = False

    left_child: 'Node' = None
    right_child: 'Node' = None
    split_feature_index: int = None
    split_value: float = None
    split_gain: float = None

    x_data: np.ndarray = None
    y_data: np.ndarray = None
    previous_prediction: np.ndarray = None
    similarity_score: float = None
    depth: int = None


class XGboostTree(ABC):
    def __init__(self, regularization_param: int, prune_constant: int, max_depth: int):
        self.lambd = regularization_param
        self.gamma = prune_constant
        self.max_depth = max_depth
        self.root = None

    @abstractmethod
    def get_similarity_score(self, y: np.ndarray, previous_predictions):
        pass

    @abstractmethod
    def get_leaf_value(self, node: Node):
        pass

    @abstractmethod
    def get_gain(self, root_node: Node, split_feature_index: int, split_value: float):
        pass

    def get_tresholds(self, X: np.ndarray):
        tresholds = []
        previous_x = X[0]
        for x in X[1:]:
            tresholds.append(np.mean([previous_x, x]))
            previous_x = x
        return sorted(tresholds)

    def get_best_feature(self, node: Node):
        n_samples, n_features = node.x_data.shape
        the_biggest_gain = float("-inf")
        the_best_feature = the_best_value = None
        for feature_index in range(n_features):
            tresholds = self.get_tresholds(node.x_data[:, feature_index])
            for treshold in tresholds:
                gain = self.get_gain(node, feature_index, treshold)
                if not gain:
                    continue
                elif gain > the_biggest_gain:
                    the_biggest_gain = gain
                    the_best_feature = feature_index
                    the_best_value = treshold
        return the_best_feature, the_best_value, the_biggest_gain

    def split_node(self, node: Node):
        the_best_feature, the_best_value, the_biggest_gain = self.get_best_feature(node)
        if the_best_feature is None or the_best_value is None:
            self.create_leaf(node)
        else:
            left_indices = node.x_data[:, the_best_feature] <= the_best_value
            right_indices = node.x_data[:, the_best_feature] > the_best_value

            left_y = node.y_data[left_indices]
            left_X = node.x_data[left_indices]
            left_predictions = node.previous_prediction[left_indices]
            right_y = node.y_data[right_indices]
            right_X = node.x_data[right_indices]
            right_predictions = node.previous_prediction[right_indices]
            node.left_child = Node(x_data=left_X, y_data=left_y, previous_prediction=left_predictions,
                                   similarity_score=self.get_similarity_score(left_y, node.previous_prediction), depth=node.depth+1)
            node.right_child = Node(x_data=right_X, y_data=right_y, previous_prediction=right_predictions,
                                    similarity_score=self.get_similarity_score(right_y, node.previous_prediction), depth=node.depth+1)

            node.split_feature_index = the_best_feature
            node.split_value = the_best_value
            node.split_gain = the_biggest_gain

    def create_leaf(self, node: Node):
        node.is_leaf = True
        node.value = self.get_leaf_value(node)

    def stop_conditions(self, node: Node):
        return len(np.unique(node.y_data)) == 0 or node.depth > self.max_depth

    def train(self, node: Node):
        if not self.stop_conditions(node):
            self.split_node(node)
            if node.is_leaf:
                return
            self.train(node.left_child)
            self.train(node.right_child)
        else:
            self.create_leaf(node)

    def fit(self, X: np.ndarray, y: np.ndarray, previous_prediction: np.ndarray):
        self.root = Node(x_data=X, y_data=y, similarity_score=self.get_similarity_score(y, previous_prediction),
                         depth=1, previous_prediction=previous_prediction)
        self.train(self.root)

    def predict(self, X: np.ndarray):
        preds = []
        for x in X:
            node = self.root
            while not node.is_leaf:
                if x[node.split_feature_index] <= node.split_value:
                    node = node.left_child
                else:
                    node = node.right_child
            preds.append(node.value)
        return np.array(preds)

    def prune(self):
        node = self.root
        self.root = self.prune_nodes(node)

    def prune_nodes(self, node: Node):
        if node.is_leaf:
            return node

        if node.left_child:
            node.left_child = self.prune_nodes(node.left_child)
        if node.right_child:
            node.right_child = self.prune_nodes(node.right_child)

        if node.left_child.is_leaf and node.right_child.is_leaf:
            pruning_subtraction = node.split_gain - self.gamma
            if pruning_subtraction < 0:
                node.is_leaf=True
                node.value = self.get_leaf_value(node)
                node.left_child = None
                node.right_child = None

        return node


class XGboostTreeRegression(XGboostTree):
    def get_similarity_score(self, y: np.ndarray, previous_predictions):
        return (np.sum(y)**2)/(len(y)+self.lambd)

    def get_leaf_value(self, node: Node):
        return np.sum(node.y_data)/(len(node.y_data)+self.lambd)

    def get_gain(self, root_node: Node, split_feature_index: int, split_value: float):
        less_indices = root_node.x_data[:, split_feature_index] <= split_value
        more_indices = root_node.x_data[:, split_feature_index] > split_value
        if len(root_node.y_data[less_indices]) == 0 or len(root_node.y_data[more_indices]) == 0:
            return None
        else:
            similarity_left = self.get_similarity_score(root_node.y_data[less_indices], root_node.previous_prediction)
            similarity_right = self.get_similarity_score(root_node.y_data[more_indices], root_node.previous_prediction)
            return similarity_left + similarity_right - root_node.similarity_score


class XGboostTreeClassification(XGboostTree):
    def __init__(self, regularization_param: int, prune_constant: int, max_depth: int, min_cover: float):
        super().__init__(regularization_param, prune_constant, max_depth)
        self.min_cover = min_cover

    def get_similarity_score(self, y: np.ndarray, previous_predictions: np.ndarray):
        return (np.sum(y)**2)/(np.sum(previous_predictions*(1-previous_predictions))+self.lambd)

    def get_leaf_value(self, node: Node):
        return np.sum(node.y_data)/(np.sum(node.previous_prediction*(1-node.previous_prediction))+self.lambd)

    def get_gain(self, root_node: Node, split_feature_index: int, split_value: float):
        less_indices = root_node.x_data[:, split_feature_index] <= split_value
        more_indices = root_node.x_data[:, split_feature_index] > split_value
        cover = np.sum(root_node.previous_prediction * (1-root_node.previous_prediction))
        if len(root_node.y_data[less_indices]) == 0 or len(root_node.y_data[more_indices]) == 0 or cover < self.min_cover:
            return None
        else:
            similarity_left = self.get_similarity_score(root_node.y_data[less_indices], root_node.previous_prediction)
            similarity_right = self.get_similarity_score(root_node.y_data[more_indices], root_node.previous_prediction)
            return similarity_left + similarity_right - root_node.similarity_score
