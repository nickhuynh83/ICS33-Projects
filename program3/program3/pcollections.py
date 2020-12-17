# Submitter: nicholhh(Huynh, Nicholas)
import re, traceback, keyword

class Point:
    _fields = ['x', 'y']
    _mutable = False
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return 'Point(x={x},y={y})'.format(x=self.x,y=self.y)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def __getitem__(self, index):
        if type(index) == int and index < len(self._fields):
            return eval('self.get_{}'.format(self._fields[index]))
        elif type(index) == str:
            return eval('self.get_' + index)
        else:
            raise IndexError('The index is out of range')
        
    def __eq__(self, comp_obj):
        return self.x == comp_obj.x and self.y == comp_obj.y
    
    def _asdict(self):
        final_dict = {}
        for element in self._fields:
            final_dict[element] = eval('self.get_{}()'.format(element))
        return final_dict
        
    def _make(iterable):
        return Point(*iterable)
    
    def _replace(self, **kargs):
        for each_key in kargs.keys():
            if each_key not in self._asdict().keys():
                raise TypeError('The key is not a field name')
        if self._mutable == True:
            for each_key in kargs.keys():
                self.__dict__[each_key] = kargs.get(each_key)
            return None
        else:
            old_dict = self._asdict()
            for each_key in kargs.keys():
                old_dict[each_key] = kargs.get(each_key)
            return Point(*old_dict.values())
        
    def __setattr__(self, name, value):
        if self._mutable == False:
            if name in self._fields and str(name) not in self.__dict__:
                self.__dict__[name] = value
            else:
                raise AttributeError('The object is not mutable')
        else:
            self.__dict__[name] = value
            


