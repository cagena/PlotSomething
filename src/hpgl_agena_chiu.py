'''!
@file controller_agena_chiu.py
This is the file that serves as a module to be imported in main. It creates a class for the controller
driver to run functions.
@author Corey Agena
@author Luisa Chiu
@date 1-27-2022
'''
    
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
        self.operation = []
        self.x = []
        
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
            for x in data:
                try:
                    float(x)
                except:
                    if 'PU' in x:
                        self.operation.append('PU')
                        raw_st = x
                        for y in raw_st:
                            try:
                                float(y)
                            except:
                                if y == ',' and cu == 0:
                                    st += ','
                                    cu = 1
                                elif y == ',' and cu == 1:
                                    self.operation.append(st)
                                    cu = 0
                                    st = ''
                            else:
                                st += y
                        self.operation.append(st)
                        st = ''
                        cu = 0
                    elif 'PD' in x:
                        self.operation.append('PD')
                        raw_st = x
                        for y in raw_st:
                            try:
                                float(y)
                            except:
                                if y == ',' and cd == 0:
                                    st += ','
                                    cd = 1
                                elif y == ',' and cd == 1:
                                    self.operation.append(st)
                                    cd = 0
                                    st = ''
                            else:
                                st += y
                        self.operation.append(st)
                        st = ''
                        cd = 0
                    else:
                        self.operation.append(x)
                        
    def run(self, i):
        self.x = []
        st = ''
        if ',' in self.operation[i]:
            for y in self.operation[i]:
                try:
                    float(y)
                except:
                    if y == ',':
                        self.x[0] = st
                        st = ''
                else:
                    st += y
                self.x[1] = st
                st = ''
    
    def report_x(self):
        return self.x[0]
    
    def report_y(self):
        return self.x[1]
    
    def length(self):
        return len(self.operation)
                