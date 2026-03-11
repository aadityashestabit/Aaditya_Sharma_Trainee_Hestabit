import pandas as pd

url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"

df = pd.read_csv(url)

df.to_csv("src/data/raw/diabetes.csv", index=False)

print("Dataset downloaded and saved to src/data/raw/heart_disease.csv")