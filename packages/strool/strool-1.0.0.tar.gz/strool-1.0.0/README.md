# strool

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
- from strool import * : to use "Strool" or "Strook" directly.

## Installation

From your console write `pip install strool`

### Contact

Carlos González

carlos.a.gb95@gmail.com
