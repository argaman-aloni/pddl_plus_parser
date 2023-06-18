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

MICONIC_LEARNED_DOMAIN_PATH = Path(CWD) / "learned_domain_miconic.pddl"

STARCRAFT_DOMAIN_PATH = Path(CWD) / "starcraft_domain.pddl"
STARCRAFT_TRAJECTORY_PATH = Path(CWD) / "starcraft_trajectory.trajectory"


UMT2_DOMAIN_PATH = Path(CWD) / "UMT2_domain.pddl"


TEST_PREDICATES_FOR_CONDITIONAL_DOMAIN = """((on ?c1 - card ?c2 - cardposition)
    (clear ?c - cardposition)
    (in-play ?c - card)
    (current-deal ?d - deal)
    (CAN-CONTINUE-GROUP ?c1 - card ?c2 - cardposition)
    (CAN-BE-PLACED-ON ?c1 - card ?c2 - card)
    (IS-ACE ?c - card)
    (IS-KING ?c - card)
    (NEXT-DEAL ?d - deal ?nd - deal)
    (TO-DEAL ?c - card ?p - tableau ?d - deal ?next - cardposition)
    (currently-dealing)
    (currently-collecting-deck)
    (collect-card ?c - cardposition)
    (part-of-tableau ?c - cardposition ?t - tableau)
    (movable ?c - card)
    (currently-updating-unmovable)
    (make-unmovable ?c - card)
    (currently-updating-movable)
    (make-movable ?c - cardposition)
    (currently-updating-part-of-tableau)
    (make-part-of-tableau ?c - card ?t - tableau)
)
"""

TEST_PREDICATES_FOR_UNIVERSAL_QUANTIFIER_DOMAIN = """(
    (origin ?person - passenger ?floor - floor)
    (destin ?person - passenger ?floor - floor)
    (above ?floor1 - floor  ?floor2 - floor)
    (boarded ?person - passenger)
    (served ?person - passenger)
    (lift-at ?floor - floor)
)
"""


TEST_TYPES_FOR_CONDITIONAL_DOMAIN = """(cardposition - object
    card_or_tableau - cardposition
    card - card_or_tableau
    tableau - card_or_tableau
    deal - cardposition
)"""

TYPES_FOR_UNIVERSAL_CONDITIONAL_DOMAIN = """(passenger - object
          floor - object)"""

TEST_CONSTANTS_FOR_CONDITIONAL_DOMAIN = """(discard - cardposition)"""

SPIDER_DOMAIN_PATH = Path(CWD, "domain_spider.pddl")
SPIDER_PROBLEM_PATH = Path(CWD, "pfile04.pddl")

DEPOT_MA_DOMAIN_PATH = Path(CWD, "Depots.pddl")
DEPOT_MA_PROBLEM_PATH = Path(CWD, "pfile1_depot.pddl")
DEPOT_MA_TRAJECTORY_PATH = Path(CWD, "test_joint_trajectory_with_potential_bug")

LOGISTICS_MA_DOMAIN_PATH = Path(CWD, "logistics_combined_domain.pddl")
LOGISTICS_MA_PROBLEM_PATH = Path(CWD, "pfile_probLOGISTICS-14-0.pddl")
LOGISTICS_MA_TRAJECTORY_PATH = Path(CWD, "ma_logistics_trajectory.trajectory")