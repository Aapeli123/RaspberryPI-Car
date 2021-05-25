import Adafruit_PCA9685
from time import sleep

class Car:
    """
    Car represents a single remote controllable car.
    It can be driven with methods like forward and backward.
    It can be steered using the methods turnLeft, turnRight and centerSteering

    Before driving call beginDriving and to stop driwing call stopDriving

    To send data to physical servos you should call updatePwm
    """
    #ESC Brushles motor states: direction, on/off
    __toggleState = 400
    __init_throttle = 430
    __delta_throttle = 20

    #steering pwm values for Servo
    __steering_center = 370
    __steering_max_left = 530
    __steering_min_right = 210
    __delta_steering = 20

    #max values for throttle:
    __fwdmax = 600
    __revmin = 200

    def __init__(self):
        self.__pwm = Adafruit_PCA9685.PCA9685()
        self.__pwm.set_pwm_freq(60)

        self.__driving = False
        if self. __init_throttle >self.__toggleState:
            self.dir = 1
        else:
            self.dir =-1

        #control values for servo and esc
        self.__throttle_pwm =self. __init_throttle
        self.__steering_pwm = self.__steering_center
    
    def beginDriving(self):
        self.__driving = True
        self.__pwm.set_pwm(2,0, self.__toggleState)
        sleep(0.1)

    def stopDriving(self):
        self.__pwm.set_pwm(2, 0, self.__toggleState)
        self.__pwm.set_pwm(1, 0, self.__steering_center)
        sleep(0.1)

    def __hasNotChanged(self):
        return self.__throttle_pwm == self.__init_throttle and not self.__driving 

    def forward(self):
        if self.__hasNotChanged():
            sleep(0.1)
            return
        if self.__throttle_pwm + self.__delta_throttle < self.__fwdmax:
            self.__throttle_pwm += self.__delta_throttle
        if self.__throttle_pwm > self.__toggleState and self.dir < 0:
                self.__pwm.set_pwm(2,0,self.__toggleState)
                self.dir = 1
                sleep(0.1)

    def __prepareBackward(self):
        pass


    def backward(self):
        if self.__hasNotChanged():
            sleep(0.1)
            return
        if self.__throttle_pwm - self.__delta_throttle > self.__revmin:
            self.__throttle_pwm -= self.__delta_throttle
            if self.__throttle_pwm < self.__toggleState and self.dir > 0:
                self.__pwm.set_pwm(2,0,self.__toggleState)
                self.dir = -1
                sleep(0.1)
            
    
    def turnRight(self):
        self.__steering_pwm -= self.__delta_steering
        self.__steering_pwm = max(self.__steering_min_right, self.__steering_pwm)

    def turnLeft(self):
        self.__steering_pwm += self.__delta_steering
        self.__steering_pwm = min(self.__steering_max_left, self.__steering_pwm)

    def centerSteering(self):
        self.__steering_pwm = self.__steering_center

    def updatePwm(self):
        self.__pwm.set_pwm(2, 0,self.__throttle_pwm)
        self.__pwm.set_pwm(1, 0,self.__steering_pwm)
        sleep(0.2)
    
    def __str__(self):
        direction = "Forward" if self.dir == 1 else "Backwards"
        return "Car: Driving: {}, Direction {}, Steering: {}, Throttle: {}".format(
            self.__driving, direction, self.__steering_pwm, self.__throttle_pwm
        )
