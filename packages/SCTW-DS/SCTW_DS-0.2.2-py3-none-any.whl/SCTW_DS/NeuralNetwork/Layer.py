from dataclasses import dataclass, field
from typing import Callable, Dict

import numpy as np


@dataclass
class Layer:
    num_nodes_in: int
    num_nodes_out: int
    activation_function: str
    error_func: str = "mse"
    weights: np.ndarray = field(init=False)
    cost_gradient_w: np.ndarray = field(init=False)
    biases: np.ndarray = field(init=False)
    cost_gradient_b: np.ndarray = field(init=False)
    nodeCost: Callable[[np.ndarray, np.ndarray], float] = field(init=False)
    _activationFunction: Callable[[np.ndarray], np.ndarray] = field(init=False)
    _activationFunctionDerivative: Callable[[np.ndarray], np.ndarray] = field(
        init=False
    )

    def __post_init__(self):
        self.weights = np.random.randn(self.num_nodes_in, self.num_nodes_out) / np.sqrt(
            self.num_nodes_in
        )
        self.biases = np.random.randn(self.num_nodes_out)
        self.cost_gradient_w = np.zeros((self.num_nodes_in, self.num_nodes_out))
        self.cost_gradient_b = np.zeros(self.num_nodes_out)

        cost_map: Dict[str, Callable[[np.ndarray, np.ndarray], float]] = {
            "mse": self._mse,
            "cross_entropy": self._cross_entropy,
        }
        activation_map: Dict[str, Callable[[np.ndarray], np.ndarray]] = {
            "sigmoid": self._sigmoid,
            "relu": self._relu,
            "leaky_relu": self._leaky_relu,
            "tanh": self._tanh,
            "softmax": self._softmax,
        }
        derivative_map: Dict[str, Callable[[np.ndarray], np.ndarray]] = {
            "sigmoid": self._sigmoid_derivative,
            "relu": self._relu_derivative,
            "leaky_relu": self._leaky_relu_derivative,
            "tanh": self._tanh_derivative,
            "softmax": self._softmax_derivative,
        }

        self.nodeCost = cost_map[self.error_func]
        self._activationFunction = activation_map[self.activation_function]
        self._activationFunctionDerivative = derivative_map[self.activation_function]

    def calculateOutputs(self, inputs: np.ndarray) -> np.ndarray:
        weighted_input = np.dot(inputs, self.weights) + self.biases
        return self._activationFunction(weighted_input)

    def applyGradient(self, learn_rate: float):
        self.weights -= learn_rate * self.cost_gradient_w
        self.biases -= learn_rate * self.cost_gradient_b

    @staticmethod
    def _mse(y_true: float, y_pred: float) -> float:
        return (y_true - y_pred) ** 2

    @staticmethod
    def _cross_entropy(y_true: float, y_pred: float) -> float:
        return -np.sum(y_true * np.log(y_pred + 1e-9))

    @staticmethod
    def _sigmoid(z: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-z))

    @staticmethod
    def _sigmoid_derivative(z: np.ndarray) -> np.ndarray:
        s = Layer._sigmoid(z)
        return s * (1 - s)

    @staticmethod
    def _relu(z: np.ndarray) -> np.ndarray:
        return np.maximum(0, z)

    @staticmethod
    def _relu_derivative(z: np.ndarray) -> np.ndarray:
        return (z > 0).astype(float)

    @staticmethod
    def _leaky_relu(z: np.ndarray) -> np.ndarray:
        return np.where(z > 0, z, 0.01 * z)

    @staticmethod
    def _leaky_relu_derivative(z: np.ndarray) -> np.ndarray:
        return np.where(z > 0, 1, 0.01)

    @staticmethod
    def _tanh(z: np.ndarray) -> np.ndarray:
        return np.tanh(z)

    @staticmethod
    def _tanh_derivative(z: np.ndarray) -> np.ndarray:
        return 1.0 - np.tanh(z) ** 2

    @staticmethod
    def _softmax(z: np.ndarray) -> np.ndarray:
        e_z = np.exp(z - np.max(z))
        return e_z / e_z.sum(axis=0, keepdims=True)

    @staticmethod
    def _softmax_derivative(z: np.ndarray) -> np.ndarray:
        s = Layer._softmax(z)
        return s * (
            1 - s
        )  # Note: Typically used with the Jacobian matrix for accurate calculations
