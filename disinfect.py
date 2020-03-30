import time
import gpiozero
import digitalio
import board

from multiprocessing import Process
from gpiozero import Button
from gpiozero import Servo
from gpiozero import LED
from gpiozero import Buzzer
from signal import pause

lamp = gpiozero.OutputDevice(4, active_high=False, initial_value=False)
fan = gpiozero.OutputDevice(3, active_high=False, initial_value=False)

# GPIO PINS
button = Button(26)
button_led = LED(25)
red_led = LED(16)
white_led = LED(21)
buzzer = Buzzer(5)
servo = Servo(17)

servo.value = None  # if you don't have this, servo will start moving immediately when program starts

door_sensor = digitalio.DigitalInOut(board.D23)  # Door sensor on gpio pin 23
door_sensor.direction = digitalio.Direction.INPUT


def kill_switch():
    print('kill switch active')
    while True:
        if door_sensor.value:
            print('DOOR OPEN!')
            lamp.off()
            buzzer.on()
            time.sleep(1.5)
            buzzer.off()
        time.sleep(0.25)


def disinfect():
    print('running')
    servo.value = 0.0
    button_led.on()

    # Short beep when function runs after button press
    buzzer.on()
    time.sleep(0.25)
    buzzer.off()

    fan.on()
    lamp.on()
    servo.max()
    red_led.on()
    time.sleep(15)  # 15 seconds (Can change this to however long you want)

    lamp.off()
    servo.value = None
    red_led.off()

    # Two short beeps when lamp runtime expires
    buzzer.on()
    time.sleep(.25)
    buzzer.off()
    buzzer.on()
    time.sleep(.25)
    buzzer.off()

    # run fan for extra 5 seconds
    time.sleep(5)
    fan.off()



if __name__ == '__main__':
    button_led.on()
    buzzer.on()  # Short beep at startup
    time.sleep(0.25)
    buzzer.off()

    # Start monitoring door status
    process_1 = Process(target=kill_switch)
    process_1.start()

    button.when_pressed = disinfect
    print('main process started')
    pause()  # Wait and listen for button press
