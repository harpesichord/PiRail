import wiringpi2
import sys

GROUND = int(sys.argv[0])  # WHITE
FOCUS = int(sys.argv[1])   # YELLOW
SHUTTER = int(sys.argv[2]) # RED
shutter_speed = int(sys.argv[3])

gpio = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_GPIO)  
gpio.pinMode(FOCUS,gpio.OUTPUT)
gpio.pinMode(SHUTTER,gpio.OUTPUT)
gpio.pinMode(GROUND,gpio.OUTPUT)

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(FOCUS, GPIO.OUT)
#GPIO.setup(SHUTTER, GPIO.OUT)
#GPIO.setup(GROUND, GPIO.OUT)

gpio.digitalWrite(GROUND, gpio.HIGH)
gpio.digitalWrite(FOCUS, gpio.HIGH)
gpio.digitalWrite(SHUTTER, gpio.HIGH)

time.sleep(shutter_speed / 1000)

gpio.digitalWrite(GROUND, gpio.LOW)
gpio.digitalWrite(FOCUS, gpio.LOW)
gpio.digitalWrite(SHUTTER, gpio.LOW)

#GPIO.output(GROUND,True)
#GPIO.output(FOCUS,True)
#GPIO.output(SHUTTER,True)
#time.sleep(shutter_speed / 1000)
#GPIO.output(SHUTTER,False)
#GPIO.output(FOCUS,False)
#GPIO.output(GROUND,False)

gpio.pinMode(FOCUS,0)
gpio.pinMode(SHUTTER,0)
gpio.pinMode(GROUND,0)