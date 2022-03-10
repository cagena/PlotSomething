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
import math

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
        #self.data = np.zeros((500,2))
        #self.operation = np.zeros(500)
        #self.data1 = [0]*500
        #self.data2 = [0]*500
        self.operation = [0]*500
        self.x = 0
        self.y = 0
        
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
        op_count = 0
        with open(filename) as f:
            ## A variable that reads lines of code from the Nucleo.
            raw_data = f.readlines()
            data = ''.join(raw_data)
            ## A variable that separates strings into ordered lists of data.
            #for x in data:
            data = data.split(';')
            for x in data:
                try:
                    float(x)
                except:
                    if 'PU' in x:
                        self.operation[op_count] = 'PU'
                        op_count += 1
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
                                    op_count += 1
                                    cu = 0
                                    st = ''
                            else:
                                st += y
                        self.operation[op_count] = st
                        op_count += 1
                        st = ''
                        cu = 0
                    elif 'PD' in x:
                        self.operation[op_count] = 'PD'
                        op_count += 1
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
                                    op_count += 1
                            else:
                                st += y
                        self.operation[op_count] = st
                        st = ''
                        cd = 0
                        op_count += 1
                    else:
                        self.operation[op_count] = x
                        op_count += 1         
        return self.operation
    
    def process(self,i):
        #for i in range(len(self.operation)):
        st = ''
        var = str(self.operation[i])
        if ',' in var:
            for y in var:
                try:
                    float(y)
                except:
                    if y == ',':
                        #self.data1[i] = st
                        self.x = st
                        st = ''
                else:
                    st += y
            #self.data2[i] = st
            self.y = st
            st = ''
        else:
            for y in str(self.operation[i]):
                st += y
            #self.data1[i] = st
            #self.data2[i] = st
            self.x = st
            st = ''
        return [self.x, self.y]
            
    def run(self,i):
        #for i in range(len(self.operation)):
            try:
                #float(self.data1[i])
                float(self.x)
            except:
                #self.data1[i] = self.data1[i]
                #self.data2[i] = self.data2[i]
                return [self.x,0]
            else:
                #x_scaled = (int(self.data1[i])/1016) - 3 - 2.5
                #y_scaled = (int(self.data2[i])/1016) + 5.59
                x_scaled = (int(self.x)/1016) - 3
                y_scaled = (int(self.y)/1016)
                r = math.sqrt(x_scaled**2 + y_scaled**2)
                duty1 = (r*16384)/0.04167
                duty2 = (16384*r*math.acos(x_scaled/r))/(2*3.14)
                self.x = duty1
                self.y = duty2
                return [self.x,self.y]
    
#     def report_x(self,i):
#         return self.data1[i]
#     
#     def report_y(self,i):
#         return self.data2[i]
    def report_x(self):
        return self.x
    
    def report_y(self):
        return self.y
    
    def length(self):
        return len(self.operation)

# if __name__ == "__main__":
    # hpgl = hpglDriver()
    # operation = hpgl.read('lines.hpgl')
    # for i in range(len(operation)):
    #     hpgl.process(i)
    #     uh = hpgl.run(i)
    #     print(uh[0])