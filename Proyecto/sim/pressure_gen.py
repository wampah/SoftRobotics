import Sofa.Core
from Sofa.constants import *
import math
import numpy as np
import pandas as pd 

class PressureGen(Sofa.Core.Controller):

    def __init__(self, *a, **kw):

        Sofa.Core.Controller.__init__(self, *a, **kw)
        self.node =kw["node"]          
        self.pressure=self.node.cavity.cavityPressure        
        self.index=0
        self.pressureValues=np.ones(100)*9000
        self.csvFile='test.csv'
        with open(self.csvFile, 'w', newline='') as f:
            df_header = pd.DataFrame({'1': ['Pressure'],'2':['tipX'],'3':['tipY'],'4':['tipZ']})
            df_header.to_csv(f, header=False, index=False)
        return

    def onAnimateEndEvent(self, edict):                        
        if self.index<len(self.pressureValues):
            #Increase pressure every step
            pressure=self.pressureValues[self.index]
            self.pressure.pressure.value=pressure
            self.index+=1            
            print('New Pressure {}'.format(self.pressure.pressure.value))
            tipPosition_mm=1000*np.mean(self.node.tipROI.position.value,axis=0)
            df=pd.DataFrame({'Pressure':[pressure],'x':tipPosition_mm[0],'y':tipPosition_mm[1],'z':tipPosition_mm[2]})
            with open(self.csvFile, 'a', newline='') as f:
                df.to_csv(f,header=False,index=False)                
            
                        