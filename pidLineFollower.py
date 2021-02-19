'''
Tufts University, Spring 2020-2021
lineFollower3.py
By: Sawyer Bailey Paccione and Olif Hordofa
Completed:   February 15th, 2021 10:30 PM

Description: Proportional Line Follower 
'''  

###############################################################################
#                                   Imports                                   #
###############################################################################
import hub 
import utime

###############################################################################
#                                  Initialize                                 #
###############################################################################
# Initialize Ports on Spike PRIME
left_motor      = hub.port.E.motor
right_motor     = hub.port.F.motor
color_sensor    = hub.port.B.device
sonar           = hub.port.C.device

# Initialize Light Sensor Readings from the line (WHITE) and the floor (BLACK)
BLACK = 9
WHITE = 79

# Initialize Proportional Controller Values
PROPORTIONAL_GAIN   = 0.9  # k_p

threshold   = (BLACK + WHITE) / 2
drive_speed = 35
goal = 10


left_motor.pwm(-20)
right_motor.pwm(20)

tick = 0

###############################################################################
#                                  Main Code                                  #
###############################################################################

while True:
    
    # Only check the sonar sensor every 5 times ~50 ms
    if tick >= 5 :
        tick = 0
        try: 
            dist = sonar.get()[0]
            diff = dist - goal
            if(diff <= 10) :
                # Slow down car proportionally
                drive_speed = int(3.5 * (diff))
            else :
                drive_speed = 35
            if (diff < 0) :
                # Begin reversing
                drive_speed = int(5 * diff)
        except:
            continue
    tick = tick + 1

    # Adjust speed by how far of the line the car is
    try:
        for_error = color_sensor.get()[0] - threshold
        turn_rate = PROPORTIONAL_GAIN * for_error
        left_motor.pwm(-int(drive_speed - turn_rate))
        right_motor.pwm(int(drive_speed + turn_rate))
    except:
        continue
        # None Type

    utime.sleep_ms(10)

# Stop Motor
left_motor.pwm(0)
right_motor.pwm(0)

left_motor.pwm(0)
right_motor.pwm(0)