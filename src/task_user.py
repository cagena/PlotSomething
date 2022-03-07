""" @file        task_user.py
    @brief       User interface task for the encoders, motors, and controllers.
    @details     Implements a finite state machine to recieve inputs from
                 the keyboard and execute the corresponding task.
    @author      Corey Agena
    @author      Luisa Chiu
    @date        3-7-22
"""

from pyb import USB_VCP
from nb_input import NB_Input
from micropython import const

## State 0 of the user interface task
S0_CALIB            = const(0)
## State 1 of the user interface task
S1_HELP             = const(1)
## State 2 of the user interface task
S2_WAIT_FOR_CHAR    = const(2)

nb_in = NB_Input (USB_VCP(), echo=True)

def input_task():
        """!  Task which runs the non-blocking input object quickly to ensure
        that keypresses are handled not long after they've occurred. """
        while True:
            nb_in.check ()
            yield 0

def task_user(state = S0_CALIB):
     while True:
        if state == S0_CALIB:
            
            state = S1_HELP
            
        elif state == S1_HELP:
            print('\n\rWelcome, press:'
                  '\n\'p\' to plot from a HPGL file'
                  '\n\'d\' to set the both motors to a duty cycle of 0'
                  '\n\'m\' to prompt the user to enter a setpoint for'
                  ' lead screw'
                  '\n\'M\' to prompt the user to enter a setpoint for'
                  ' the wheel'
                  '\n\'q\' to quit'
                  '\n\'h\' return to the welcome screen')
            state = S2_WAIT_FOR_CHAR
            
        elif state == S2_WAIT_FOR_CHAR:
            if nb_in.any ():
                if nb_in.get() == 'q':
                    print('\r\nThe program was exited')
                elif nb_in.get() == 'h':
                    state = S1_HELP
                    print('\r\n')
                elif nb_in.get() == 'm':
                    print('\r\nLinear position set')
        yield 0
