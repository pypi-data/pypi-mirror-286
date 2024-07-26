import pickle
from typing import List

import numpy as np

from ..Utils.DataPoint import DataPoint
from ..Utils.progress_bar import ProgressBar
from .Layer import Layer


class NeuralNetwork:
    def __init__(self, layers: List[Layer]) -> None:
        self.layers = layers
        self.velocity_w = [np.zeros_like(layer.weights) for layer in layers]
        self.velocity_b = [np.zeros_like(layer.biases) for layer in layers]

    def calculateOutputs(self, inputs: np.ndarray) -> np.ndarray:
        for layer in self.layers:
            inputs = layer.calculateOutputs(inputs)
        return inputs

    def _classify(self, inputs: np.ndarray) -> np.intp:
        outputs = self.calculateOutputs(inputs)
        return np.argmax(outputs)

    def classify(self, inputs: List[DataPoint]) -> List[np.intp]:
        preds = []
        for point in inputs:
            pred = self._classify(point.inputs)
            preds.append(pred)
        return preds

    def _cost(self, data_point: DataPoint) -> float:
        outputs = self.calculateOutputs(np.array(data_point.inputs))
        output_layer = self.layers[-1]

        cost = 0.0
        for out_node in range(len(outputs)):
            cost += output_layer.nodeCost(
                outputs[out_node], data_point.expected_outputs[out_node]
            )
        return cost

    def cost(self, data_points: List[DataPoint]) -> float:
        total_cost = 0.0
        for data_point in data_points:
            total_cost += self._cost(data_point)
        return total_cost / len(data_points)

    def learn(
        self,
        training_data: List[DataPoint],
        learning_rate: float,
        batch_size: int,
        momentum: float = 0.9,
    ) -> float:
        batches = [
            training_data[k : k + batch_size]
            for k in range(0, len(training_data), batch_size)
        ]

        for batch in batches:
            nabla_w = [np.zeros_like(layer.weights) for layer in self.layers]
            nabla_b = [np.zeros_like(layer.biases) for layer in self.layers]

            for data_point in batch:
                activation = np.array(data_point.inputs)
                activations = [activation]
                zs = []
                for layer in self.layers:
                    z = np.dot(activation, layer.weights) + layer.biases
                    zs.append(z)
                    activation = layer._activationFunction(z)
                    activations.append(activation)

                delta = (
                    activations[-1] - np.array(data_point.expected_outputs)
                ) * self.layers[-1]._activationFunctionDerivative(zs[-1])
                nabla_b[-1] += delta
                nabla_w[-1] += np.outer(activations[-2], delta)

                for layer_idx in range(2, len(self.layers) + 1):
                    z = zs[-layer_idx]
                    sp = self.layers[-layer_idx]._activationFunctionDerivative(z)
                    delta = np.dot(delta, self.layers[-layer_idx + 1].weights.T) * sp
                    nabla_b[-layer_idx] += delta
                    nabla_w[-layer_idx] += np.outer(activations[-layer_idx - 1], delta)

            for i, layer in enumerate(self.layers):
                self.velocity_w[i] = (
                    momentum * self.velocity_w[i]
                    - (learning_rate / len(batch)) * nabla_w[i]
                )
                self.velocity_b[i] = (
                    momentum * self.velocity_b[i]
                    - (learning_rate / len(batch)) * nabla_b[i]
                )
                layer.weights += self.velocity_w[i]
                layer.biases += self.velocity_b[i]

        return self.cost(training_data)

    def train(
        self,
        iterations: int,
        data_points: List[DataPoint],
        learning_rate: float,
        batch_size: int,
        decay: float = 1e-7,
        momentum: float = 0.9,
    ) -> List[float]:
        cost = None
        costs = []
        progress = ProgressBar(total=iterations, program_name="training.", cost=cost)
        for _ in range(iterations):
            # learning_rate = learning_rate * (1.0 / 1.0 + decay * iterations)
            cost = self.learn(data_points, learning_rate, batch_size, momentum)
            progress.increment(cost=cost)
            costs.append(cost)
        return costs

    def save_model(self, file_path: str):
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_model(cls, file_path: str) -> "NeuralNetwork":
        with open(file_path, "rb") as file:
            return pickle.load(file)
