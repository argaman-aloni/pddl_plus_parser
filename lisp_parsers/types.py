"""Module to contain all user defined types needed for the parsing process."""
from types import Union
from typing import List

Token = str
Number = Union[int, float]
Expression = Union[Token, List['Expression']]