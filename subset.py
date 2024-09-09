import pandas as pd

df = pd.read_csv("email.csv")

subset_df = df.sample(frac= 0.0001)

subset_df.to_csv("email_subset.csv", index = False)
