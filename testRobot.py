# ****************************************************
# Filename: testRobot.py
# Creater: Joe
# Description: Tests robot.py module
# ****************************************************

import robot

def main():
    try:
        rob = robot.Robot()
        rob.forward(30, 20)
    except:
        rob.stop()
        del rob

if __name__ == '__main__':
    main()