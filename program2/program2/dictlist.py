# Submitter: nicholhh(Huynh, Nicholas)
from goody import type_as_str  # Useful for some exceptions

class DictList:
    def __init__(self, *dict_input):
        if len(dict_input) == 0:
            raise AssertionError('DictList.__init__: A dictionary argument is needed')
        else:    
            for element in dict_input:
                if type(element) != dict:
                    raise AssertionError('DictList.__init__: {} is not a dictionary'.format(element))
                elif element == dict():
                    raise AssertionError('DictList.__init__: {} is an empty dictionary'.format(element))
        for each_dict in dict_input:
            self.dl = list(dict_input)
            
            
    def __len__(self):
        set_keys = set()
        for element in self.dl:
            list_keys = element.keys()
            for each_key in list_keys:
                set_keys.add(each_key)
        return len(set_keys)
    
    
    def __bool__(self):
        return len(self.dl) > 1
    
    
    def __repr__(self):    
        return 'DictList({})'.format(','.join(str(element) for element in self.dl))   
    
    
    def __contains__(self, k):
        for element in self.dl:
            if k in element:
                return True
        return False
    
    
    def __getitem__(self, k):
        val = None
        for element in self.dl:
            if k in element:
                val = element.get(k)
        if val != None:
            return val
        else:
            raise KeyError('{} appears in no dictionaries'.format(k))
        
        
    def __setitem__(self, k, v):
        if DictList.__contains__(self, k) == True:
            for i in range(len(self.dl)):
                if k in self.dl[-(i+1)]:
                    self.dl[-(i+1)][k] = v
                    break
        else:
            self.dl.append({k : v})
            
            
    def __delitem__(self, k):
        if DictList.__contains__(self, k) == True:
            for i in range(len(self.dl)):
                if k in self.dl[-(i+1)]:
                    del self.dl[-(i+1)][k]
                    if len(self.dl[-(i+1)]) == 0:
                        del self.dl[-(i+1)]
                    break
        else:
            raise KeyError('The key {} does not exist in any of the dictionaries'.format(k))


    def __call__(self, k):
        final_list = []
        for i in range(len(self.dl)):
            if k in self.dl[i]:
                final_list.append((i, self.dl[i].get(k)))
        return final_list
    
    
    def __iter__(self):
        list_key = []
        for i in range(len(self.dl)):
            internal_list = []
            for each_key in self.dl[-(i+1)]:
                if each_key not in list_key:
                    internal_list.append(each_key)
            for element in sorted(internal_list):
                list_key.append(element)
        def gen(list_of_keys):
            for i in range(len(list_of_keys)):
                yield list_of_keys[i]
        return gen(list_key)
                    
    
    def items(self):
        list_key = []
        list_tuple = []
        for i in range(len(self.dl)):
            internal_list = []
            for each_key in self.dl[-(i+1)]:
                if each_key not in list_key:
                    internal_list.append(each_key)
            for element in sorted(internal_list):
                list_key.append(element)
                list_tuple.append((element, self.dl[-(i+1)].get(element)))
        def gen(list_of_tuples):
            for i in range(len(list_of_tuples)):
                yield list_of_tuples[i]
        return gen(list(list_tuple))
    
    
    def collapse(self):
        return {each_tuple[0]:each_tuple[1] for each_tuple in DictList.items(self)}
    
    
    def __eq__(self, comp_obj):
        if type(comp_obj) == DictList:
            return DictList.collapse(self) == DictList.collapse(comp_obj)
        elif type(comp_obj) == dict:
            return DictList.collapse(self) == comp_obj
        else:
            raise TypeError('Cannot compare {} object to DictList object'.format(type(comp_obj)))
    
    
    def __lt__(self, comp_obj): 
        if type(comp_obj) == DictList:
            if DictList.__len__(self) < DictList.__len__(comp_obj):
                for each_key in DictList.collapse(self):
                    if DictList.collapse(comp_obj).get(each_key) == None or DictList.collapse(self).get(each_key) != DictList.collapse(comp_obj).get(each_key):
                        return False
                return True
            return False  
        elif type(comp_obj) == dict:
            if DictList.__len__(self) < len(comp_obj):
                for each_key in DictList.collapse(self):
                    if comp_obj.get(each_key) == None or DictList.collapse(self).get(each_key) != comp_obj.get(each_key):
                        return False
                return True
            return False   
        else:
            raise TypeError('Cannot compare {} object to DictList object'.format(type(comp_obj)))
    
    
    def __gt__(self, comp_obj):
        if type(comp_obj) == DictList:
            if DictList.__len__(self) > DictList.__len__(comp_obj):
                for each_key in DictList.collapse(comp_obj):
                    if DictList.collapse(self).get(each_key) == None or DictList.collapse(comp_obj).get(each_key) != DictList.collapse(self).get(each_key):
                        return False
                return True
            return False  
        elif type(comp_obj) == dict:
            if DictList.__len__(self) > len(comp_obj):
                for each_key in comp_obj:
                    if DictList.collapse(self).get(each_key) == None or DictList.collapse(self).get(each_key) != comp_obj.get(each_key):
                        return False
                return True
            return False   
        else:
            raise TypeError('Cannot compare {} object to DictList object'.format(type(comp_obj)))
    
    
    def __add__(self, add_obj):
        if type(add_obj) == DictList:
            list_dict = []
            for each_dict in self.dl:
                list_dict.append(dict(each_dict))
            for element in add_obj.dl:
                list_dict.append(dict(element))
            return DictList(*list_dict)
        elif type(add_obj) == dict:
            list_dict = []
            for each_dict in self.dl:
                list_dict.append(dict(each_dict))
            list_dict.append(dict(add_obj))
            return DictList(*list_dict)
        else:
            raise TypeError('Cannot add {} object to DictList object'.format(type(add_obj)))
        
    
    def __radd__(self, add_obj):
        if type(add_obj) == dict:
            list_dict = []
            list_dict.append(dict(add_obj))
            for each_dict in self.dl:
                list_dict.append(dict(each_dict))
            return DictList(*list_dict)
        else:
            raise TypeError('Cannot add {} object to DictList object'.format(type(add_obj)))


    def __setattr__(self, name, value): 
        if name != 'dl':
            raise AssertionError('Cannot create new attributes for DictList objects')
        else:
            self.__dict__[name] = value    
           

if __name__ == '__main__':
    #Simple tests before running driver
    #Put your own test code here to test DictList before doing bsc tests
    
    d = DictList(dict(a=1,b=2), dict(b=12,c=13))
    print('len(d): ', len(d))
    print('bool(d):', bool(d))
    print('repr(d):', repr(d))
    print(', '.join("'"+x+"'" + ' in d = '+str(x in d) for x in 'abcx'))
    print("d['a']:", d['a'])
    print("d['b']:", d['b'])
    print("d('b'):", d('b'))
    print('iter results:', ', '.join(i for i in d))
    print('item iter results:', ', '.join(str(i) for i in d.items()))
    print('d.collapse():', d.collapse())
    print('d==d:', d==d)
    print('d+d:', d+d)
    print('(d+d).collapse():', (d+d).collapse())
    
    print()
    import driver
    driver.default_file_name = 'bsc22S20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
