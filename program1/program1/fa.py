# Submitter: nicholhh(Huynh, Nicholas)
import goody


def read_fa(file : open) -> {str:{str:str}}:
    with file:
        line_list = [line.rstrip('\n') for line in file]
        final_dict = {}
        for each_line in line_list:
            list_val = each_line.split(';')
            final_dict[list_val[0]] = {element[0] : element[1] for element in list(zip(list_val[1::2], list_val[2::2]))}       
    return final_dict
            

def fa_as_str(fa : {str:{str:str}}) -> str:
    final_str = ''
    for each_key in sorted(fa):
        final_str += '  {} transitions: {}\n'.format(each_key, sorted(fa.get(each_key).items()))
    return final_str

    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    final_list = [state]
    new_state = state
    for each_input in inputs:
        if fa.get(new_state).get(each_input) != None:
            new_state = fa.get(new_state).get(each_input)
            final_list.append((each_input, new_state))
        else:
            final_list.append(('x', None))
            break
    return final_list
        


def interpret(fa_result : [None]) -> str:
    final_str = 'Start state = {}\n'.format(fa_result[0])
    for element in fa_result[1:]:
        if element[0] != 'x':
            final_str += '  Input = {}; new state = {}\n'.format(element[0], element[1])
        else:
            final_str += '  Input = {}; illegal input: simulation terminated\n'.format(element[0])
    final_str += 'Stop state = {}\n'.format(fa_result[-1][1])
    return final_str




if __name__ == '__main__':
    # Write script here
    
    file_input = input('Enter the file name designating this Finite Automaton: ')
    fa_dict = read_fa(open(file_input))
    print('\nThe Contents of the file designating this Finite Automaton\n{}'.format(fa_as_str(fa_dict)))
    sequence_file = input('Enter the file name designating a sequence of start-states and their subsequent inputs: ')
    line_list = []
    print('')
    with open(sequence_file) as open_sequence:
        line_list = [line.rstrip('\n') for line in open_sequence]
    for each_line in line_list:
        list_contents = each_line.split(';')
        print('Initiate tracing this FA from a start-state\n{}'.format(interpret(process(fa_dict, list_contents[0], list_contents[1:]))))
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
