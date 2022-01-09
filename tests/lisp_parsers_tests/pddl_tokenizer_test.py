from pytest import fixture

from lisp_parsers import PDDLTokenizer
from tests.lisp_parsers_tests.consts import TEST_PARSING_FILE_PATH


@fixture()
def simple_lisp_parser() -> PDDLTokenizer:
    return PDDLTokenizer(TEST_PARSING_FILE_PATH)

def test_simple_parsing(simple_lisp_parser: PDDLTokenizer):
    tokens = simple_lisp_parser.parse()
    print(tokens)