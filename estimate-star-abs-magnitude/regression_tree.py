class TreeNode:
    def __init__(self, examples, features_names: list[str], target_name: str):
        self.examples: list = examples
        self.features_names = features_names
        self.target_name = target_name
        self.left = None
        self.right = None
        self.split_point = None

    def split(self, depth: int = 10):
        if len(self.examples) == 1 or depth <= 0:
            return

        # look for the split point which minimizes the MSE
        best_split_point = {
            "feature": None,
            "value": None,
            "mse": float("inf"),
            "split_index": None
        }

        for feature in self.features_names:
            # order examples using the values of the current feature to get the split points
            self.examples.sort(key=lambda example : example[feature])

            # each split point will be the avg between two adjacent values
            for i in range(len(self.examples) - 1):
                split_point = (self.examples[i][feature] + self.examples[i+1][feature]) / 2

                # compute mse to determine if it's the best split point
                mse, split_idx = self.__get_split_point_mse(feature, split_point)

                #print(f'{best_split_point["mse"]=}', f"{mse=}")
                if mse is not None and best_split_point["mse"] > mse:
                    best_split_point = {
                        "feature": feature,
                        "value": split_point,
                        "mse": mse,
                        "split_index": split_idx
                    }

        self.split_point = best_split_point
        print(f"{best_split_point=}")
        self.examples.sort(key=lambda example: example[self.split_point["feature"]])

        self.left = TreeNode(
            self.examples[:self.split_point["split_index"]],
            self.features_names,
            self.target_name
        )
        self.left.split(depth - 1)

        self.right = TreeNode(
            self.examples[self.split_point["split_index"]:],
            self.features_names,
            self.target_name,
        )
        self.right.split(depth - 1)


    def __get_split_point_mse(self, feature: str, split_point: float):
        left_labels = [example[self.target_name] for example in self.examples if example[feature] <= split_point]
        right_labels = [example[self.target_name] for example in self.examples if example[feature] > split_point]

        # we want to know if it's really has splitted the examples
        if not len(left_labels) or not len(right_labels):
            return None, None
        
        left_mse = get_variance(left_labels)
        right_mse = get_variance(right_labels)
        num_samples = len(left_labels) + len(right_labels)

        mse = ((len(left_labels) * left_mse) + (len(right_labels) * right_mse)) / num_samples

        # marks the idx where the values before belong to the left child
        split_index = len(left_labels)

        return mse, split_index


def get_variance(values: list) -> float:
    """Computes node impurity with variance (it's a version of the mean squared error score).
    Instad of using the expected value we use the average, which at the end for the mode it must be the 
    value predicted."""
    n = len(values)
    avg = sum(values) / n

    mse = 0

    for value in values:
        mse += (avg - value)**2

    return mse / n


class RegressionTree:
    def __init__(self, examples, features_names: list[str], target_name: str):
        # Don't change the following two lines of code.
        self.root = TreeNode(examples, features_names, target_name)
        self.target_name = target_name
        # self.train()

    def train(self, depth: int = 10):
        # Don't edit this line.
        self.root.split(depth)

    def predict(self, example):
        node = self.root

        while node.left and node.right:
            if example[node.split_point["feature"]] <= node.split_point["value"]:
                node = node.left
            else:
                node = node.right

        leaf_labels = [leaf[self.target_name] for leaf in node.examples]

        return sum(leaf_labels) / len(node.examples)

    def print(self):
        queue = list()
        queue.append(self.root)
        queue.append(None)

        while len(queue) > 0:
            node: TreeNode = queue.pop(0)

            if not node:
                if len(queue) > 0:
                    queue.append(None)
                print("")
            else:
                print(node.split_point, end=" ")

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)