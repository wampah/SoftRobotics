import Sofa.Core
from Sofa.constants import *
import math
import numpy as np

class MyController(Sofa.Core.Controller):

    def __init__(self, *a, **kw):

        Sofa.Core.Controller.__init__(self, *a, **kw)
        self.node = kw["node"]  
        self.force=self.node.particles.ForceField      
        return

    def onKeypressedEvent(self, e):        
        increments=1
        
        if e["key"] == Sofa.constants.Key.leftarrow:
            print("left arrow")            
            forceValue=np.copy(self.force.forces.value)
            forceValue[0][0]=forceValue[0][0]-increments
            self.force.forces.value=forceValue
            print(forceValue)

        if e["key"] == Sofa.constants.Key.rightarrow:
            print("right arrow")            
            forceValue=np.copy(self.force.forces.value)
            forceValue[0][0]=forceValue[0][0]+increments
            self.force.forces.value=forceValue
            print(forceValue)

            