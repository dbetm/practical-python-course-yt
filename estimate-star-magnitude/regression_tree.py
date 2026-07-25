from typing import List, Optional


class TreeNode:
    def __init__(self, data: List[dict], feature_names: List[str], target_name: str):
        self.data: list = data
        self.feature_names = feature_names
        self.target_name = target_name
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
        # feature: str, value: Any, error: float, split_index: int
        self.split_point: Optional[dict] = None
    
    def split(self, depth: int = 10):
        if len(self.data) == 1 or depth == 0:
            return

        """
        [
            {"temperature": 2600, "radius": 0.102, "abs_mag": 18.7},
            {"temperature": 2800, "radius": 0.16, "abs_mag": 16.65},
            {"temperature": 3042, "radius": 0.1542, "abs_mag": 16.6},
            {"temperature": 3068, "radius": 0.17, "abs_mag": 16.12},
        ]

        1. Iterar features
            1.1 Ordenar los datos con el feature actual
            1.2 Obtener split points (calculando el promedio entre data points adyacentes)
            1.3 Calcular el error y obtener el índice
            1.4 Checar si hemos encontrado un mejor best_split_point
        2. Asignar self.split_point
        3. Ordenar datos con el feature obtenido del best_split_point
        4. Instanciar nodo izquierda con los datos de la izquierda del split_index
            4.1 llamar split (algoritmo DFS)
        5. Instanciar nodo derecha con los datos de la derecha del split_index
            4.1 llamar split (algoritmo DFS)
        6. Detener recursividad (caso base) cuando solo tengamos un data point 
            o cuando hayamos alcanzado la máxima profundidad deseada.
        """
        best_split_point = {
            "feature": None,
            "value": None,
            "error": float("inf"),
            "split_index": None,
        }

        for feature in self.feature_names:
            self.data.sort(key=lambda x : x[feature])

            # each split will be the average between two adjacent values
            for i in range(len(self.data) - 1):
                split_point = (self.data[i][feature] + self.data[i + 1][feature]) / 2

                error, split_idx = self.__get_split_point_idx_and_error(feature, split_point)

                if error is not None and best_split_point["error"] > error:
                    best_split_point = {
                        "feature": feature,
                        "value": split_point,
                        "error": error,
                        "split_index": split_idx,
                    }
        
        self.split_point = best_split_point
        self.data.sort(key=lambda x : x[self.split_point["feature"]])

        self.left = TreeNode(
            self.data[:self.split_point["split_index"]],
            self.feature_names, 
            self.target_name,
        )
        self.left.split(depth - 1)

        self.right = TreeNode(
            self.data[self.split_point["split_index"]:],
            self.feature_names, 
            self.target_name,
        )
        self.right.split(depth - 1)


    def __get_split_point_idx_and_error(self, feature: str, split_point: float) -> tuple:
        left_labels = [
            example[self.target_name] for example in self.data if example[feature] <= split_point
        ]
        right_labels = [
            example[self.target_name] for example in self.data if example[feature] > split_point
        ]

        if not len(left_labels) or not len(right_labels):
            return None, None

        left_variance = get_variance(left_labels)
        right_variance = get_variance(right_labels)

        num_examples = len(left_labels) + len(right_labels)

        error = ( (len(left_labels) * left_variance) + (len(right_labels) * right_variance)) / num_examples

        split_idx = len(left_labels)

        return error, split_idx



def get_variance(values: list) -> float:
    n = len(values)
    avg = sum(values) / n

    acc_value = 0
    for value in values:
        acc_value += (value - avg)**2

    return acc_value / n



class RegressionTree:
    def __init__(self, data: List[dict], feature_names: List[str], target_name: str):
        self.target_name = target_name
        self.root = TreeNode(data, feature_names, target_name)

    def train(self, depth: int = 10):
        self.root.split(depth)

    def predict(self, example: dict) -> float:
        node = self.root

        while node.left and node.right:
            if example[node.split_point["feature"]] <= node.split_point["value"]:
                node = node.left
            else:
                node = node.right

        leaf_labels = [example[self.target_name] for example in node.example]

        return sum(leaf_labels) / len(node.examples)