import curses, sys, os
from car import Car

#user interface
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

def printscreen():
        # The command os.system('clear') clears the screen.
        os.system('clear')
        print("============ RC car controller ============\r")
        print(u"\u2191/\u2193: accelerate/brake\r")
        print(u"\u2190/\u2192: left/right\r")
        print("q:   stops the motor and exit\r")
        print("x:   exit the program\r")
        print("s:   start the program\r")
        
car = Car()
while True:
    printscreen()
    print(car)
    char = screen.getch()
    if char == ord('q'):
        car.stopDriving()
        break
    elif char == ord('-'):
        car.centerSteering()
    elif char == ord('s'):
        print("lets start driving!")
        car.beginDriving()
    elif char == curses.KEY_UP:
        print('forward')
        car.forward()
    elif char == curses.KEY_DOWN:
        print('reverse')
        car.backward()
    elif char == curses.KEY_RIGHT:
        print('right')
        car.turnRight()
    elif char == curses.KEY_LEFT:
        print('left')
        car.turnLeft()
    car.updatePwm()
    
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()