from inputs import get_gamepad
import math
import threading
import time
import numpy as np
from matplotlib.gridspec import GridSpec

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode

        return [self.LeftJoystickX,
                self.LeftJoystickY,
                self.RightJoystickX,
                self.RightJoystickY,
                self.LeftTrigger,
                self.RightTrigger
                ]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state




if __name__ == '__main__':
    
    
    joy = XboxController()
    fig = plt.figure(figsize=(10, 5))
    gs = GridSpec(1, 4, width_ratios=[1, 6, 6, 1])
    fig.suptitle('Xbox Controller Data')

    ax1 = fig.add_subplot(gs[1], polar=True,)
    ax1.set_title('Joystick L')

    ax2 = fig.add_subplot(gs[2], polar=True)
    ax2.set_title('Joystick R')
    
    ax3 = fig.add_subplot(gs[0])
    ax3.set_title('Trigger L')
    
    ax4 = fig.add_subplot(gs[3])
    ax4.set_title('Trigger R')
    
    ax1.set_ylim(0, 1.25)
    ax2.set_ylim(0, 1.25)
    ax3.set_ylim(0, 1.25)
    ax4.set_ylim(0, 1.25)
    
    ax1.set_xticks(np.deg2rad([30, 150, 270]))  # Set 8 ticks evenly spaced around the circle
    
    ax2.set_xticks(np.deg2rad([30, 150, 270])) # Set 8 ticks evenly spaced around the circle
    
    ax1.set_aspect('equal', adjustable='box')
    ax2.set_aspect('equal', adjustable='box')
    
    point1,=ax1.plot(0,0,'bo',animated=False)
    point2,=ax2.plot(0,0,'ro',animated=False)
    
    bar1=ax3.bar(1,0,width=0.1,animated=False)
    bar2=ax4.bar(1,0,width=0.1,animated=False)
    
    plt.show(block=False)
    while True:
        vals=joy.read()
        #print(vals)
        
        L_radio=np.sqrt(vals[0]**2+vals[1]**2)
        L_angulo=np.arctan2(vals[1],vals[0])
        
        R_radio=np.sqrt(vals[2]**2+vals[3]**2)
        R_angulo=np.arctan2(vals[3],vals[2])
        
        if L_angulo<0:
            L_angulo+= 2 * np.pi
        if R_angulo<0:
            R_angulo+= 2 * np.pi

        L_trig=vals[4]
        R_trig=vals[5]
        def animate(frame):
            point1.set_data(L_angulo, L_radio)
            point2.set_data(R_angulo, R_radio)
            bar1[0].set_height(L_trig)
            bar2[0].set_height(R_trig)
            return point1, point2, bar1, bar2
        
        point1.set_data(L_angulo,L_radio)
        point2.set_data(R_angulo,R_radio)
        
        bar1[0].set_height(L_trig)
        bar2[0].set_height(R_trig)
        
        ax1.draw_artist(point1)
        ax2.draw_artist(point2)
        ax3.draw_artist(bar1[0])
        ax4.draw_artist(bar2[0])
        
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()
        

        
        