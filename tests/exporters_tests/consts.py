import os
from pathlib import Path

CWD = Path(os.getcwd()) / "exporters_tests"
TEST_DISCRETE_DOMAIN_PATH = Path(CWD, "elevators_domain.pddl")
TEST_DISCRETE_PROBLEM_PATH = Path(CWD, "elevators_p03.pddl")
TEST_DISCRETE_PLAN_PATH = Path(CWD, "elevators_p03_plan.solution")
TEST_NUMERIC_DOMAIN_PATH = Path(CWD, "depot_numeric.pddl")
TEST_NUMERIC_PROBLEM_PATH = Path(CWD, "pfile2.pddl")
TEST_NUMERIC_PLAN_PATH = Path(CWD, "depot_numeric.solution")
TEST_FAULTY_NUMERIC_PLAN_PATH = Path(CWD, "depot_numeric_faulty.solution")
TEST_DISCRETE_TRAJECTORY_FILE_PATH = Path(CWD, "test_trajectory")
TEST_NUMERIC_TRAJECTORY_FILE_PATH = Path(CWD, "test_numeric_trajectory")

TEST_CONDITIONAL_DOMAIN_PATH = Path(CWD, "domain_spider.pddl")
TEST_CONDITIONAL_PROBLEM_PATH = Path(CWD, "pfile01_spider.pddl")
TEST_CONDITIONAL_PLAN_PATH = Path(CWD, "pfile01_spider.solution")

TEST_MINECRAFT_DOMAIN_PATH = Path(CWD, "minecraft_domain.pddl")
TEST_MINECRAFT_PROBLEM_PATH = Path(CWD, "minecraft_problem.pddl")
TEST_MINECRAFT_PLAN_PATH = Path(CWD, "minecraft_pfile0.solution")


TEST_MICONIC_DOMAIN_PATH = Path(CWD, "domain_miconic.pddl")
TEST_MICONIC_PROBLEM_PATH = Path(CWD, "miconic_problem.pddl")
TEST_MICONIC_PLAN_PATH = Path(CWD, "miconic_solution.solution")