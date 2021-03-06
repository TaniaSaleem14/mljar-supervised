import numpy as np
import copy
from supervised.algorithms.registry import AlgorithmsRegistry
from supervised.algorithms.registry import BINARY_CLASSIFICATION


class HillClimbing:

    """
    Example params are in JSON format:
    {
        "booster": ["gbtree", "gblinear"],
        "objective": ["binary:logistic"],
        "eval_metric": ["auc", "logloss"],
        "eta": [0.0025, 0.005, 0.0075, 0.01, 0.025, 0.05, 0.075, 0.1]
    }
    """

    @staticmethod
    def get(params, ml_task, seed=1):
        np.random.seed(seed)
        keys = list(params.keys())
        if "num_class" in keys:
            keys.remove("num_class")
        keys.remove("model_type")
        keys.remove("seed")
        keys.remove("ml_task")

        model_type = params["model_type"]
        if model_type == "Baseline":
            return [None, None]
        model_info = AlgorithmsRegistry.registry[ml_task][model_type]
        model_params = model_info["params"]

        permuted_keys = np.random.permutation(keys)
        key_to_update = None
        for key_to_update in permuted_keys:
            values = model_params[key_to_update]
            if len(values) > 1:
                break

        left, right = None, None
        for i, v in enumerate(values):
            if v == params[key_to_update]:
                if i + 1 < len(values):
                    right = values[i + 1]
                if i - 1 >= 0:
                    left = values[i - 1]

        params_1, params_2 = None, None
        if left is not None:
            params_1 = copy.deepcopy(params)
            params_1[key_to_update] = left
        if right is not None:
            params_2 = copy.deepcopy(params)
            params_2[key_to_update] = right

        return [params_1, params_2]
