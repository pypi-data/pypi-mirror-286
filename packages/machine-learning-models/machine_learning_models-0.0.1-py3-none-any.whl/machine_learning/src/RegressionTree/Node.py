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

    def __eq__(self, other: 'Node'):
        return self.split_feature == other.split_feature and \
            self.split_value == other.split_value and \
            self.depth == other.depth and \
            self.is_leaf == other.is_leaf

    def __hash__(self):
        return hash((self.split_feature, self.split_value, self.depth, self.is_leaf))
