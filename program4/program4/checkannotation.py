# Submitter: nicholhh(Huynh, Nicholas)
from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # Start by binding the class attribute to True allowing checking to occur
    #   (but only if the function's self._checking_on is also bound to True)
    checking_on  = True
  
    # Check the decorated function by binding its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # Start by matching check's function annotation against its arguments
        if annot == None:
            pass 
        
        
        elif isinstance(annot, type):
                if isinstance(value, str):
                    assert isinstance(value, annot), '\'{name}\' failed annotation check(wrong type): value = \'{val}\'\n\
    was type {inc_type} ...should be type {cor_type}'.format(name=param, val=value, inc_type=type(value).__name__, cor_type=annot.__name__)
                assert isinstance(value, annot), '\'{name}\' failed annotation check(wrong type): value = {val}\n\
    was type {inc_type} ...should be type {cor_type}'.format(name=param, val=value, inc_type=type(value).__name__, cor_type=annot.__name__)
                

        
        elif isinstance(annot,list):
            assert isinstance(value, list), '\'{name}\' failed annotation check(wrong type): value = {val}\n\
    was type {inc_type} ...should be type list'.format(name=param, val=value, inc_type=type(value).__name__)
            if len(annot) == 1:
                list_class_content = annot[0]
                for i in range(len(value)):
                    try:
                        self.check(param, list_class_content, value[i], check_history)
                    except AssertionError:
                        check_history += 'list[{index}] check: {type_element}\n'.format(index=i, type_element=list_class_content)
                        raise
            elif len(annot) > 1:
                assert len(annot) == len(value), '\'{name}\' failed annotation check(wrong number of elements): value = {val}\n\
    annotation had {len_annot} elements{annot_list}'.format(name=param, val=value, len_annot=len(annot), annot_list=annot)
                for i in range(len(value)):
                    try:
                        self.check(param, annot[i], value[i], check_history)
                    except AssertionError:
                        check_history += 'list[{index}] check: {type_element}\n'.format(index=i, type_element=annot[i])
                        raise
        
        
        elif isinstance(annot, tuple):
            assert isinstance(value, tuple), '\'{name}\' failed annotation check(wrong type): value = {val}\n\
    was type {inc_type} ...should be type tuple'.format(name=param, val=value, inc_type=type(value).__name__)
            if len(annot) == 1:
                tuple_class_content = annot[0]
                for i in range(len(value)):
                    try:
                        self.check(param, tuple_class_content, value[i], check_history)
                    except AssertionError:
                        check_history += 'tuple[{index}] check: {type_element}\n'.format(index=i, type_element=type(value[i]))
                        raise
            elif len(annot) > 1:
                assert len(annot) == len(value), '\'{name}\' failed annotation check(wrong number of elements): value = {val}\n\
    annotation had {len_annot} elements{annot_list}'.format(name=param, val=value, len_annot=len(annot), annot_list=annot)
                for i in range(len(value)):
                    try:
                        self.check(param, annot[i], value[i], check_history)
                    except AssertionError:
                        check_history += 'tuple[{index}] check: {type_element}\n'.format(index=i, type_element=annot[i])
                        raise

        
        elif isinstance(annot, dict):
            assert isinstance(value, dict), '\'{name}\' failed annotation check(wrong type): value = {val}\n\
    was type {inc_type} ...should be type dict'.format(name=param, val=value, inc_type=type(value).__name__)
            assert len(annot) == 1, '\'{name}\' annotation inconsistency: dict should have 1 item but had {len_annot}\n\
    annotation = {annotation}'.format(name=param, len_annot=len(annot), annotation=annot)
            for key_class in annot:
                for each_key in value:
                    try:
                        self.check(param, key_class, each_key, check_history)
                    except AssertionError:
                        check_history += 'dict key check: {type_element}\n'.format(type_element=key_class)
                        raise
                    try:
                        self.check(param, annot[key_class], value[each_key], check_history)
                    except AssertionError:
                        check_history += 'dict key check: {type_element}\n'.format(type_element=annot[key_class])
                        raise
                
                
        elif isinstance(annot, set):
            assert isinstance(value, set), '\'{name}\' failed annotation check(wrong type): value = {val}\n\
    was type {inc_type} ...should be type set'.format(name=param, val=value, inc_type=type(value).__name__)
            assert len(annot) == 1, '\'{name}\' annotation inconsistency: set should have 1 item but had {len_annot}\n\
    annotation = {annotation}'.format(name=param, len_annot=len(annot), annotation=annot)
            for class_cont in annot:
                for element in value:
                    try:
                        self.check(param, class_cont, element, check_history)
                    except AssertionError:
                        check_history += 'set value check: {type_element}\n'.format(type_element=class_cont)
                        raise

        
        
        elif isinstance(annot, frozenset):
            assert isinstance(value, frozenset), '\'{name}\' failed annotation check(wrong type): value = {val}\n\
    was type {inc_type} ...should be type frozenset'.format(name=param, val=value, inc_type=type(value).__name__)
            assert len(annot) == 1, '\'{name}\' annotation inconsistency: frozenset should have 1 item but had {len_annot}\n\
    annotation = {annotation}'.format(name=param, len_annot=len(annot), annotation=annot)
            for class_cont in annot:
                for element in value:
                    try:
                        self.check(param, class_cont, element, check_history)
                    except AssertionError:
                        check_history += 'frozenset value check: {type_element}\n'.format(name=param, val=element, inc_type=type(element).__name__, cor_type=class_cont.__name__, type_element=class_cont)
                        raise
        
        
        elif isinstance(annot, str):
            try:    
                assert eval(annot, self.ord_dict), '\'{name}\' failed annotation check(str predicate: \'{annotation}\')\n\
    args for evaluation: {ord_dict}'.format(name=param, annotation=annot, ord_dict=', '.join([str(each_key)+'->'+str(self.ord_dict.get(each_key))  for each_key in self.ord_dict])) 
            except AssertionError:
                raise 
            except Exception as name_except:
                assert 1 == 0, '\'{name}\' annotation check(str predicate: \'{annotation}\') raised exception\n\
    exception = {type_error}: {error_name}'.format(name=param, annotation=annot, type_error=type(name_except).__name__, error_name=name_except)
        
                    
        elif inspect.isfunction(annot):
            assert len(annot.__code__.co_varnames) == 1, '\'{name} annotation inconsistency: predicate should have 1 parameter but had {len_annot}\n\
    predicate = {annotation}'.format(name=param, len_annot=len(annot.__code__.co_varnames), annotation=annot) #have to check the lambda to see if it works
            try:    
                annot(value)
                assert annot(value) 
            except AssertionError:
                raise AssertionError('\'{name}\' failed annotation check: value = {val}\n\
    predicate = {annotation}'.format(name=param, val=value, annotation=annot))
            except Exception as name_except:
                assert 1 == 0, '\'{name}\' annotation predicate({func_annot}) raised exception\n\
    exception = {type_error}: {error_type}'.format(name=param, func_annot=annot, type_error=type(name_except).__name__, error_type=name_except)
    

        else:
            try:
                annot.__check_annotation__(self.check, param, value, '')
            except AttributeError:
                assert 1 == 0, '\'{name}\' annotation undecipherable: {obj}'.format(name=param, obj=annot)
            except AssertionError:
                raise
            except Exception as name_except:
                try:
                    assert 1 == 0, '\'{name}\' annotation predicate{annotation} raised exception\n\
        exception = {type_error}: {error_name}'.format(name=param, annotation=annot, type_error=type(name_except).__name__, error_name=name_except)
                except AssertionError:
                    check_history += '{obj_name} value check:{annotation}'.format(obj_name=annot.__name__, annotation=type(value))
                    raise
                
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return the parameter/argument bindings in an ordereddict, derived
        #   from a dict: it binds the function header's parameters in order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if self.checking_on != True or self._checking_on != True:
            return self._f
        
        try:
            # For each annotation present, check if the parameter satisfies it

            # Compute/remember the value of the decorated function
            
            # If 'return' is in the annotation, check it
            
            # Return the decorated answer
            
            self.ord_dict = param_arg_bindings()
            annot_dict = self._f.__annotations__
            for each_key in annot_dict.keys(): 
                if each_key != 'return':
                    self.check(each_key, annot_dict[each_key], self.ord_dict[each_key])
            dec_func_result = self._f(*self.ord_dict.values())
            if annot_dict.get('return') != None:
                self.ord_dict['_return'] = dec_func_result
                self.check('_return', annot_dict['return'], self.ord_dict['_return'])
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
        #    print(80*'-')
        #    for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
        #        print(l.rstrip())
        #    print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation 
    
    def f(x:[[int]]): pass
    f = Check_Annotation(f)
    f([[1,2],[3,4],[5,'a']])
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4S20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
