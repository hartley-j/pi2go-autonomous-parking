# ****************************************************
# Filename: testRobot.py
# Creater: Joe
# Description: Tests robot.py module
# ****************************************************

import robot
from time import sleep

def testFoward():
    try:
        rob = robot.Robot()
        rob.forward(30, 10)
    except:
        rob.stop()
        del rob

def testTurn():
    rob = robot.Robot()
    rob.rotateAngle(deg=90, speed=50)

def test1():
    rob = robot.Robot()
    print(rob.heading.getMedianHeading(nmax=10))
    # Compare the heading against a compass
    del rob

def test2():
    rob = robot.Robot()
    print(rob.heading.getMedianHeading(nmax=10))
    # Rotate the robot 20 degrees clockwise using compass
    sleep(10)
    print(rob.heading.getMedianHeading(nmax=10))
    del rob

def test3():
    rob = robot.Robot()
    # Rotate 90 degrees clockwise:
    rob.rotateAngle(90, speed=30,tolerance=10)
    # Rotate 90 degrees anti-clockwise:
    rob.rotateAngle(-90, speed=30, tolerance=10)
    del rob

def test4():
    rob = robot.Robot()
    # Input angle larger than 180:
    rob.rotateAngle(270, speed=30,tolerance=10)
    del rob

def test5():
    rob = robot.Robot()
    # Input angle smaller than -180:
    rob.rotateAngle(-300, speed=30,tolerance=10)
    del rob

def test6():
    rob = robot.Robot()
    # Move forward 10cm:
    rob.forward(10)
    del rob

if __name__ == '__main__':
    testFoward()