def pnamedtuple(type_name, field_names, mutable= False, defaults= {}):
    def show_listing(s):
        for line_number, line_text in enumerate(s.split('\n'),1):  
            print(f' {line_number: >3} {line_text.rstrip()}')

    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    def legal_name(name: str) -> str:
        if re.match(r'([a-z]|[A-Z])([a-z]|[0-9]|[_])*', str(name)) != None and name not in keyword.kwlist:
            return name
        else:
            raise SyntaxError('{} is not a legal name'.format(name))
        
        
    def legal_field_name(field_names):
        if type(field_names) == list:
            for element in unique(field_names):
                legal_name(element)
            return field_names
        elif type(field_names) == str:
            final_list = []
            list_return = []
            if len(field_names.split(',')) > 1:
                list_element = field_names.split(',')
                for element in list_element:
                    final_list.append(element.lstrip())
                for e in unique(final_list):
                    list_return.append(legal_name(e))
                return list_return
            elif len(field_names.split()) > 1:
                list_element = field_names.split()
                for element in list_element:
                    final_list.append(element.lstrip())
                for e in unique(final_list):
                    list_return.append(legal_name(e))
                return list_return
            else:
                return list(legal_name(field_names))
        else:
            raise SyntaxError('The field names must be either a string or list')
    
    
    def unique(iterable): 
        iterated = set()
        for i in iterable:
            if i not in iterated:
                iterated.add(i)
                yield i
                
                
    def legal_default(list_field_names, default: dict) -> bool:
        for element in default.keys():
            if element not in list_field_names:
                raise SyntaxError('{} is not a field name'.format(element))
        return True
    
    
    def init_param(field_names, defaults):
        list_param = legal_field_name(field_names)
        if len(defaults) > 0 and legal_default(legal_field_name(field_names), defaults) == True:
            for each_key in defaults:
                ind = list_param.index(each_key)
                del list_param[ind]
                list_param.insert(ind, '{}={}'.format(each_key, defaults.get(each_key)))
        return ', '.join(list_param)
    
    
    def gen_attr(field_names):
        final_str = ''
        for element in legal_field_name(field_names):
            final_str += gen_init.format(attr = element, arg_val = element)
        return final_str
    
    
    def str_for_repr(field_names):
        final_str = '{}={{}}'.format(legal_field_name(field_names)[0])
        for element in legal_field_name(field_names)[1:]:
            final_str += ',{}={{}}'.format(element)
        return final_str
    
    
    def str_for_self(field_names):
        final_str = 'self.{}'.format(legal_field_name(field_names)[0])
        for element in legal_field_name(field_names)[1:]:
            final_str += ', self.{}'.format(element)
        return final_str
    
    
    def str_for_get(field_names):
        final_str = ''
        for element in legal_field_name(field_names):
            final_str += gen_get.format(attr = element, self_val = 'self.{}'.format(element))
        return final_str
        
        
    def list_for_eq(field_names):
        final_list = []
        for element in legal_field_name(field_names):
            final_list.append('self.{} == comp_obj.{}'.format(element, element))  
        return final_list
        
    
    type_class_definition = '''\
class {class_name}:
\t_fields = {field_names}
\t_mutable = {mutable}\n  
'''    
    
    gen_class = '''\
\tdef __init__(self, {}):
'''

    gen_init = '''\
\t\tself.{attr} = {arg_val}
'''

    gen_repr = '''\
\n\tdef __repr__(self):
'''

    gen_contents = '''\
\t\treturn '{class_name}({repr_contents})'.format({self_contents})\n
'''

    gen_get = '''\
\tdef get_{attr}(self):
\t\treturn {self_val}\n
'''

    gen_getitem = '''\
\tdef __getitem__(self,index):
\t\tif type(index) == int and index < len(self._fields):
\t\t\treturn eval('self.get_{}()'.format(self._fields[index])) 
\t\telif type(index) == str and index in self._fields:
\t\t\treturn eval('self.get_' + index + '()')
\t\telse:
\t\t\traise IndexError('The index is out of range')\n
'''   

    gen_eq = '''\
\tdef __eq__(self, comp_obj):
\t\tif type(self) == type(comp_obj):
\t\t\treturn {cond_str}
\t\telse:
\t\t\treturn False\n
'''

    gen_asdict = '''\
\tdef _asdict(self):
\t\tfinal_dict = {}
\t\tfor element in self._fields:
\t\t\tfinal_dict[element] = eval('self.get_{}()'.format(element))
\t\treturn final_dict\n
'''

    gen_make = '''\
\tdef _make(iterable):
\t\treturn {class_name}(*iterable)\n
'''

    gen_replace = '''\
\tdef _replace(self, **kargs):
\t\tfor each_key in kargs:
\t\t\tif each_key not in self._asdict().keys():
\t\t\t\traise TypeError('The key is not a field name')
\t\tif self._mutable == True:
\t\t\tfor each_key in kargs:
\t\t\t\tself.__dict__[each_key] = kargs.get(each_key)
\t\t\treturn None
\t\telse:
\t\t\told_dict = self._asdict()
\t\t\tfor each_key in kargs.keys():
\t\t\t\told_dict[each_key] = kargs.get(each_key)
\t\t\treturn {class_name}(*old_dict.values())\n
'''

    gen_setattr = '''\
\tdef __setattr__(self, name, value):
\t\tif self._mutable == False:
\t\t\tif name in self._fields and str(name) not in self.__dict__:
\t\t\t\tself.__dict__[name] = value
\t\t\telse:
\t\t\t\traise AttributeError('The object is not mutable')
\t\telse:
\t\t\tself.__dict__[name] = value
'''
    
    
    class_definition = \
      type_class_definition.format(class_name = legal_name(type_name), field_names = legal_field_name(field_names), mutable = mutable) \
      + gen_class.format(init_param(field_names, defaults)) \
      + gen_attr(field_names) \
      + gen_repr \
      + gen_contents.format(class_name = type_name, repr_contents = str_for_repr(field_names), self_contents = str_for_self(field_names)) \
      + str_for_get(field_names) \
      + gen_getitem \
      + gen_eq.format(cond_str = ' and '.join(list_for_eq(field_names))) \
      + gen_asdict \
      + gen_make.format(class_name = type_name) \
      + gen_replace.format(class_name = type_name) \
      + gen_setattr
      
    
            
                    


    # To help debug, uncomment next line, which shows source code for the class
    # show_listing(class_definition)
    
    # Execute the class_definition (str), in a special name space; then bind its
    #   source_code attribute to class_definition; following try/except return
    #   the class object created; if there is a syntax error, show the class
    #   and also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )        
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):            
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    #driver tests
    import driver  
    driver.default_file_name = 'bscp3S20.txt'
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
