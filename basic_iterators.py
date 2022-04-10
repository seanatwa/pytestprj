import os

import itertools 
import collections

############################################
## Reverse a string
############################################
def reverse_str(aStr):
    '''
    Baics list string opertion: split, join, reverse
    '''
    ret = list(aStr)
    ret.reverse()
    return ''.join(ret)
  
assert('zyz', reverse_str('xyz')


############################################
## Record postion of a elements
############################################
ret = collections.defaultdict(list)
curr_pos = 0  
for item in [2, None, -10, None, 4, 8]:
    ret[item].append(curr_pos)
    curr_pos += 1
    
print(ret)

ret = collections.defaultdict(list)
curr_pos = 0  
for item in 'mississippi':
    ret[item].append(curr_pos)
    curr_pos += 1
    
print(ret)

############################################
## Sort dictionary by value
############################################
mydict = {'one':1,'three':3,'five':5,'two':2,'four':4}

sorted(mydict.items(), key=lambda x: x[0])   # sort by key
sorted(mydict.items(), key=lambda x: x[1])   # sort by value

my_dict_sorted = dict(sorted(mydict.items(), key=lambda x: x[1]))


############################################
## Generate deck
## https://docs.python.org/3/library/itertools.html
############################################
RANKS = ['A', 'K', 'Q', 'J'] + list(map(str, range(2, 11)))
SUITS = ['H', 'D', 'C', 'S']

import itertools
ret = list(map(lambda x: '-'.join(x), 
                 list(itertools.product(SUITS, RANKS))))

print(ret)
