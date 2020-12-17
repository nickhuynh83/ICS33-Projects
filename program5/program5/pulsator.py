# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions


from blackhole import Black_Hole


class Pulsator(Black_Hole): 
    
    counter_constant = 30
    
    def __init__(self,x,y):
        Black_Hole.__init__(self,x,y)
        self.counter = 0
    
    def update(self, model):
        self.counter += 1
        eaten_set = Black_Hole.update(self, model)
        if len(eaten_set) != 0:
            self.counter = 0
            self.radius += 0.5 * len(eaten_set)
            self.change_dimension(len(eaten_set), len(eaten_set))
        if len(eaten_set) == 0 and self.counter == self.counter_constant:
            self.counter = 0
            self.radius -= 0.5
            self.change_dimension(-1, -1)
        return eaten_set
    