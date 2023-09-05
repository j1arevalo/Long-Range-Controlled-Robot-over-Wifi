# Libraries
import RPi.GPIO as GPIO
import time
from evdev import InputDevice, categorize
from adafruit_servokit import ServoKit 
 # Check if the gamepad is connected
# You need to adjust the event number if the wrong input device is read
gamepad = InputDevice('/dev/input/event0')
print(gamepad)

print("Press CTRL+C to end the program.")
# GPIO Mode (BOARD / BCM)
#GPIO.setmode(GPIO.BOARD)
kit = ServoKit(channels=16)
channel_servo1 = 0
channel_motor1 = 2
channel_servo12 = 12
channel_motor12 = 2
# set GPIO Pins
GPIO_Ain1 = 17 #11
GPIO_Ain2 = 27 #13
GPIO_Apwm = 22 #15
GPIO_Bin1 = 5   #29
GPIO_Bin2 = 6	#31
GPIO_Bpwm = 13	#33
ServoPin = 4		#7
# Set GPIO direction (IN / OUT)
GPIO.setup(ServoPin, GPIO.OUT)
GPIO.setup(GPIO_Ain1, GPIO.OUT)
GPIO.setup(GPIO_Ain2, GPIO.OUT)
GPIO.setup(GPIO_Apwm, GPIO.OUT)
GPIO.setup(GPIO_Bin1, GPIO.OUT)
GPIO.setup(GPIO_Bin2, GPIO.OUT)
GPIO.setup(GPIO_Bpwm, GPIO.OUT)

# Both motors are stopped 
GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)

# Set PWM parameters
pwm_frequency = 50
pwm_frequency = 50
duty_min = 2.5 * float(pwm_frequency) / 50.0
duty_max = 12.5 * float(pwm_frequency) / 50.0
kit.servo[channel_servo1].set_pulse_width_range(400,2300)
kit.continuous_servo[channel_motor1].set_pulse_width_range(1200,1800)
# Create the PWM instances
def set_duty_cycle(angle):
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)
pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)
# Set the duty cycle (between 0 and 100)
# The duty cycle determines the speed of the wheels
pwmA.start(100)
pwmB.start(100)
pwm_servo = GPIO.PWM(ServoPin, pwm_frequency)
print("Press CTRL+C to end the program.")
# Keep track of the state
FSM1State = 0
FSM1NextState = 0

# Keep track of the timing
FSM1LastTime = 0
duration = 2

delayTarget = 1
LastTime = 0
old_button = 1
Motor_Position = 1

angle = 0

# Main program
try:
        
        
        noError = True
        while noError:
    
            newbutton = False
            newstick  = False
            try:
                for event in gamepad.read():            # Use this option (and comment out the next line) to react to the latest event only
                    #event = gamepad.read_one()         # Use this option (and comment out the previous line) when you don't want to miss any event
                    eventinfo = categorize(event)
                    if event.type == 1:
                        newbutton = True
                        codebutton  = eventinfo.scancode
                        valuebutton = eventinfo.keystate
                    elif event.type == 3:
                        newstick = True
                        codestick  = eventinfo.event.code
                        valuestick = eventinfo.event.value
            except:
                pass


            # If there was a gamepad event, show it
            if newbutton:
                print("Button: ",codebutton,valuebutton)
            if newstick and codestick == 1 and valuestick == 0:
                print("Stick : ",codestick,valuestick)
        # Check the current time
                currentTime = time.time()

        # Update the state
                FSM1State = FSM1NextState
                
     
                GPIO.output(GPIO_Ain1, True)
                GPIO.output(GPIO_Ain2, False)
                GPIO.output(GPIO_Bin1, True)
                GPIO.output(GPIO_Bin2, False)
                pwmA.ChangeDutyCycle(100)                # duty cycle between 0 and 100
                pwmB.ChangeDutyCycle(100)                # duty cycle between 0 and 100
                print ("Forward half speed")
                time.sleep(0.1)

                GPIO.output(GPIO_Ain1, True)
                GPIO.output(GPIO_Ain2, False)
                GPIO.output(GPIO_Bin1, True)
                GPIO.output(GPIO_Bin2, False)
                pwmA.ChangeDutyCycle(100)               # duty cycle between 0 and 100
                pwmB.ChangeDutyCycle(100)               # duty cycle between 0 and 100
                print ("Forward full speed")
                time.sleep(0.1)
            if newstick and codestick == 1 and valuestick == 255:
                GPIO.output(GPIO_Ain1, False)
                GPIO.output(GPIO_Ain2, True)
                GPIO.output(GPIO_Bin1, False)
                GPIO.output(GPIO_Bin2, True)
                pwmA.ChangeDutyCycle(100)                # duty cycle between 0 and 100
                pwmB.ChangeDutyCycle(100)                # duty cycle between 0 and 100
                print ("Backward third speed")
                time.sleep(0.1)
            if newstick and codestick == 1 and valuestick == 128: 
                GPIO.output(GPIO_Ain1, False)
                GPIO.output(GPIO_Ain2, False)
                GPIO.output(GPIO_Bin1, False)
                GPIO.output(GPIO_Bin2, False)
                print ("Stop")
                time.sleep(0.1)
        # Clean up GPIO if there was an error
        #GPIO.cleanup()
            
            if newbutton and codebutton == 304 and valuebutton == 1:        
                    channel = channel_servo1
                    kit.servo[0].angle = angle
                    angle = 180
                    kit.servo[channel].angle = angle
                    print ('angle: {0} \t channel: {1}'.format(angle,channel))
                    kit.servo[0].angle = angle
                    channel = channel_motor1
                    speed = 1
                    kit.continuous_servo[channel].throttle = speed
                    print ('speed: {0} \t channel: {1}'.format(speed,channel))
                    kit.servo[0].angle = angle
                    FSM1NextState = 1
                    kit.servo[0].angle = angle
            elif newbutton and codebutton == 307 and valuebutton == 1 :
                    FSM1NextState = 0
                    angle = 0
                    kit.servo[0].angle = angle
                    

            if newbutton and codebutton == 305 and valuebutton == 1:        
                    channel = channel_servo12
                    angle = 0
                    kit.servo[channel].angle = angle
                    kit.servo[12].angle = angle
                    print ('angle: {0} \t channel: {1}'.format(angle,channel))
                    channel = channel_motor12
                    speed = 1
                    kit.continuous_servo[channel].throttle = speed
                    print ('speed: {0} \t channel: {1}'.format(speed,channel))
                    FSM1NextState = 2
                    kit.servo[12].angle = angle
            elif newbutton and codebutton == 306 and valuebutton == 1 :
                    FSM1NextState = 3
                    angle = 180
                    kit.servo[12].angle = angle
            
            if newbutton and codebutton == 312 and valuebutton == 1:
                raise KeyboardInterrupt        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()

