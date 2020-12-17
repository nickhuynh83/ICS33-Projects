import controller
import model   # Use to pass a reference to this module when calling update in update_all

#Use the reference to this module to pass it to update methods

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special   import Special


# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
running = False
cycle_count = 0
simul_obj = None
set_simul = set()



#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running, cycle_count, set_simul
    running = False
    cycle_count = 0
    set_simul = set()


#start running the simulation
def start ():
    global running
    running = True


#stop running the simulation (freezing it)
def stop ():
    global running
    running = False


#tep just one update in the simulation
def step ():
    global running, cycle_count
    if running == False:
        running = True
    cycle_count += 1
    for element in set_simul:
        element.update(model)
    running = False


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global simul_obj
    simul_obj = kind


#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    global set_simul
    remove_set = set()
    if simul_obj == 'Remove':
        remove_set = {element for element in set_simul if element.contains((x,y))}
        for element in remove_set:
            remove(element)
    else:
        add(eval('{type_simul}({x_val},{y_val})'.format(type_simul=simul_obj, x_val=x, y_val=y)))


#add simulton s to the simulation
def add(s):
    global set_simul
    set_simul.add(s)

# remove simulton s from the simulation    
def remove(s):
    global set_simul
    set_simul.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    pred_set = set()
    for element in set_simul:
        if p(element):
            pred_set.add(element)
    return pred_set


#call update for every simulton (passing model to each) in the simulation
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    global cycle_count, set_simul
    if running:
        cycle_count += 1
        remove_set = set()
        copy_set_simul = set(set_simul)
        for element in copy_set_simul:
            eaten_set = element.update(model)
            if eaten_set != None:   
                for each_obj in eaten_set:
                    remove_set.add(each_obj)
            if element.get_dimension() == (0,0):
                remove_set.add(element)
        if remove_set != None:
            for element in remove_set:
                remove(element)

#For animation: (1) delete every simulton from the canvas; (2) call display on
#  each simulton being simulated to add it back to the canvas, possibly in a
#  new location; also, update the progress label defined in the controller
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
        
    for element in set_simul:
        element.display(controller.the_canvas)
        
    controller.the_progress.config(text=str(len(set_simul))+" simultons/"+str(cycle_count)+" cycles")
