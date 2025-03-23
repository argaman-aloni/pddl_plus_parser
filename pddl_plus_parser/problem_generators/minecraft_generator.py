#!/usr/bin/python3
import random
import sys
from pathlib import Path
from typing import NoReturn

from pddl_plus_parser.problem_generators import get_problem_template

TEMPLATE_FILE_PATH = Path("minecraft_template.pddl")


def generate_instance(instance_name: str, num_trees: int) -> str:
    """Generate a single planning problem instance.

    :param instance_name: the name of the problem instance.
    :param num_counters: the number of counters in the problem.
    :param max_int: the maximal integer value.
    :return: the string representing the planning problem.
    """
    template = get_problem_template(TEMPLATE_FILE_PATH)
    template_mapping = {
        "instance_name": instance_name,
        "trees_in_map_initial": f"(= (trees_in_map) {random.randint(0, 100)})",
        "count_log_in_inventory_initial": f"(= (count_log_in_inventory) {random.randint(0, 2)})",
        "count_planks_in_inventory_initial": f"(= (count_planks_in_inventory) {random.randint(0, 2)})",
        "count_stick_in_inventory_initial": f"(= (count_stick_in_inventory) {random.randint(0, 2)})",
        "count_sack_polyisoprene_pellets_in_inventory_initial": f"(= (count_sack_polyisoprene_pellets_in_inventory) {random.randint(0, 1)})",
        "count_tree_tap_in_inventory_initial": f"(= (count_tree_tap_in_inventory) {random.randint(0, 1)})",
    }
    return template.substitute(template_mapping)


def generate_multiple_problems(output_folder: Path) -> NoReturn:
    """Generate multiple problems based on the input arguments.

    :param min_counters: the minimal number of counters possible in the problems.
    :param max_counters: the maximal number of counters possible in the problems.
    :param max_int: the maximal integer value.
    :param output_folder: the path to the output folder where the problems will be saved.
    """
    for i in range(100, 200):
        print(f"Generating problem with {i} counters")
        with open(output_folder / f"pfile{i}.pddl", "wt") as problem_file:
            problem_file.write(generate_instance(f"instance_{i}"))


def main():
    generate_multiple_problems(output_folder=Path(sys.argv[1]))


if __name__ == "__main__":
    main()
