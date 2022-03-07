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

class Task_User:
    
    def __init__(self):
        self.state = S0_CALIB

    def input_task ():
            """!  Task which runs the non-blocking input object quickly to ensure
            that keypresses are handled not long after they've occurred. """
            while True:
                nb_in.check ()
                yield 0

    def task_user(self):
         while True:
            if self.state == S0_CALIB:
                self.tansition_to(S1_HELP)
                
            elif self.state == S1_HELP:
                print('Welcome, press:'
                      '\n\'b\' to start balancing the plate'
                      '\n\'d\' to set the both motors to a duty cycle of 0'
                      '\n\'m\' to prompt the user to enter a setpoint for'
                      ' lead screw'
                      '\n\'M\' to prompt the user to enter a setpoint for'
                      ' the wheel'
                      '\n\'s\' to end data collection prematurely'
                      '\n\'h\' return to the welcome screen')
                self.transition_to(S2_WAIT_FOR_CHAR)
                
            elif self.state == S2_WAIT_FOR_CHAR:
                if nb_in.any ():
                    if nb_in.get() == 'q':
                        print('\r\nThe program was exited')
                    elif nb_in.get() == 'h':
                        self.transition_to(S1_HELP)
            yield 0
            
    def transition_to(self, new_state):
        ''' @brief      Transitions the FSM to a new state.
            @details    Optionally a debugging message can be printed
                        if the dbg flag is set when the task object is created.
            @param      new_state The state to transition to.
        '''
        if (self.dbg):
            print('{:}: S{:}->S{:}'.format(self.name,self.state,new_state))
        self.state = new_state
    
