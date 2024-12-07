import pigpio
import time

pi = pigpio.pi()
GPIO_PINS = [17,27,22,23,24,25]
 
a = [1500, 1500, 1100, 1500, 1500, 1500]

servo_pin = [13,16,19,20,21,26]

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

def pulse_dur():
    return  pulse_durations

def aa():
    while True:
        a1 = servo_spin(pulse_durations)
        print(a1)
    

def servo_spin(pwm_signals):
    global a
    pwm_values = list(pwm_signals.values())
    
    if ((max(pwm_values) >= 2500) or (min(pwm_values) < 500)):
        return a
        pass
        
    else:
        a = pwm_values
        #print(pwm_values)
        return pwm_values

while True:
    a = servo_spin(pulse_durations)
    pi.set_servo_pulsewidth(servo_pin[0], a[0])  
    pi.set_servo_pulsewidth(servo_pin[1], a[1]) 
    pi.set_servo_pulsewidth(servo_pin[2], a[2]) 
    pi.set_servo_pulsewidth(servo_pin[3], a[3]) 
    pi.set_servo_pulsewidth(servo_pin[4], a[4]) 
    pi.set_servo_pulsewidth(servo_pin[5], a[5]) 
    #print(pulse_dur())
    print(a)
    return a
    

