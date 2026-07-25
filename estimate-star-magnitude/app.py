from pprint import pprint 

from regression_tree import RegressionTree


with open("data/final_dataset.csv", "r") as f:
    raw_records = f.readlines()


records = []

for idx, raw_record in enumerate(raw_records):
    if idx == 0:
        # ignore header
        continue

    temperature, radius, abs_mag = map(float, raw_record.replace("\n", "").split(","))

    records.append(
        {
            "temperature": temperature,
            "radius": radius,
            "abs_mag": abs_mag,
        }
    )


model = RegressionTree(
    data=records,
    feature_names=["temperature", "radius"],
    target_name="abs_mag",
)

model.train(depth=7)


result = model.predict(
    example={"temperature": 30000, "radius": 6.3}
)

print(result)


# Mean Squared Error
def mse_score(y_true: list, y_pred: list) -> float:
    n = len(y_true)
    return sum((true - pred)**2 for true, pred in zip(y_true, y_pred)) / n


# depth: 5, mse_score: 1.2797605959821186
# depth: 7: mse_score: 0.49837338902686035

print(
    mse_score(
        y_true=[record["abs_mag"] for record in records],
        y_pred=[model.predict(record) for record in records]
    )
)