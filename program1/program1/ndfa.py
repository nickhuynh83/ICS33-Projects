# Submitter: nicholhh(Huynh, Nicholas)
import goody
from collections import defaultdict

def read_ndfa(file : open) -> {str:{str:{str}}}:
    with file:
        line_list = [line.rstrip('\n') for line in file]
        final_dict = {}
        for each_line in line_list:
            list_val = each_line.split(';')
            list_tuple = list(zip(list_val[1::2], list_val[2::2]))
            internal_dict = defaultdict(set)
            for each_tuple in list_tuple:
                internal_dict[each_tuple[0]].add(each_tuple[1])
            final_dict[list_val[0]] = internal_dict
    return final_dict
        


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    final_str = ''
    for each_key in sorted(ndfa):
        final_str += '  {} transitions: ['.format(each_key)
        tuple_str = ''
        for element in sorted(ndfa.get(each_key).items()):
            tuple_str += '{}'.format((element[0], sorted(element[1])))
            if sorted(ndfa.get(each_key).items()).index(element) != (len(sorted(ndfa.get(each_key).items())) - 1):
                tuple_str += ', '
        final_str += '{}]\n'.format(tuple_str)
    return final_str


       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    final_list = [state]
    list_new_state = [state]
    for each_input in inputs:
        action_set = set()
        new_states = []
        bool_val = False
        
        for element in list_new_state:
            if ndfa.get(element) != None:
                inner_dict = ndfa.get(element)
                if inner_dict.get(each_input) != None:
                    inner_val = inner_dict.get(each_input)
                    for each_element in inner_val:
                        new_states.append(each_element)
                        action_set.add(each_element)
                    
        del list_new_state
        list_new_state = []
                
        for each_state in new_states:
            list_new_state.append(each_state)

        final_list.append((each_input, action_set))
        if action_set == set():
            break
        
    return final_list


def interpret(result : [None]) -> str:
    final_str = 'Start state = {}\n'.format(result[0])
    for each_tuple in result[1:]:
        final_str += '  Input = {}; new possible states = {}\n'.format(each_tuple[0], sorted(each_tuple[1]))
    final_str += 'Stop state(s) = {}\n'.format(sorted(result[-1][1]))
    return final_str
    



if __name__ == '__main__':
    # Write script here
    file_input = input('Enter the file name designating this Non-Deterministic Finite Automaton: ')
    print('\nThe Contents of the file designating this Non-Deterministic Finite Automaton\n{}'.format(ndfa_as_str(read_ndfa(open(file_input)))))
    action_file = input('Enter the file name designating a sequence of start-states and their subsequent inputs: ')
    print('')
    with open(action_file) as open_sequence:
        line_list = [line.rstrip('\n') for line in open_sequence]
    for each_line in line_list:
        list_contents = each_line.split(';')
        print('Initiate tracing this NDFA from a start-state\n{}'.format(interpret(process(read_ndfa(open(file_input)), list_contents[0], list_contents[1:]))))
    
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
