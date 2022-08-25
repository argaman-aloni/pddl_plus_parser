import os
from pathlib import Path

CWD = os.getcwd()
TEST_PARSING_FILE_PATH = Path(CWD, "test_domain_format_file.pddl")
TEST_WOODWORKING_DOMAIN_PATH = Path(CWD, "woodworking_domain.pddl")
TEST_NUMERIC_DEPOT_DOMAIN_PATH = Path(CWD, "depot_numeric_domain.pddl")
TEST_NUMERIC_PROBLEM = Path(CWD, "test_agricola_problem.pddl")
TEST_NUMERIC_DOMAIN = Path(CWD, "test_agricola_domain.pddl")

TEST_NUMERIC_DEPOT_DOMAIN = Path(CWD, "depot_numeric.pddl")
TEST_NUMERIC_DEPOT_PROBLEM = Path(CWD, "pfile2.pddl")
TEST_NUMERIC_DEPOT_TRAJECTORY = Path(CWD, "test_numeric_trajectory")

FARMLAND_NUMERIC_DOMAIN = Path(CWD, "farmland.pddl")
FARMLAND_NUMERIC_PROBLEM = Path(CWD, "pfile10_10.pddl")
FARMLAND_NUMERIC_TRAJECTORY = Path(CWD, "pfile10_10.trajectory")

ZENOTRAVEL_DOMAIN_PATH = Path(CWD, "zenonumeric.pddl")
ZENOTRAVEL_PROBLEM_PATH = Path(CWD, "pfile0.pddl")

PLANT_WATERING_DOMAIN = Path(CWD, "plant_watering_domain.pddl")

WOODWORKING_COMBINED_DOMAIN_PATH = Path(CWD) / "woodworking_combined_domain.pddl"
WOODWORKING_COMBINED_PROBLEM_PATH = Path(CWD) / "woodworking_combined_problem.pddl"
WOODWORKING_COMBINED_TRAJECTORY_PATH = Path(CWD) / "ma_woodworking_trajectory.trajectory"
