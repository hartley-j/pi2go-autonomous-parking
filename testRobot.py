# ****************************************************
# Filename: testRobot.py
# Creater: Joe
# Description: Tests robot.py module
# ****************************************************

import robot

def testFoward():
    try:
        rob = robot.Robot()
        rob.forward(30, 50)
    except:
        rob.stop()
        del rob

def testTurn():
    rob = robot.Robot
    rob.rotateAngle(deg=90, speed=50)

if __name__ == '__main__':
    testTurn()