'''!
@file controller_agena_chiu.py
This is the file that serves as a module to be imported in main. It creates a class for the controller
driver to run functions.
@author Corey Agena
@author Luisa Chiu
@date 1-27-2022
'''

from ulab import numpy as np
from array import array

class hpglDriver:  
    '''! 
    This class implements a controller driver for a motor and flywheel rig. 
    '''
    def __init__(self):
        '''! 
        Creates a controller driver by initializing the gain
        and initial setpoint used in closed-loop control.
        @param K_p The initial proportional gain for the controller.
        @param i_set The initial setpoint for the controller.
        '''
        self.data = np.zeros((500,2))
        self.operation = np.array(0,500, dtype = object)
        #self.operation = []
        
    def read(self,filename):
        '''!
        Called repeatedly to run the control algorithm.
        @param pos Current position of the encoder.
        @return duty Duty cycle to set the motor.
        '''
        raw_st = ''
        st = ''
        cu = 0
        cd = 0
        with open(filename) as f:
            ## A variable that reads lines of code from the Nucleo.
            raw_data = f.readlines()
            data = ''.join(raw_data)
            ## A variable that separates strings into ordered lists of data.
            #for x in data:
            data = data.split(';')
            op_count = 0
            for x in data:
                try:
                    float(x)
                except:
                    if 'PU' in x:
                        self.operation[op_count] = 'PU'
                        raw_st = x
                        for y in raw_st:
                            try:
                                float(y)
                            except:
                                if y == ',' and cu == 0:
                                    st += ','
                                    cu = 1
                                elif y == ',' and cu == 1:
                                    self.operation[op_count] = st
                                    cu = 0
                                    st = ''
                            else:
                                st += y
                        self.operation[op_count] = st
                        st = ''
                        cu = 0
                    elif 'PD' in x:
                        self.operation[op_count] = 'PD'
                        raw_st = x
                        for y in raw_st:
                            try:
                                float(y)
                            except:
                                if y == ',' and cd == 0:
                                    st += ','
                                    cd = 1
                                elif y == ',' and cd == 1:
                                    self.operation[op_count] = st
                                    cd = 0
                                    st = ''
                            else:
                                st += y
                        self.operation[op_count] = st
                        st = ''
                        cd = 0
                    else:
                        self.operation[op_count] = raw_st
    
    def process(self):
        for i in range(len(self.operation)):
            st = ''
            if ',' in self.operation[i]:
                for y in self.operation[i]:
                    try:
                        float(y)
                    except:
                        if y == ',':
                            self.data[i,0] = st
                            st = ''
                    else:
                        st += y
                self.data[i,1] = st
                st = ''
            else:
                for y in self.operation[i]:
                    st += y
                self.data[i,0] = st
                self.data[i,1] = st
                st = ''
            
    def run(self):
        for i in range(len(self.operation)):
            try:
                float(self.data[i,0])
            except:
                self.data[i,0] = self.data[i,0]
                self.data[i,1] = self.data[i,1]
            else:
                x_scaled = (self.data[i,0]/1016) - 3 - 2.5
                y_scaled = (self.data[i,1]/1016) + 5.59
                r = math.sqrt(x_scaled^2 + y_scaled^2)
                duty1 = (r*16384)/0.04167
                duty2 = (16384*20.27*math.acos(x_scaled/r))/2
                self.data[i,0] = duty1
                self.data[i,1] = duty2
    
    def report_x(self,i):
        return self.data[i,0]
    
    def report_y(self,i):
        return self.data[i,1]
    
    def length(self):
        return len(self.operation)
                