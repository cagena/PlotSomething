"""!
@file main.py
This is the main file for Lab 3, it contains a program that runs two motor tasks which includes closed loop control
for each motor. The code was adapted from Dr. Ridgely's basic task example.
@author Corey Agena
@author Luisa Chiu
@date 2-9-2022
"""

import gc
import pyb
import cotask
import encoder_agena_chiu
import motor_agena_chiu
import controller_agena_chiu
import task_share
from pyb import USB_VCP
from nb_input import NB_Input
from micropython import const
import hpgl_agena_chiu
import math
import sys
from array import array
import utime

## State 0 of the user interface task
S0_CALIB            = const(0)
## State 1 of the user interface task
S1_HELP             = const(1)
## State 2 of the user interface task
S2_WAIT_FOR_CHAR    = const(2)
## State 3 of the user interface task
S3_READ             = const(3)
## State 4 of the user interface task
S4_PLOT             = const(4)

nb_in = NB_Input (USB_VCP(), echo=True)



# from pyb import USB_VCP
# from nb_input import NB_Input
# 
# nb_in = NB_Input (USB_VCP(), echo=True)

# def input_task ():
#         """!  Task which runs the non-blocking input object quickly to ensure
#         that keypresses are handled not long after they've occurred. """
#         while True:
#             nb_in.check ()
#             yield 0
# 
# def user_task():
#      while True:
#         if nb_in.any ():
#             if nb_in.get() == 'q':
#                 print('\r\nThe program was exited')
#         yield 0
    

def task_motor1(duty_cycle = 0):
    ## The variable that calculates change in time.
    #difference = 0
    ## The variable that marks the start of the timer.
    #start = utime.ticks_ms()
    ## The variable that indicates if the current run is the initial run of the loop.
    #runs1 = 0
    while True:
        ## A variable that creates a timer which marks the current time.
        #current = utime.ticks_ms()
        #difference = (current - start)
        #controller_1.set_setpoint(lin_set.get())
        ## A variable that defines duty cycle for the controller's run function.
        enc1 = -encoder_drv1.read()
        duty_cycle = controller_1.run(enc1, 100)
        # print(duty_cycle)
        motor_drv1.set_duty_cycle(duty_cycle)
        flag1 = controller_1.flag()
        if flag1 == True:
            move_flag1.put(1)
            flag2 = False
            print('success')
        #print(enc1, lin_set.get())
        # if enc1 >= lin_set.get() - 100 and enc1 <= lin_set.get() + 100:
        #     move_flag1.put(1)
#         if difference <= 1500:
#             print_task.put('{:},{:}\r\n'.format(difference,encoder_drv1.read()))
#         else:
#             if runs1 == 0:
#                 print_task.put('Done\r\n')
#                 motor_drv1.disable()
#                 runs1 = 1
        yield()

def task_motor2(duty_cycle = 0):
    ## The variable that calculates change in time.
    # difference = 0
    ## The variable that marks the start of the timer.
    # start = utime.ticks_ms()
    while True:
        ## A variable that creates a timer which marks the current time.
        # current = utime.ticks_ms()
        # difference = (current - start)
        #controller_2.set_setpoint(ang_set.get())
        enc2 = -encoder_drv2.read()
        ## A variable that defines duty cycle for the controller's run function.
        duty_cycle = controller_2.run(enc2,75)
        motor_drv2.set_duty_cycle(-duty_cycle)
        flag2 = controller_2.flag()
        if flag2 == True:
            move_flag2.put(1)
            flag2 = False
            print('double success')
        # if enc2 >= ang_set.get() - 100 and enc2 <= ang_set.get() + 100:
        #     move_flag2.put(1)
        # if difference >= 1500:
        #     motor_drv2.disable()
        # The print portion is commented out for the second motor.
            # if difference <= 1500:
            # print_task.put('{:},{:}\r\n'.format(difference,encoder_drv2.read()))
        yield()
        
def input_task():
        """!  Task which runs the non-blocking input object quickly to ensure
        that keypresses are handled not long after they've occurred. """
        while True:
            nb_in.check ()
            yield ()

