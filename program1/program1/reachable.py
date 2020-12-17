# Submitter: nicholhh(Huynh, Nicholas)
import goody
import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    with file:
        line_list = [line.rstrip('\n') for line in file]
        nodes_dict = {}
        for each_line in line_list:
            if nodes_dict.get(each_line[0]) != None:
                nodes_dict.get(each_line[0]).add(each_line[2])
            else:
                nodes_dict[each_line[0]] = set(each_line[2])
    
    return nodes_dict
            

def graph_as_str(graph : {str:{str}}) -> str:
    final_str = ''
    for each_key in sorted(graph):
        final_str += ('  {} -> {}\n'.format(each_key, sorted(graph.get(each_key))))
    
    return final_str

        
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    reached_set = set()
    exploring_list = [start]
    while True:
        set_values = graph.get(exploring_list[0])
        if trace == True:
            print('\nreached_set    = {}\nexploring list = {}'.format(reached_set, exploring_list))
        if set_values != None:
            for each_value in set_values:
                exploring_list.append(each_value)
        reached_set.add(exploring_list[0])
        if trace == True:
            print('removing node {node} from the exploring list; then adding it to the reached list\nafter adding all nodes reachable directly from {node} but not already in reached, exploring = {node_list}'.format(node = exploring_list[0], node_list = exploring_list[1:]))
        exploring_list.pop(0)
        if len(exploring_list) == 0:
            break
    return reached_set




if __name__ == '__main__':
    # Write script here
    file_input = input('Enter the file name designating this graph: ')
    nodes_dict = read_graph(open(file_input))
    print('\nGraph: a node -> [designating all its destination nodes]')
    print(graph_as_str(nodes_dict))
    while True:
        start_input = input('Enter one start node (or enter quit): ')
        if start_input == 'quit':
            break
        elif start_input not in nodes_dict.keys():
            print('  Entry Error: \'{}\'; Illegal: not a source node\n  Please enter a legal String\n'.format(start_input))
        else:
            trace_input = input('Enter whether or not to trace the algorithm[True]: ')
            if trace_input == 'True':
                print('From the node {} its reachable nodes: {}\n'.format(start_input, reachable(nodes_dict, start_input, bool(trace_input))))
            else:
                print('From the node {} its reachable nodes: {}\n'.format(start_input, reachable(nodes_dict, start_input)))
            
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
