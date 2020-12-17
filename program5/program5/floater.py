# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage


#from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random


class Floater(Prey): 
    def __init__(self,x,y):
        Prey.__init__(self,x,y,10,10,0,5)
        Prey.randomize_angle(self)
        self.radius = 5
        
        
    def update(self, model):
        if random() > 0.3:
            self.move()
        else:
            fl_spd = 0
            while fl_spd < 3 or fl_spd > 7:
                fl_spd = self.get_speed()+(random()-0.5)
            self.set_speed(fl_spd)
            self.set_angle(self.get_angle()+(random()-0.5))
            self.move()
            
            
    def display(self, canvas):
        canvas.create_oval(self.get_location()[0]-self.radius, self.get_location()[1]-self.radius, self.get_location()[0]+self.radius, self.get_location()[1]+self.radius, fill='red')
