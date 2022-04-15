import pi2go
from heading import Compass
from time import sleep


def main():
    try:
        heading = Compass()
        pi2go.init()
        pi2go.spinRight(50)
        while True:
            print(heading.getHeading())
            sleep(0.25)

    except KeyboardInterrupt:
        pi2go.go(0, 0)
        pi2go.cleanup()

def currentHeading():
    try:
        heading = Compass()

        while True:
            print(heading.getHeading())
            sleep(0.01)
    except:
        del heading

def faceNorth():
    pi2go.init()
    heading = Compass()

    if heading.getHeading() != 0:
        isNorth = False
        pi2go.spinRight(35)
    else:
        isNorth = True

    while not isNorth:
        currentHead = heading.getHeading()
        print(currentHead)
        if -10 < currentHead < 10:
            break

    pi2go.go(0, 0)


def plotHeadingUncertainty():
    '''
    Capture data by manually pointing the pi2go in N-E-S-W directions, and capturing x number of heading observations
    - How many observations of heading do we need in order to have a stable heading value?
    - Is median or mean the best measure?
    '''
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    # On the pi2go, run the following code:
    # python calibrateIMU.py
    # git add calibration_manual.txt
    # git add calibration.txt
    # git commit -m "calibration files from the pi2go"
    # git push

    # Load DataFrame
    df = pd.read_csv("calibration_manual.txt", names=['n', 'x', 'y', 'z', 'obs'])
    sns.scatterplot(data=df, x='x', y='y', hue='obs')
    plt.savefig("plots/NESW_scatterplot.png")

    sns.histplot(data=df.loc[df['obs'] == 'N', 'y']).set(title="North | Y coordinate")
    plt.savefig("plots/calibrate_maxY_histogram.png")
    plt.close()
    sns.histplot(data=df.loc[df['obs'] == 'S', 'y']).set(title="South | Y coordinate")
    plt.savefig("plots/calibrate_minY_histogram.png")
    plt.close()
    sns.histplot(data=df.loc[df['obs'] == 'W', 'x']).set(title="West | X coordinate")
    plt.savefig("plots/calibrate_minX_histogram.png")
    plt.close()
    sns.histplot(data=df.loc[df['obs'] == 'E', 'x']).set(title="East | X coordinate")
    plt.savefig("plots/calibrate_maxX_histogram.png")
    plt.close()

    # Plot Z for each angle (not really sure what this means)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='n', y='z', hue='obs')
    plt.savefig("plots/calibrate_Z_histogram.png")
    plt.close()


if __name__ == "__main__":
    faceNorth()
