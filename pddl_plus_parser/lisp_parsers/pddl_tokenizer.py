"""Module that contains the tokenization process of the PDDL files."""
import re
from collections import deque
from pathlib import Path
from typing import List, Optional

from pddl_plus_parser.lisp_parsers import Expression


class PDDLTokenizer:
    """Class that tokenizes the content of a PDDL file according to the known PDDL scheme."""

    pddl_file_content: List[str]

    def __init__(
            self, file_path: Optional[Path] = None, pddl_str: Optional[str] = None
    ):
        if file_path is None and pddl_str is None:
            raise ValueError(
                "Cannot receive both the file path and the PDDL str as null."
            )

        if file_path is not None:
            with open(file_path, "rt", encoding="utf-8") as pddl_file:
                self.pddl_file_content = pddl_file.readlines()

        else:
            self.pddl_file_content = pddl_str.replace("\t", "").split("\n")

    def _is_comment_line(self, line: str) -> bool:
        """Indicates whither or not a line is a comment line

        :param line: the line to test.
        :return: whether the line is indeed a comment line.
        """
        return line.strip().startswith(";")

    def tokenize(self) -> deque:
        """Tokenize the PDDL file into tokens."""
        tokens = deque()
        for line in self.pddl_file_content:
            if self._is_comment_line(line):
                continue

            no_comments_line = re.sub(r";.*", "", line)
            line_tokens = (
                no_comments_line.lower().replace("(", " ( ").replace(")", " ) ").split()
            )
            tokens.extend(line_tokens)

        return tokens

    def read_from_tokens(self, tokens: deque) -> Expression:
        """Extract concrete PDDL expressions from the tokens.

        :param tokens: the list of tokens extracted from the PDDL file.
        :return: concrete PDDL expressions that can be converted to objects.
        """
        if len(tokens) == 0:
            raise SyntaxError("Unexpected EOF")

        token = tokens.popleft()
        if token == "(":
            expression = []
            while tokens[0] != ")":
                expression.append(self.read_from_tokens(tokens))

            tokens.popleft()  # pop off ')'
            return expression

        if token == ")":
            raise SyntaxError("Unexpected ) while parsing the expressions")

        return token

    def parse(self) -> Expression:
        """Extracts the expressions from the PDDL file.

        :return: the list of expressions that represent the PDDL file.
        """
        return self.read_from_tokens(self.tokenize())
