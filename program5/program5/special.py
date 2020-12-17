# This special object will have a width and height of 16 and a radius of 8 pixels.
# The purpose of this object is to create balls every 15 cycles in the simulation.
# After it spits out a ball, the object's radius gets smaller by one. 
# After 8 balls are spit out, the special object will be removed.

from prey import Prey
from ball import Ball
from mobilesimulton import Mobile_Simulton

class Special(Mobile_Simulton):
    
    counter_constant = 15
    
    def __init__(self,x,y):
        Prey.__init__(self,x,y,16,16,0,6)
        self.radius = 8
        self.counter = 0
        self._x = x
        self._y = y
        
    def update(self, model):
        self.counter += 1
        if self.counter == self.counter_constant:
            model.add(Ball(self._x, self._y))
            self.counter = 0
            self.radius -= 1
            self.change_dimension(-2,-2)
    
    def display(self, canvas):
        canvas.create_oval(self.get_location()[0]-self.radius, self.get_location()[1]-self.radius, self.get_location()[0]+self.radius, self.get_location()[1]+self.radius, fill='cyan')