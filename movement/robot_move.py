import sys
import termios
import time
import tty
import nxt
from nxt.motor import *
from detection.shape_detection import Arrows


class Robot_move:
    def __init__(self):
        #print "czemu:(?"
        self.b = nxt.locator.find_one_brick()
        self.motor_c = Motor(self.b, PORT_C)
        self.motor_a = Motor(self.b, PORT_A)
        self.two_motors = nxt.SynchronizedMotors(self.motor_c, self.motor_a, 0)
        self.two_motors_c = nxt.SynchronizedMotors(self.motor_c, self.motor_a, 100)
        self.two_motors_a = nxt.SynchronizedMotors(self.motor_a, self.motor_c, 100)
        #self.two_motors_a.turn(100, 90, False)
        #self.two_motors_c.turn(100, 90, False)

    def getch(self):
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

    def process_arrow(self, arrow):
        """
        Turn the robot in the direction determined by arrow parameter.
        """

        if arrow == Arrows.left :
            print 'left'
            self.two_motors_c.turn(100, 90, False)
            #time.sleep(5)
            #self.two_motors.turn(-100, 360, False)
            #self.two_motors.turn(-100, 360, False)
            #time.sleep(5)
            return
        if arrow == Arrows.right:
            print 'right'
            self.two_motors_a.turn(100, 90, False)
            #time.sleep(5)
            #self.two_motors.turn(-100, 360, False)
            #self.two_motors.turn(-100, 360, False)
            #time.sleep(5)
            return
        if arrow == Arrows.straight:
            print 'straight'
            self.two_motors.turn(-100, 360, False)
            #time.sleep(5)
            #self.two_motors.turn(-100, 360, False)
           # self.two_motors.turn(-100, 360, False)
            #time.sleep(5)

            return







