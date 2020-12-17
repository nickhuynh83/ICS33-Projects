# Submitter: nicholhh(Huynh, Nicholas)
import prompt
import goody

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    with open_file:
        line_list = [line.rstrip('\n') for line in open_file]
        result_dict = {}
        for each_line in line_list:
            list_content = each_line.split(';')
            result_dict[list_content[0]] = [None, list_content[1:]]
            
    return result_dict


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    final_str = ''
    for element in sorted(d, key=key, reverse=reverse):
        final_str += ('  {} -> {}\n'.format(element, d.get(element)))
                      
    return final_str


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    for element in order:
        if element == p1 or element == p2:
            return element


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    final_set = set()
    for each_man in men:
        final_set.add((each_man, men.get(each_man)[0]))
    return final_set


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    copy_men = dict(men.items())
    unmatched_set = set(copy_men.keys())
    if trace == True:
        print('\nWomen Preferences (unchanging)\n{}'.format(dict_as_str(women)))
    while True:
        if trace == True:
            print('Men Preferences (current)\n{}\nunmatched men = {}\n'.format(dict_as_str(copy_men), unmatched_set))
        focus_man = unmatched_set.pop()
        pref_list_man = copy_men.get(focus_man)[1]
        pref_woman = pref_list_man[0]
        pref_list_man.pop(0)
        copy_men[focus_man] = [pref_woman, pref_list_man]
        match_status = False
        for each_man in men:
            if copy_men.get(each_man)[0] == pref_woman and each_man != focus_man:
                match_status = True
                favor_man = who_prefer(women.get(pref_woman)[1], each_man, focus_man)
                if favor_man == each_man:
                    unmatched_set.add(focus_man)
                    copy_men[focus_man] = [None, pref_list_man]
                    if trace == True:
                        print('{} proposes to {}, a matched woman, rejecting the proposal (preferring her current match)\n'.format(focus_man, pref_woman))
                else:
                    unmatched_set.add(each_man)
                    copy_men[each_man] = [None, copy_men.get(each_man)[1]]
                    copy_men[focus_man] = [pref_woman, pref_list_man]
                    if trace == True:
                        print('{} proposes to {}, a matched woman, accepting the proposal (preferring her new match)\n'.format(focus_man, pref_woman))
        
        if trace == True and match_status == False:
            print('{} proposes to {}, an unmatched woman, accepting the proposal\n'.format(focus_man, pref_woman))
            
        if len(unmatched_set) == 0:
            break
    
    if trace == True:
        print('At end of trace, the final matches = {}'.format(extract_matches(copy_men)))
    
    return extract_matches(copy_men)
    
  
    
if __name__ == '__main__':
    # Write script here
    file_men = input('Enter the file name designating the preferences for men: ')
    file_women = input('Enter the file name designating the preferences for women: ')
    print('\nMen Preferences\n{}\nWomen Preferences\n{}'.format(dict_as_str(read_match_preferences(open(file_men))), dict_as_str(read_match_preferences(open(file_women)))))
    trace_value = input('Enter whether or not to trace the algorithm[True]: ')
    if trace_value == 'True':
        print('\nThe final matches = {}'.format(make_match(read_match_preferences(open(file_men)), read_match_preferences(open(file_women)), trace=True)))
    else:
        print('\nThe final matches = {}'.format(make_match(read_match_preferences(open(file_men)), read_match_preferences(open(file_women)))))  
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
