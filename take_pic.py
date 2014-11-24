import RPi.GPIO as GPIO
import sys

GROUND = int(sys.argv[0])  # WHITE
FOCUS = int(sys.argv[1])   # YELLOW
SHUTTER = int(sys.argv[2]) # RED
shutter_speed = int(sys.argv[3])

GPIO.setmode(GPIO.BOARD)
GPIO.setup(FOCUS, GPIO.OUT)
GPIO.setup(SHUTTER, GPIO.OUT)
GPIO.setup(GROUND, GPIO.OUT)

GPIO.output(GROUND,True)
GPIO.output(FOCUS,True)
GPIO.output(SHUTTER,True)
time.sleep(shutter_speed / 1000)
GPIO.output(SHUTTER,False)
GPIO.output(FOCUS,False)
GPIO.output(GROUND,False)

GPIO.cleanup()