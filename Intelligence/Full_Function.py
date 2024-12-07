import time
import pigpio
import RPi.GPIO as GPIO
from receiver_5 import final


pi = pigpio.pi()

GPIO.setmode(GPIO.BCM)

trig_pin = 3
echo_pin = 2

GPIO_PINS = [17, 27, 22, 23, 24, 25]
servo_pin = [13, 16, 19, 20, 21, 26]

pulse_durations = {pin: 0 for pin in GPIO_PINS}


hover_throttle = 1350
max_throttle = 1700
min_throttle = 1170
kp = 0.1  # Proportional gain
ki = 0.01  # Integral gain
integrated_error = 0

target_altitude = 50



def takeoff(pwm_values):
    while pwm_values[2] <= 1400:
        pi.set_servo_pulsewidth(servo_pin[2], pwm_value[2] - 100)
        time.sleep(0.1)


def pwm_value(pwm_signals):
    values = list(pwm_signals.values())
    return values


def interrupt_checker():
    while True:
        a1 = pwm_value(pulse_durations)
        time.sleep(0.05)
        a2 = pwm_value(pulse_durations)
        if a1 == a2:
            return 0
        else:
            return 1


def throttle_override():
    while True:
        a1 = servo_spin(pulse_durations)
        a1 = a1[2]
        time.sleep(0.05)
        a2 = servo_spin(pulse_durations)
        a2 = a2[2]

        if True == ((a1 - 5) <= a2 <= (a1 + 5)):
            print("Throttle constant")
            # print(a1, '\t', a2)
            return 1  # No throttle change
        else:
            print("Throttle override")
            # print(a1, '\t', a2)
            return 0  # Throttle override


def height_measure():
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.output(trig_pin, GPIO.LOW)
    time.sleep(0.001)
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)
    pulse_start = time.time()
    pulse_end = time.time()

    # Wait for ECHO pin to go high or timeout after 0.1 seconds
    timeout = time.time() + 0.1
    while GPIO.input(echo_pin) == 0 and time.time() < timeout:
        pulse_start = time.time()

    # Wait for ECHO pin to go low or timeout after 0.1 seconds
    timeout = time.time() + 0.1
    while GPIO.input(echo_pin) == 1 and time.time() < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = round(pulse_duration * 17150, 2)
    if distance > 0:
        print(f"Distance: {distance} cm")


def landing(pwm_values):
    while pwm_values[2] >= min_throttle:
        pi.set_servo_pulsewidth(servo_pin[2], pwm_value[2] - 100)
        time.sleep(0.1)


def alt_hold_switch():
    print('in alt hold switch')
    state1 = interrupt_checker()
    state2 = throttle_override()
    print(state2)

    if (state1 == 1) and (state2 == 1):
        if a[5] >= 1500:
            print("Altitude hold")
            return 1
        else:
            print("Manual")
            return 0
    elif state1 == 0:
        print("Signal lost, Altitude hold")
        return 2
    else:
        print("Manual")
        return 0


def servo_spin(pwm_signals):
    #global a
    pwm_values = pwm_value(pwm_signals)
    print(pwm_values)

    if ((max(pwm_values) >= 2500) or (min(pwm_values) < 500)):
        #return a
        pass

    else:
        a = pwm_values
        return pwm_values


if __name__ == "__main__":
    thr=alt_hold_switch()
    while thr==1:
        pv=final(pulse_durations)
        print(pv)
        while True:
            distance = height_measure(trig_pin, echo_pin)
            error = distance - target_altitude  # target altitude of 50 cm
            if error < 1:
                break
            proportional_term = kp * error
            integrated_error += error
            integral_term = ki * integrated_error
            output = hover_throttle + proportional_term + integral_term

            if output > max_throttle:
                output = max_throttle
                integrated_error -= error

            elif output < min_throttle:
                output = min_throttle
                integrated_error -= error

            # send the throttle value to the flight controller
            print("Throttle:", output)
            time.sleep(0.1)
        state = alt_hold_switch()
        if state == 2:
            fpv = pwm_value(pulse_durations)
            landing(fpv)
            break
