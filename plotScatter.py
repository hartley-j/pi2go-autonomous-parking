import pandas as pd
import seaborn as sns

df = pd.read_csv('D:/Personal files/Documents/testICM_scatterplot2.txt')
df["x1"] = df['x'] * -1
df["y1"] = df['y'] * -1
sns.scatterplot(data=df, x='x1', y='y1', hue='heading')