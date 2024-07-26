from typing import List, Tuple

import pandas as pd

from .DataPoint import DataPoint


def trainTestSplit(
    df: pd.DataFrame, ratio: float = 0.8
) -> Tuple[List[DataPoint], List[DataPoint]]:
    data_points = []
    cols = df.columns
    inputs = []
    for i in range(len(df[cols[0]])):
        inputs = [df[cols[j]][i] for j in range(len(cols) - 1)]
        output = df[cols[-1]][i]
        expected_outputs = [0.0] * (int(df[cols[-1]].max()) + 1)
        expected_outputs[int(output)] = 1.0
        data_points.append(DataPoint(inputs, expected_outputs))

    train_data = data_points[: int(ratio * len(data_points))]
    test_data = data_points[int(ratio * len(data_points)) :]

    return train_data, test_data
