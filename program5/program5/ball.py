# A Ball is Prey; it updates by moving in a straight
#   line and displays as blue circle with a radius
#   of 5 (width/height 10).


from prey import Prey


class Ball(Prey): 
    def __init__(self,x,y):
        Prey.__init__(self,x,y,10,10,0,5) #what does height/width do
        Prey.randomize_angle(self)
        self.radius = 5
        
        
    def update(self, model):
        self.move()
        
        
    def display(self, canvas):
        canvas.create_oval(self.get_location()[0]-self.radius, self.get_location()[1]-self.radius, self.get_location()[0]+self.radius, self.get_location()[1]+self.radius, fill='blue')
