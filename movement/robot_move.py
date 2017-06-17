import sys
import termios
import tty
import nxt
from nxt.motor import *
from detection.shape_detection import Arrows


def getch():
    """
    Read a single keypress from stdin and return the resulting character.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        control = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return control


def control_robot():
    """
    Control move of the robot via keyboard via arrows.
    """
    b = nxt.locator.find_one_brick()
    motor_c = Motor(b, PORT_C)
    motor_a = Motor(b, PORT_A)
    two_motors = nxt.SynchronizedMotors(motor_c, motor_a, 0)
    two_motors_c = nxt.SynchronizedMotors(motor_c, motor_a, 100)
    two_motors_a = nxt.SynchronizedMotors(motor_c, motor_a, 100)
    control = ' '
    while(control):
        control = getch()
        if control == 'A':
            two_motors.turn(100, 360, False)
        elif control == 'B':
            two_motors.turn(-100,360, False)
        elif control == 'D':
            two_motors_c.turn(100, 90, False)
        elif control == 'C':
            two_motors_a.turn(100, 90, False)


def process_arrow(arrow):
    """
    Turn the robot in the direction determined by arrow parameter.
    """

    b = nxt.locator.find_one_brick()
    motor_c = Motor(b, PORT_C)
    motor_a = Motor(b, PORT_A)
    two_motors = nxt.SynchronizedMotors(motor_c, motor_a, 0)
    two_motors_c = nxt.SynchronizedMotors(motor_c, motor_a, 100)
    two_motors_a = nxt.SynchronizedMotors(motor_c, motor_a, 100)

    if arrow == Arrows.left:
        two_motors_c.turn(100, 90, False)
        return
    if arrow == Arrows.right:
        two_motors_a.turn(100, 90, False)
        return
    if arrow == Arrows.straight:
        two_motors.turn(100, 360, False)
        return







