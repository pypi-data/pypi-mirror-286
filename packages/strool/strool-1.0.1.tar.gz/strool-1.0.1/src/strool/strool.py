"""strool - Fusion between str and bool
    
It's a lot like strings, but with boolean controls. They could display
the text or not, depending on the parameters.

Inside the module there's available:
- Strool (str bool): gives text if "case" is True.
- Strook (str case): gives text if "case" can be found in "cases".
- Strool.whoosh: returns an invisible version of the string provided. It
can be the object's "self". To do that, don't pass any argument.

Strook inherits from Strool, so `isinstance(Strook(), Strool)` will
return True. Check each one for more details.

The recommended way to import is one of the following:
- import strool as st : to use "st.l" and "st.k"
- from strool import * : to use "Strool" or "Strook" directly."""

from __future__ import annotations
from typing import Iterable, Any, IO, Literal
from collections import UserString
from re import sub

__all__ = ['Strool', 'Strook', 'k', 'l']

class Strool(UserString):
    """Strool - A string, but it will show text or not, depending on the
    boolean value of "case".

    Parameters:
    - string: actual text stored, it will be shown if check returns True.
    - case: bool-compatible object that will determine the "check" return.
    - negated: False by default, negates "check" output.
    - invisible_ink: if true, when check returns False, text will be
    invisible.

    Except for "string", all parameters are saved inside the object with the
    name of the parameter (e.g.: "case" is saved in "object.case"). The
    parameter "string" is saved in "object.data".
    
    Methods:
    - check: returns True if text would be shown, taking "negated" into
    account, otherwise False.
    - reset_count: sets the counter of how many times the text has been
    shown (self.recount) to 0.
    - print: prints the text if "check" returns True. You can set a
    "return_type".
    - modify: an easy way to modify the object's parameters. 

    To convert between strool types, simply give the old strool object to
    the new strool constructor. e.g.: `new_object = st.k(Strool_object)`.
    It'll ignore any parameters and save all data from the object."""

    __slots__ = ['data', 'case', 'negated', 'invisible_ink', 'recount', 'last_try', 'cases', 'case_sensitive']
    def __init__(self,
                 string : str | Strool = '',
                 case : bool | Any = True,
                 *,
                 negated: bool = False,
                 invisible_ink : bool = False
                 ) -> None:
        
        if isinstance(string, Strool):
            super().__init__(string.data)
            self.case = string.case
            self.negated = string.negated
            self.invisible_ink = string.invisible_ink
            self.recount = string.recount
            self.last_try = string.last_try

            try:
                self.cases = string.cases
                self.case_sensitive = string.case_sensitive
            except: pass

        else:
            super().__init__(string)
            self.case = case
            self.negated = negated
            self.invisible_ink = invisible_ink
            self.recount = 0
            self.last_try = False
       
        self.whoosh = self._object_whoosh

    def check(self):
        """Returns True if bool(case) is True, otherwise False. If "negated" is
        True, the output is negated (True becomes False and False becomes True)."""
        if self.negated: return not bool(self.case)
        else: return bool(self.case)
    
    def print(self,
              *,
              end: str = '\n',
              file: IO[str] | None = None,
              flush: bool = False,
              return_type : Iterable[str] | Literal['bool', 'int', 'str', 'stl', 'all'] = ()
              ) -> None | bool | int | str | Strool | tuple:
        """The method responsible for printing, it can do pretty much the same as
        regular "print(strool_object)", but it can be simpler to read by humans,
        specially when you don't want/have to save the text in a variable.
        You can also set a return_type:

        - bool: returns True or False, depending if the text has been shown.
        - int: returns the total amount of times the text has been shown.
        - str: returns the actual string shown, if it was shown, otherwise
        it'll return an empty (or invisible) string.
        - stl: returns the actual strool object (useful to print and store
        in one line).
        - all: returns a list with all the previous returns, in that order.

        For multiple selection, you can make it an Iterable, and it will return
        a list with all the returns in the order they were written. For example:
        `object.print(return_type = ('str', 'bool'))` will return str and
        bool, in that order."""
        def append_to_return_list(self, item):
            match (item, self.last_try, self.invisible_ink):
                case ('bool',  x  ,   y  ): return_list.append(self.last_try)
                case ('int',   x  ,   y  ): return_list.append(self.recount)
                case ('str', True ,   _  ): return_list.append(self.data)
                case ('str', False, True ): return_list.append(self.whoosh(self.data))
                case ('str', False, False): return_list.append('')
                case ('stl',   x  ,   y  ): return_list.append(self)
                case ('all', True ,   _  ): return_list.extend((self.last_try, self.recount, self.data, self))
                case ('all', False, True ): return_list.extend((self.last_try, self.recount, self.whoosh(self.data), self))
                case ('all', False, False): return_list.extend((self.last_try, self.recount, '', self))

        def handle_end(self, end):
            match (self.last_try, self.invisible_ink):
                case (True, _) : return end
                case (False, False) : return ''
                case (False, True) : return self.whoosh(end)

        print(self.__str__(), end=handle_end(self, end), file=file, flush=flush)

        return_list = []
        if isinstance(return_type, Iterable) and not isinstance(return_type, (str, UserString)):
            for item in return_type:
                if item in ('bool', 'int', 'str', 'stl', 'all'): append_to_return_list(self, item)
        else: append_to_return_list(self, return_type)

        match len(return_list):
            case 0 : return None
            case 1 : return return_list[0]
            case _ : return tuple(return_list)

    def modify(self,
               string : str | Strool = None,
               case : Any = None,
               cases : Iterable = None, *,
               negated : bool = None,
               invisible_ink : bool = None,
               case_sensitive : bool = None,
               case_none : bool = False):
        """An easy way to modify the object's parameters. Specially useful when you
        convert between strool types. It modifies the object and returns it. For
        example, if "stl" is a Strool object, you can convert it and modify it
        the following way:
        - `stk = Strook(stl).modify(case='yes', cases=['positive', 'yes'])`
        
        This method ignores variables set to None. To set the value of "case" to
        None, set case to None and case_none to True."""

        if isinstance(string, UserString): string = string.data
        args = {'data': string,
                'case': case,
                'negated': negated,
                'invisible_ink': invisible_ink,
                'cases': cases,
                'case_sensitive': case_sensitive}

        for name, value in args.items():
            if value == None: continue
            else: self.__setattr__(name, value)

        if case_none and case == None: self.case = None
        
        return self

    def reset_count(self) -> Strool:
        """Sets the counter of how many times text has been shown to zero. It also
        returns the Strool object, so you can use the object, this function, and
        assign it to a new variable in one expression. For example:
        - `stk = Strook(stl).modify(<modifications>)\\
            .reset_count().print(return_type='stl')`"""
        self.recount = 0
        return self
    
    @staticmethod
    def whoosh(string : str) -> str:
        """WHOOOOOSH!! NOW YOUR STRING IS INVISIBLE!!!!
        
        It substitutes visible characters with whitespaces, mainly for contexts
        and fonts with fixed width, like in console programs."""
        return sub(r'(?!\s).', ' ', string)
    
    def _object_whoosh(self, string : str | None = None):
        if string == None:
            string = self.data
        return Strool.whoosh(string)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.data}>'
    
    def __str__(self):
        self.last_try = False
        match [self.check(), self.invisible_ink]:
            case [True, _] :
                        self.recount = self.recount + 1
                        self.last_try = True
                        return self.data
            case [False, False] : return ''
            case [False, True] : return self.whoosh(self.data)

    def __getattr__(self, name: str) -> Any:
        if name == 'whoosh': return self._object_whoosh
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
class Strook(Strool):
    """Strool - A string, but it will show text or not, depending if "case"
    can be found in cases.

    Parameters:
    - string: actual text stored, it will be shown if "check" returns True.
    - case: object to be found in "cases".
    - case_sensitive: if True, when "case" is text, "check" will take
    uppercase and lowercase letters as equivalent (with str.casefold).
    - negated: False by default, negates "check" output.
    - invisible_ink: if true, when check returns False, text will be
    invisible.

    Except for "string", all parameters are saved inside the object with the
    name of the parameter (e.g.: "case" is saved in "object.case"). The
    parameter "string" is saved in "object.data".
    
    Methods:
    - check: returns True if "case" can be found in "cases", otherwise
    False, unless "negated" is True.
    - reset_count: sets the counter of how many times the text has been
    shown (self.recount) to 0.
    - print: prints the text if "check" returns True. You can set a
    "return_type".
    - modify: an easy way to modify the object's parameters. 

    To convert between strool types, simply give the old strool object to
    the new strool constructor. e.g.: `new_object = st.k(Strool_object)`.
    It'll ignore any parameters and save all data from the object."""
    def __init__(self,
                 string: str | Strool = '',
                 case: Any = None,
                 cases : Iterable = [],
                 *,
                 case_sensitive : bool = False,
                 negated: bool = False,
                 invisible_ink: bool = False
                 ) -> None:
        super().__init__(string, case, negated=negated, invisible_ink=invisible_ink)
        
        if not isinstance(string, Strool):
            self.cases = cases
            self.case_sensitive = case_sensitive

    def check(self):
        """Returns True if "case" can be found in "cases", otherwise False. If
        "negated" is True, the output is negated (True becomes False and False
        becomes True)."""
        cases = []
        match (  isinstance(self.case, UserString), isinstance(self.case, str), self.case_sensitive  ):
            case ( True, False, True) :
                case = self.case.data.casefold()
                for item in self.cases:
                    try: cases.append(item.casefold())
                    except: cases.append(item)
            case ( False, True, True) :
                case = self.case.casefold()
                for item in self.cases:
                    try: cases.append(item.casefold())
                    except: cases.append(item)
            case _ :
                case = self.case
                cases = self.cases
        if self.negated: return not case in cases
        else: return case in cases

k = Strook
l = Strool