def task_user(state = S0_CALIB, calib_flag = 0):
    while True:
        if state == S0_CALIB:
            if calib_flag == 0:
                sol.low()
                print('\r\nReady to Calibrate? Press c and Enter')
                calib_flag = 1
            if nb_in.any ():
                char_in = nb_in.get()
                if char_in == 'c':
                    print('\r\nCalibrating')
                    pin = pyb.Pin(pyb.Pin.cpu.A0, pyb.Pin.IN)
                    adc = pyb.ADC(pin)
                    val = adc.read()
                    if val > 10:
                        motor_drv1.set_duty_cycle(-100)
                        while True:
                            val = adc.read()
                            if val <= 5:
                                encoder_drv1.zero()
                                encoder_drv2.zero()
                                motor_drv1.set_duty_cycle(0)
                                state = S1_HELP
                                break
                    else:
                        encoder_drv1.zero()
                        encoder_drv2.zero()
                        motor_drv1.set_duty_cycle(0)
                        state = S1_HELP
                        
        elif state == S1_HELP:
            print('\n\rWelcome, press:'
                  '\n\'p\' to plot from a HPGL file'
    #                   '\n\'d\' to set the both motors to a duty cycle of 0'
                   '\n\'l\' to prompt the user to enter a setpoint for'
                   ' lead screw'
    #                   '\n\'a\' to prompt the user to enter a setpoint for'
    #                   ' the wheel'
                  '\n\'q\' to quit'
                  '\n\'h\' return to the welcome screen')
            state = S2_WAIT_FOR_CHAR
            
        elif state == S2_WAIT_FOR_CHAR:
            if nb_in.any ():
                char_in = nb_in.get()
                if char_in == 'q':
                    motor_drv1.set_duty_cycle(0)
                    motor_drv2.set_duty_cycle(0)
                    print('\r\nThe program was exited')
                    sys.exit()
                elif char_in == 'h':
                    state = S1_HELP
                    print('\r\n')
                elif char_in == 'l':
                    print('\r\nLinear position adjustment')
                    if nb_in.any():
                        char_in = nb_in.get()
                        if char_in == '+':
                            print('\r\nPositve Linear Motion')
                            motor_drv1.set_duty_cycle(100)
                        elif char_in == '-':
                            print('\r\nNegative Linear Motion')
                            motor_drv1.set_duty_cycle(-100)
                        elif char_in == 's':
                            print('\r\nStopped Motion')
                            motor_drv1.set_duty_cycle(0)
                elif char_in == 'a':
                    print('\r\nAngular position set')
                elif char_in == 'm' or char_in == 'M':
                    print('\r\nPosition set')
                elif char_in == 'p' or char_in == 'P':
                    state = S3_READ
                    i = 0
        
        elif state == S3_READ:
            if i == 0:
                print('\r\nEnter hpgl file name:')
            elif nb_in.any ():
                filename = nb_in.get()
                print('\r\n',filename)
                if '.hpgl' in filename or '.HPGL' in filename:
                    hpgl.read(filename)
                    state = S4_PLOT
                    plot_count = 0
                    move_flag1.put(1)
                    move_flag2.put(1)
                    print('Plotting')
                else:
                    print('\r\ninvalid file name')
            i += 1
        
        elif state == S4_PLOT:
            mflag1 = move_flag1.get()
            mflag2 = move_flag2.get()
            if mflag1 == 1 and mflag2 == 1:
                print('in loop')
                move_flag1.put(0)
                move_flag2.put(0)
                hpgl.process(plot_count)
                output = hpgl.run(plot_count)
                x = output[0]
                try:
                    float(x)
                except:
                    if x == 'PU':
                        print('ho')
                        sol.low()
                        utime.sleep(1)
                        plot_count += 1
                        move_flag1.put(1)
                        move_flag2.put(1)
                    elif x == 'PD':
                        print('he')
                        sol.high()
                        utime.sleep(1)
                        plot_count += 1
                        move_flag1.put(1)
                        move_flag2.put(1)
                    elif x == 'IN' and plot_count > 0:
                        print('quit')
                        state = S1_HELP
                    else:
                        print('hi')
                        move_flag1.put(1)
                        move_flag2.put(1)
                        plot_count += 1
                else:
                    #print('{:},{:}'.format(x,y))
#                         x_scaled = (int(x)/1016) - 3 - 2.5
#                         y_scaled = (int(y)/1016) + 5.59
#                         r = math.sqrt(x_scaled**2 + y_scaled**2)
#                         duty1 = (r*16384)/0.04167
#                         duty2 = (16384*20.27*math.acos(x_scaled/r))/2
                    print('uh')
                    y = output[1]
                    #x_int = int(x)
                    #y_int = int(y)
                    # lin_set.put(x_int)
                    # ang_set.put(y_int)
                    controller_1.set_setpoint(x)
                    controller_2.set_setpoint(y)
                    plot_count += 1
        yield ()

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    ## A variable that creates a encoder driver for encoder 1.
    encoder_drv1 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    ## A variable that creates a encoder driver for encoder 2.
    encoder_drv2 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 8)
    ## A variable that creates a motor driver for motor 1.
    motor_drv1 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.A10, pyb.Pin.cpu.B4, pyb.Pin.cpu.B5, 3)
    ## A variable that creates a motor driver for motor 2.
    motor_drv2 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.C1, pyb.Pin.cpu.A0, pyb.Pin.cpu.A1, 5)
    ## A variable that creates a controller driver for motor 1.
    controller_1 = controller_agena_chiu.ControllerDriver(0, 0)
    ## A variable that creates a controller driver for motor 2.
    controller_2 = controller_agena_chiu.ControllerDriver(0, 0)
    # Enable both motors.
    motor_drv1.enable()
    motor_drv2.enable()
    
    hpgl = hpgl_agena_chiu.hpglDriver()

    lin_set = task_share.Share('L', name = 'Linear Setpoint')
    ang_set = task_share.Share('l', name = 'Angular Setpoint')
    
    move_flag1 = task_share.Share('B', name = 'Movement Flag 1')
    move_flag2 = task_share.Share('B', name = 'Movement Flag 2')
    
    sol = pyb.Pin(pyb.Pin.cpu.B3, pyb.Pin.OUT_PP)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

#     x = input('Input Kp to run step response, input s to stop: ')
#     try:
#         float(x)
#     except:
#         if x == 's':
#             motor_drv1.set_duty_cycle(0)
#             motor_drv2.set_duty_cycle(0)
#     else:
    ## A variable that requests for set point from the user.
#    y = input('Input set point: ')
    controller_1.set_gain(0.1)
    controller_1.set_setpoint(0)
    controller_2.set_gain(0.1)
    controller_2.set_setpoint(0)
    encoder_drv1.zero()
    encoder_drv2.zero()
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task_motor1, name = 'Task_Motor1', priority = 2, 
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (task_motor2, name = 'Task_Motor2', priority = 2, 
                         period = 10, profile = True, trace = False)
    in_task = cotask.Task (input_task, name = 'Input Task', priority = 1, 
                           period = 50, profile = True, trace = False)
    task_user = cotask.Task (task_user, name = 'User Task', priority = 2, 
                           period = 100, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (in_task)
    cotask.task_list.append (task_user)
    while True:
        # Run the scheduler with the chosen scheduling algorithm. 
        cotask.task_list.pri_sched ()
    
