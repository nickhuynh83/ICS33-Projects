# Black_Hole inherits from only Simulton, updating by finding/removing
#   any Prey-derived class whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    def __init__(self,x,y):
        Simulton.__init__(self,x,y,20,20)
        self.radius = 10
        
    def contains(self, xy):
        return self.distance(xy) < self.radius
    
    def update(self, model):
        eaten_set = set()
        set_prey = model.find(lambda obj : isinstance(obj, Prey))
        for element in set_prey:
            if self.contains(element.get_location()):
                eaten_set.add(element)
        return eaten_set
    
    def display(self, canvas):
        canvas.create_oval(self.get_location()[0]-self.radius, self.get_location()[1]-self.radius, self.get_location()[0]+self.radius, self.get_location()[1]+self.radius, fill='black')
            
