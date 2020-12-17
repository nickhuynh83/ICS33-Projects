# Hunter inherits from the Pulsator (1st) and the Mobile_Simulton (2nd) class:
#   updating/displaying like its Pulsator base, but also moving (either in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.


from prey import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2


class Hunter(Pulsator, Mobile_Simulton):
    
    distance_constant = 200
    
    def __init__(self,x,y):
        Pulsator.__init__(self,x,y)
        Mobile_Simulton.__init__(self,x,y,20,20,0,5)
        
    def update(self, model):
        eaten_set = Pulsator.update(self, model)
        prey_set = model.find(lambda x : isinstance(x, Prey))
        visible_set = {element for element in prey_set if self.distance(element.get_location()) < self.distance_constant}
        if len(visible_set) != 0: 
            shortest_dist = None   
            shortest_element = None    
            for element in visible_set:
                if shortest_dist == None or self.distance(element.get_location()) < shortest_dist:
                    shortest_dist = self.distance(element.get_location())
                    shortest_element = element
            dist_x = shortest_element.get_location()[0] - self.get_location()[0]
            dist_y = shortest_element.get_location()[1] - self.get_location()[1] 
            self.set_angle(atan2(dist_y,dist_x))
        Mobile_Simulton.move(self)
        return eaten_set
        