# ****************************************************
# Filename: plotScatter.py
# Creater: Joe
# Description: Plots a series of graphs from raw mag data
# ****************************************************

# Imports required packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

# Reads data from csv files and outputs a pandas dataframe
def readData(name="test360Spin.csv"):
    if name == "NSEW":
        df = pd.read_csv("D:/Personal files/Documents/testICM_scatterplot2.txt")
    else:
        df = pd.read_csv(name)
    return df

# Plots a graph and groups data by heading (either N, S, E or W)
def plotNSEW(df):
    sns.set_theme(style="whitegrid")
    g = sns.scatterplot(data=df, x='x1', y='y1', hue='heading')
    g.set_title("Scatter plot of Raw Mag Data at NSEW")
    plt.savefig("D:/Personal files/Documents/scatterNSEW.png")

# Plots a scatter graph
def plotCircleScatter(df, hue=None,title=None, filename=None):
    sns.set_theme(style="whitegrid")
    if hue:
        g = sns.scatterplot(data=df, x='x1', y='y1',hue=hue, cmap="viridis")
    else:
        g = sns.scatterplot(data=df, x='x1', y='y1')
    g.set_title(title)
    plt.savefig(f"D:/Personal files/Documents/{filename}")

# Calibrates input dataframe
def calibrateData(df):
    df["x1"] = df['x'] * -1
    df["y1"] = df['y'] * -1

    xmax = df["x1"].max()
    xmin = df["x1"].min()
    ymax = df["y1"].max()
    ymin = df["y1"].min()

    df["x1"] -= xmin
    df["x1"] /= (xmax - xmin)
    df["x1"] -= 0.5


    df["y1"] -= ymin
    df["y1"] /= (ymax - ymin)
    df["y1"] -= 0.5

    minmax = [xmin, ymin, xmax, ymax]
    print(minmax)

    return df


# Calculates heading from dataframe
def headingCalc(df):
    df["heading"] = [math.degrees(math.atan2(df["x1"].to_numpy()[i], df["y1"].to_numpy()[i])) for i in np.arange(len(df["x1"]))]
    # We want the heading, which is the angle from North which, in our case, lies on the Y axis.
    # Atan2 takes the arguments atan2(y, x) to find the angle from the X axis. However, we want the angle from the Y axis so we switch it around.

    return df

# Main function
def main():
    df = readData("NSEW")
    df["x1"] = df['x'] * -1
    df["y1"] = df['y'] * -1
    plotNSEW(df)

    df = readData("test360Spin.csv")
    df["x1"] = df['x']
    df["y1"] = df['y']
    plotCircleScatter(df, title="Scatter plot Uncalibrated Data", filename="uncalibratedDataSctter.png")
    df = calibrateData(df)
    plotCircleScatter(df, title="Scatter plot Calibrated Data", filename="calibratedDataSctter.png")

    df = headingCalc(df)
    plotCircleScatter(df, hue="heading", title="Scatter plot Calibrated Data with Heading", filename="calibratedDataSctterHeading.png")

    plotCircleScatter(calibrateddf, hue="heading", title="Scatter plot Calibrated Data with Heading",
                      filename="calibratedDataSctterHeading.png")


if __name__ == "__main__":
    main()