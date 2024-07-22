"""
Feel totally free to read, copy, modify, test and play with this file!
(But don't push it to the repository, lol!)
"""
import sys
sys.path.append( '/'.join(__file__.split('/')[:-2]) )

from src.strool.strool import *
import src.strool.strool as st
from typing import Callable, Literal, Iterable
from io import StringIO

def debug(self,
          get : Literal['var', 'func', 'all'] = 'var',
          ignore_from_class : Iterable  = (None,),
          ignore_single_underscore = False,
          print_else_return=True):
    def select(get, name):
        try: attr = self.__getattribute__(name)
        except: attr = None
        match (get, isinstance(attr, Callable)):
            case ('var' , True ): return 0
            case ('func', False): return 0
            case (  _   , None ): return 0
            case ('var' , False): return item, attr
            case ('func', True ): return item, attr
            case ('all' ,   _  ): return item, attr
            case _ : raise Exception("Unknown error ocurred")

    match get:
        case 'func': names = ['Functions']
        case 'var' : names = ['Variables']
        case   _   : names = ['Attributes']
    attrs = [type(self)]

    ignore_set = set()
    for item in ignore_from_class:
        ignore_set.update( dir(item) )

    for item in dir(self):
        if item in ignore_set: continue
        if item.startswith('_' if ignore_single_underscore else '__'): continue
        selection = select(get, item)
        if selection != 0:
            name, attr = selection
            names.append(name)
            attrs.append(attr)
    
    string_io = StringIO()

    print(file=string_io)
    max_len = max(len(item) for item in names)
    for name, value in zip(names, attrs):
        print( (max_len-len(name))*' '+name, ': ', value, sep='', file=string_io)

    out = string_io.getvalue()
    string_io.close()

    if print_else_return: print(out)
    else: return(out)

Strool.debug = debug
Strook.debug = debug

test_strool = Strool('test test test' )
test_strook = Strook(test_strool).modify(case='yes', cases=['yes', 'affirmative', 'positive'])

a = test_strool.print(return_type=('stl', 'all'))
for i in (print(type(item)) for item in a): pass

from collections import UserString
test_strook.debug('func', ignore_from_class = (UserString,), ignore_single_underscore = True)
test_strook.debug('var', ignore_from_class = (None,), ignore_single_underscore = True)

from timeit import timeit
print( 'Strool 1.000.000 times:', timeit(Strool) )
print( 'Strook 1.000.000 times:', timeit(Strook) )