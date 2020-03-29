import sys
import time
import gpiozero
import RPi.GPIO as GPIO  # needed for the reedswitch
from gpiozero import Button
from gpiozero import Servo
from gpiozero import LED
from gpiozero import Buzzer
from signal import pause

relay = gpiozero.OutputDevice(4, active_high=False, initial_value=False)
fan = gpiozero.OutputDevice(3, active_high=False, initial_value=False)

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

GPIO.setup(22, GPIO.IN) # GPIO Assign mode

reedswitch = GPIO.input(22)
button = Button(26)
button_led = LED(25)
red_led = LED(16)
white_led = LED(21)
buzzer = Buzzer(5)
servo = Servo(17)
servo.value = None  # if you don't have this, servo will start moving immediately



def play_buzzer():
    buzzer.on()
    time.sleep(0.25)
    buzzer.off()
    time.sleep(0.25)
    buzzer.off()

def kill_switch(seconds):
    n = 1
    while True:
        
        if reedswitch == 1:
            relay.off()
        time.sleep(1)
        n + 1
        if n == seconds:
            break

def disinfect():
    print('running')
    servo.value = 0.0
    
    if reedswitch == 0:
        buzzer.on()
        time.sleep(0.25)
        buzzer.off()
        fan.on()
        relay.on()
        servo.max()
        red_led.on()
        
        #time.sleep(15)  # 30 Minutes
        kill_switch(10)
        
        relay.off()
        fan.off()
        servo.value = None
        red_led.off()
        #play_buzzer()
        #play_buzzer()
    
    else:
        print('door open!')
        #buzzer.on()
        #time.sleep(1)
        #buzzer.off()

if __name__ == '__main__':
    
    button_led.on()
    button.when_pressed = disinfect
    pause() # this is needed or else the program will end immediately and not wait for button press

  
