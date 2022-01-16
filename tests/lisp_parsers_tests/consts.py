import os
from pathlib import Path

CWD = os.getcwd()
TEST_PARSING_FILE_PATH = Path(CWD, "test_domain_format_file.pddl")
TEST_WOODWORKING_DOMAIN_PATH = Path(CWD, "woodworking_domain.pddl")
TEST_NUMERIC_DEPOT_DOMAIN_PATH = Path(CWD, "depot_numeric_domain.pddl")
