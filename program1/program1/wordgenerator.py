# Submitter: nicholhh(Huynh, Nicholas)
import goody
from goody import irange
import prompt
from random import choice


# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    list_words = [next(file) for i in range(os + 1)]
    final_dict = {tuple(list_words[0:-1]) : list(list_words[-1])}
    
    for element in file:
        del list_words[0]
        list_words.append(element)
        
        if final_dict.get(tuple(list_words[0:-1])) != None:
            if list_words[-1] not in final_dict.get(tuple(list_words[0:-1])):
                val = final_dict.get(tuple(list_words[0:-1]))
                val.append(list_words[-1])
                final_dict[tuple(list_words[0:-1])] = val
        else:
            final_dict[tuple(list_words[0:-1])] = [list_words[-1]]   
        
    return final_dict
            

def corpus_as_str(corpus : {(str):[str]}) -> str:
    final_str = ''
    val_list = []
    
    for each_key in sorted(corpus):
        final_str += '  {} can be followed by any of {}\n'.format(each_key, corpus.get(each_key))
        val_list.append(corpus.get(each_key))
        
    min_length = len(sorted(val_list, key=(lambda t : len(t)))[0])
    max_length = len(sorted(val_list, key=(lambda t : len(t)))[-1])
    final_str += 'min/max value lengths = {}/{}\n'.format(min_length, max_length)
    return final_str


def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    len_tuple = len(start)
    for i in range(count):
        if corpus.get(tuple(start[i:len_tuple + i])) != None:
            start.append(choice(corpus.get(tuple(start[i:(len_tuple + i)]))))
        else:
            start.append(None)
            break
    return start




        
if __name__ == '__main__':
    # Write script here
    order_stat = int(input('Designate an order statistic: '))
    file_input = input('Enter the file name designating the text to read: ')
    print('Corpus\n{}\nDesignate {} words for start of list'.format(corpus_as_str(read_corpus(order_stat, word_at_a_time(open(file_input)))), order_stat))
    word_1 = input('Designate word 1: ')
    word_2 = input('Designate word 2: ')
    num_word = int(input('Designate # of words for appending to list: '))
    print('Random text = {}'.format(produce_text(read_corpus(order_stat, word_at_a_time(open(file_input))), [word_1, word_2], num_word)))
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
