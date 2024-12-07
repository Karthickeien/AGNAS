import time
import pigpio
import RPi.GPIO as GPIO

print("auto hold")
GPIO.setmode(GPIO.BCM)

pi = pigpio.pi()

trig_pin = 3
echo_pin = 2

GPIO_PINS = [17,27,22,23,24,25]
servo_pin = [13,16,19,20,21,26]

pulse_durations = {pin: 0 for pin in GPIO_PINS}

kp = 1.0
ki = 0.1
hover_throttle = 1350
max_throttle = 1700
min_throttle = 1170

prev_error = 0
integrated_error = 0

target_altitude = 50 # height in cm

def callback_function(pin, level, tick, pulse_durations):
    if level == 1:  # rising edge
        pulse_durations[pin] = tick
    elif level == 0:  # falling edge
        pulse_duration = pigpio.tickDiff(pulse_durations[pin], tick)
        pulse_durations[pin] = pulse_duration


# set up callbacks for each GPIO pin
for pin in GPIO_PINS:
    pi.set_mode(pin, pigpio.INPUT)
    pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
    pi.callback(pin, pigpio.EITHER_EDGE, lambda p, l, t, pd=pulse_durations: callback_function(p, l, t, pd))


def height_measure(GPIO_TRIG, GPIO_ECHO):
    GPIO.setup(GPIO_TRIG, GPIO.OUT) 
    GPIO.setup(GPIO_ECHO, GPIO.IN) 
    GPIO.output(GPIO_TRIG, GPIO.LOW) 
    time.sleep(0.001) 
    GPIO.output(GPIO_TRIG, GPIO.HIGH) 
    time.sleep(0.00001) 
    GPIO.output(GPIO_TRIG, GPIO.LOW) 
    pulse_start = time.time() 
    pulse_end = time.time() 

    # Wait for ECHO pin to go high or timeout after 0.1 seconds
    timeout = time.time() + 0.1
    while GPIO.input(GPIO_ECHO)==0 and time.time() < timeout:
        pulse_start = time.time() 

    # Wait for ECHO pin to go low or timeout after 0.1 seconds
    timeout = time.time() + 0.1
    while GPIO.input(GPIO_ECHO)==1 and time.time() < timeout: 
        pulse_end = time.time() 

    pulse_duration = pulse_end - pulse_start 
    distance = round(pulse_duration * 17150, 2)
    if distance > 0:
        print(f"Distance: {distance} cm")
        return distance

def pwm_value(pwm_signals):
    global b
    values = list(pwm_signals.values())
    b = values
    return values

def servo_spin(pwm_signals):
    global a
    pwm_values = pwm_value(pwm_signals)
    
    if ((max(pwm_values) >= 2500) or (min(pwm_values) < 500)):
        return a
        pass
        
    else:
        a = pwm_values
        return pwm_values
def takeoff():
	
def landing(pwm_signals):
    pwm_values = list(pwm_signals.values())
    while pwm_values[2]>=min_throttle:
        pi.set_servo_pulsewidth(servo_pin[2], pwm_value[2]-100)
        time.sleep(0.1)
        

def alt_hold_switch():
    print('in alt hold switch')
    state1 = interrupt_checker()
    state2 = throttle_override()
    print(state2)
    
    if ((state1 and state2) == 1):
        if(a[5] >= 1500):
            print("Altitude hold")
            return 1

        else:
            print("Manual")
            return 0
    elif (state1 == 0):
        print("Signal lost, Altitude hold")
        return 2
    else:
        print("Manual")
        return 0
        
        
        
def throttle_override():
    print('throttle')
    while True:
        a1 = servo_spin(pulse_durations)
        a1 = a1[2]
        time.sleep(0.05)
        a2 = servo_spin(pulse_durations)
        a2 = a2[2]
        
        if(True == ((a1-5) <= a2 <= (a1+5))):
            print("Throttle constant")
            #print(a1, '\t', a2)
            return 1 # No throttle change
        else:
            print("Throttle override")
            #print(a1, '\t', a2)
            return 0 # Throttle override
            
            
def interrupt_checker():
    print('interupt checker')
    
    while True:
        a1 = pwm_value(pulse_durations)
        time.sleep(0.05)
        a2 = pwm_value(pulse_durations)
    
        if(a1==a2):
            #print("Off")
            return 0 # Receiver is off
        else:
            #print("On")
            return 1 # Receiver is on
            

interrupt_read=alt_hold_switch()

if interrupt_read==2:
	while True:
		distance = height_measure(trig_pin,echo_pin)
		error = distance - target_altitude  # target altitude of 50 cm
		proportional_term = kp * error
		integrated_error += error
		integral_term = ki * integrated_error
		output = hover_throttle + proportional_term + integral_term
		if output > max_throttle:
			output = max_throttle
			integrated_error = integrated_error- error
		elif output < min_throttle:
			output = min_throttle
			integrated_error -= error
			
		# send the throttle value to the flight controller
		print("Throttle:", output)
		time.sleep(0.1)
	else: 
		print("will land soon")
