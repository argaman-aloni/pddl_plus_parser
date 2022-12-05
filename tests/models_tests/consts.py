import os
from pathlib import Path

CWD = os.getcwd()
TEST_NUMERIC_PROBLEM = Path(CWD, "test_agricola_problem.pddl")
TEST_NUMERIC_DOMAIN = Path(CWD, "test_agricola_domain.pddl")
TEST_HARD_NUMERIC_DOMAIN = Path(CWD, "satellite_numeric_domain.pddl")

SPIDER_DOMAIN_PATH = Path(CWD, "domain_spider.pddl")
NURIKABE_DOMAIN_PATH = Path(CWD, "nurikabe_domain.pddl")
NURIKABE_PROBLEM_PATH = Path(CWD, "nurikabe_problem.pddl")