import pigpio
import time

pi = pigpio.pi()
GPIO_PINS = [18, 23] # Throttle and aux1 
 
a = [1100, 1200]

servo_pin = 8

# initialize dictionary to store pulse durations
pulse_durations = {pin: 0 for pin in GPIO_PINS}

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


def servo_spin(pwm_signals):
    global a
    pwm_values = list(pwm_signals.values())
    
    if ((max(pwm_values) >= 2500) or (min(pwm_values) < 500)):
        return a
        pass
        
    else:
        a = pwm_values
        return pwm_values
    

def interrupt_checker():
    
    while True:
        a1 = servo_spin(pulse_durations)
        time.sleep(0.07)
        a2 = servo_spin(pulse_durations)
    
        if(a1==a2):
            print("OFF")
            return 0 # Receiver is off
        else:
            print("On")
            return 1 # Receiver is on

def throttle_override():
    while True:
        a1 = servo_spin(pulse_durations)
        a1 = a1[0]
        time.sleep(0.07)
        a2 = servo_spin(pulse_durations)
        a2 = a2[0]
        
        if(True == ((a1-10) <= a2 <= (a1+10))):
            print("Throttle constant")
            #print(a1, '\t', a2)
            return 1 # No throttle change
        else:
            print("Throttle override")
            #print(a1, '\t', a2)
            return 0 # Throttle override
            

def alt_hold_switch():
    state1 = interrupt_checker()
    state2 = throttle_override()
    
    if ((state1 and state2) == 1):
        if(a[1] >= 1500):
            print("Altitude hold")
            return 1

        else:
            print("Manual")
            return 0
    else:
        print("Manual")
        return 0
        # Add a condition in future if remote turns off, do landing or proceed to the code or something.
    
    
while True:
    #throttle_override()
    #print()
    interrupt_checker()
    #alt_hold_switch()
    

