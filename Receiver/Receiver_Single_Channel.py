import pigpio

pi = pigpio.pi()
GPIO_PIN = 23

pi.set_mode(GPIO_PIN, pigpio.INPUT)
pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_DOWN)

# initialize variables to store edge timestamps
start_time = None
end_time = None

def callback_function(GPIO_PIN, level, tick):
    global start_time, end_time
    if level == 1:  # rising edge
        start_time = tick
    elif level == 0:  # falling edge
        end_time = tick
        # calculate pulse duration in microseconds
        pulse_duration = pigpio.tickDiff(start_time, end_time)
        print("PWM pulse duration: {} us".format(pulse_duration))

pi.callback(GPIO_PIN, pigpio.EITHER_EDGE, callback_function)

while True:
    pass  # loop forever

