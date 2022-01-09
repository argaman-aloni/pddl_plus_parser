"""Module to contain all user defined types needed for the parsing process."""
from typing import List, Union

Token = str
Number = Union[int, float]
Expression = Union[Token, List["Expression"]]