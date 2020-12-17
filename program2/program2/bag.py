# Submitter: nicholhh(Huynh, Nicholas)
from collections import defaultdict
from goody import type_as_str

class Bag:
    def __init__(self, *iter_obj):
        self.dict_items = defaultdict()
        for element in iter_obj:
            for each_element in element:
                count = 0
                for every_element in element:
                    if every_element == each_element:
                        count += 1
                if self.dict_items.get(count) == None:
                    self.dict_items[count] = set(each_element)
                else:
                    self.dict_items[count].add(each_element)


    def __repr__(self):
        str_items = ''
        for each_key in self.dict_items:
            for i in range(each_key):
                str_items += str(self.dict_items.get(each_key))
        return 'Bag({})'.format(list(str_items))
    
    
    def __str__(self):
        str_print = ''
        for each_key in self.dict_items:
            for element in self.dict_items.get(each_key):
                str_print += str(element) + str([each_key])
        return 'Bag({})'.format(str_print)
    
    
    def __len__(self):
        return sum([each_key*len(self.dict_items.get(each_key)) for each_key in self.dict_items])
    
    
    def unique(self):
        return sum([len(self.dict_items.get(each_key)) for each_key in self.dict_items])
    
    
    def __contains__(self, item):
        if len(self.dict_items) > 0:
            for each_key in self.dict_items:
                if item in self.dict_items.get(each_key):
                    return True
        return False
    
    
    def count(self, item):
        if len(self.dict_items) > 0:
            for each_key in self.dict_items:
                if item in self.dict_items.get(each_key):
                    return each_key
        return 0
    
    
    def add(self, item):
        num = Bag.count(self, item)
        if num > 0:
            self.dict_items[num].remove(item)
            if self.dict_items.get(num+1) != None:
                self.dict_items[num+1].add(item)
            else:
                self.dict_items[num+1] = set(item)
        else:
            if self.dict_items.get(1) != None:
                self.dict_items[1].add(item)
            else:
                self.dict_items[1] = set(item)
                
                
    def __add__(self, bag_obj):
        if type(bag_obj) == Bag:
            list_tuple_1 = self.dict_items.items()
            list_tuple_2 = bag_obj.dict_items.items()
            list_items = []
            for each_tuple in list_tuple_1:
                for element in each_tuple[1]:
                    for i in range(each_tuple[0]):
                        list_items.append(element)
            for each_tuple in list_tuple_2:
                for element in each_tuple[1]:
                    for i in range(each_tuple[0]):
                        list_items.append(element)
            return Bag(list_items)
        else:
            raise TypeError('Cannot add {} because it is not a Bag type object'.format(bag_obj))
    
    
    def remove(self, item):
        if Bag.__contains__(self, item) == True:
            dict_key = Bag.count(self, item)
            if dict_key == 1:
                self.dict_items[1].remove(item)
            else:
                self.dict_items[dict_key].remove(item)
                self.dict_items[dict_key-1].add(item)
        else:
            raise ValueError('There is no {} item in the Bag'.format(item))
        
    
    def __eq__(self, bag_obj):
        if type(bag_obj) == Bag:
            return self.dict_items == bag_obj.dict_items
        else:
            return False
        
        
    def __iter__(self):
        list_dict_items = []
        for each_key in self.dict_items:
            for element in self.dict_items.get(each_key):
                for i in range(each_key):
                    list_dict_items.append(element)
        def gen(list_dict_items):
            for i in range(len(list_dict_items)):
                yield list_dict_items[i]
        return gen(list(list_dict_items))
        

if __name__ == '__main__':
    
    #driver tests
    import driver
    driver.default_file_name = 'bsc21S20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
