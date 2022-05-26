# Splitable str
A Python module for manipulating parts of a string that are not surrounded by specific symbols.
## Features
* Separate the part surrounded by a specific symbol and the part not surrounded by a character string.
* Perform a string operation (replacement, etc.) on the part of the string that is not surrounded by a specific symbol.
* Checks if a string is surrounded by multiple types of strings (can be forward or backward only).
## How to use
1. Import the sstr module
   
   \* To import as below, the program itself and the sstr module must be in the same directory.
   ```
   from sstr import sstr
   ```
2. Convert a normal character string (str type) to a unique character string (sstr type)
   
   ```
   old_string = 'This is a "test".'
   new_string = sstr(old_string)  # str -> sstr
   ```
   \* To convert a unique character string (sstr type) to a normal character string (str type), do the following.
   ```
   previous_string = str(new_string)  # sstr -> str
   ```
3. Performs any operation on the unique character string (sstr type).
   
   Example 1: Separate the parts surrounded and not surrounded by a specific symbol
   ```
   divided_data = new_string.divide(enclosure='"')  # (enclosure)
   print(divided_data)  # ['This is a ', '"test"', '.']
   print(type(divided_data[0]))  # <class 'str'>
   ```
   Example 2: Replace the characters in the part not surrounded by a specific symbol
   ```
   edited_string = new_string.sreplace('s', '#', enclosure='"')  # (__old, __new, enclosure)
   print(edited_string)  # Thi# i# a "test".
   print(type(edited_string))  # <class 'str'>
   ```
   Example 3: Count the number of "s" in the part not surrounded by a specific symbol (when the surrounding symbols are different before and after)
   ```
   new_string = sstr('This is a "test". This is also a (test).')
   # quantity = new_string.scount('s', enclosure='"')  # (x, enclosure)
   # quantity = new_string.scount('s', enclosure=[['(', ')']])  # (x, enclosure)
   quantity = new_string.scount('s', enclosure=['"', ['(', ')']])  # (x, enclosure)
   print(quantity)  # 5
   print(type(quantity))  # <class 'int'>
   ```
### About each method
Methods that can be used with the str type string can also be used with the sstr type string (the entire string is the target of the operation).

Some of the methods available for str strings also provide their own methods that operate only on the portion of the string not surrounded by a particular symbol (they can be called with "s" + their original name).

There is also a completely new method for sstr strings.

Please check the program file for details about the provided methods and how to call them.
## Licence
Please see the [license file](LICENSE).
