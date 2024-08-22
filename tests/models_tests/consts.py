import os
from pathlib import Path

CWD = os.getcwd()
TEST_NUMERIC_PROBLEM = Path(CWD, "test_agricola_problem.pddl")
TEST_NUMERIC_DOMAIN = Path(CWD, "test_agricola_domain.pddl")
TEST_HARD_NUMERIC_DOMAIN = Path(CWD, "satellite_numeric_domain.pddl")

SPIDER_DOMAIN_PATH = Path(CWD, "domain_spider.pddl")
SPIDER_PROBLEM_PATH = Path(CWD, "pfile04.pddl")
NURIKABE_DOMAIN_PATH = Path(CWD, "nurikabe_domain.pddl")
NURIKABE_PROBLEM_PATH = Path(CWD, "nurikabe_problem.pddl")

MICONIC_DOMAIN_PATH = Path(CWD, "domain_miconic.pddl")
MICONIC_NESTED_DOMAIN_PATH = Path(CWD, "miconic_learned_domain.pddl")
MICONIC_NESTED_PROBLEM_PATH = Path(CWD, "miconic_pfile_1-0.pddl")
MICONIC_TRAJECTORY_PATH = Path(CWD, "miconic_pfile_1-0.trajectory")

MINECRAFT_LARGE_DOMAIN_PATH = Path(CWD, "advanced_minecraft_domain.pddl")
MINECRAFT_LARGE_PROBLEM_PATH = Path(CWD, "advanced_map_instance_0.pddl")

ZENO_DOMAIN_PATH = Path(CWD, "zenonumeric.pddl")
DEPOT_NUMERIC_DOMAIN_PATH = Path(CWD, "depot_numeric.pddl")

HARD_DRIVERLOG_DOMAIN_PATH = Path(CWD, "driverlogHardNumeric.pddl")
HARD_DRIVERLOG_PROBLEM_PATH = Path(CWD, "pfile558.pddl")

HARD_TEST_NUMERIC_DOMAIN = Path(CWD, "test_domain.pddl")
DOMAIN_TO_TEST_INEQUALITY_REMOVAL = Path(CWD, "domain_to_test_linear_inequality_removal.pddl")
DOMAIN_TO_TEST_BOTH_TYPES_OF_INEQUALITY = Path(CWD, "zenotravel_test_domain.pddl")

