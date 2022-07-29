#!/usr/bin/python3
import argparse
import itertools
import random
from pathlib import Path

from pddl_plus_parser.problem_generators import get_problem_template

TEMPLATE_FILE_PATH = Path("sailing_template.pddl")


def generate_instance(instance_name: str, num_boats: int, num_people: int, max_dist_goals: int) -> str:
    template = get_problem_template(TEMPLATE_FILE_PATH)
    template_mapping = {
        "instance_name": instance_name,
        "domain_name": "sailing",
        "boat_name_list": " ".join([f"b{i}" for i in range(num_boats)]),
        "boat_positions": "\n".join(
            [f"(= (x b{i}) {random.randint(-10, +10)})\n(= (y b{i}) 0)" for i in range(num_boats)]),
        "people_name_list": " ".join([f"p{i}" for i in range(num_people)]),
        "people_d_position": "\n".join(
            [f"(= (d p{i}) {random.randint(0, max_dist_goals)})" for i in range(num_people)]),
        "people_to_save": "\n".join([f"(saved p{i})" for i in range(num_people)])
    }

    return template.substitute(template_mapping)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate sailing planning instance")
    parser.add_argument("--min_boats", required=True, help="Starting numer of boats")
    parser.add_argument("--max_boats", required=True, help="Maximal number of boats")
    parser.add_argument("--min_people", required=True, help="Min of people to save")
    parser.add_argument("--max_people", required=True, help="Max of people to save")
    parser.add_argument("--max_dist_goal", required=False, help="Max distance people to be rescued", default=500)
    parser.add_argument("--output_folder", required=True, help="Path to the directory containing the generated problems")

    args = parser.parse_args()
    return args


def generate_multiple_problems(
        min_boats: int, max_boats: int, min_people: int, max_people: int, max_dist_goal: int, output_folder: Path):
    boats_range = [i for i in range(min_boats, max_boats + 1)]
    people_range = [i for i in range(min_people, max_people + 1)]
    for num_boats, num_people in itertools.product(boats_range, people_range):
        with open(output_folder / f"pfile{num_boats}_{num_people}_{max_dist_goal}.pddl", "wt") as problem_file:
            problem_file.write(
                generate_instance(f"instance_{num_boats}_{num_people}", num_boats, num_people, max_dist_goal))


def main():
    generate_multiple_problems(16, 20, 5, 9, 100, Path("C:\Argaman\Planning\Minecraft\more_domains\sailin"))
    # args = parse_arguments()
    # generate_multiple_problems(args.min_boats, args.max_boats, args.min_people, args.max_people, args.max_dist_goal,
    #                            Path(args.output_folder))


if __name__ == '__main__':
    main()
