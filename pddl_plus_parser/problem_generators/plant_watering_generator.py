#!/usr/bin/python3
import argparse
import itertools
import random
from pathlib import Path

from pddl_plus_parser.problem_generators import get_problem_template

TEMPLATE_FILE_PATH = Path("plant_watering_template.pddl")


def construct_pouring_inner_goal(num_plants) -> str:
    """

    :param num_plants:
    :return:
    """
    if num_plants == 0:
        return f"(poured plant{num_plants})"

    inner_layer = construct_pouring_inner_goal(num_plants - 1)
    return f"(+ (poured plant{num_plants}) {inner_layer})"


def generate_instance(
    instance_name: str, num_taps: int, num_agents: int, num_plants: int
) -> str:
    template = get_problem_template(TEMPLATE_FILE_PATH)
    max_int = 10 * 2 * num_plants
    template_mapping = {
        "instance_name": instance_name,
        "domain_name": "mt-plant-watering-constrained",
        "taps_list": " ".join([f"tap{i}" for i in range(num_taps)]),
        "agents_list": " ".join([f"agent{i}" for i in range(num_agents)]),
        "plants_list": " ".join([f"plant{i}" for i in range(num_plants)]),
        "max_int_value": str(max_int),
        "poured_plants": "\n".join(
            [f"(= (poured plant{i}) 0)" for i in range(num_plants)]
        ),
        "agents_locations": "\n".join(
            [
                f"(= (x agent{i}) {coordinate})\n\t\t(= (y agent{i}) {coordinate})"
                for i, coordinate in zip(
                    range(num_agents), random.choices(range(10), k=num_agents)
                )
            ]
        ),
        "plants_locations": "\n".join(
            [
                f"(= (x plant{i}) {coordinate})\n\t\t(= (y plant{i}) {coordinate})"
                for i, coordinate in zip(
                    range(num_agents), random.choices(range(10), k=num_plants)
                )
            ]
        ),
        "taps_locations": "\n".join(
            [
                f"(= (x tap{i}) {coordinate})\n\t\t(= (y tap{i}) {coordinate})"
                for i, coordinate in zip(
                    range(num_agents), random.choices(range(10), k=num_taps)
                )
            ]
        ),
        "pour_goals": "\n".join(
            [
                f"(= (poured plant{i}) {val})"
                for i, val in zip(
                    range(num_agents), random.choices(range(max_int), k=num_plants)
                )
            ]
        ),
        "total_poured_goal": f"(= (total_poured) {construct_pouring_inner_goal(num_plants)} )",
    }
    return template.substitute(template_mapping)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate plat watering instance")
    parser.add_argument(
        "--num_taps", required=True, help="taps to plant the water with"
    )
    parser.add_argument(
        "--num_agents", required=True, help="number of agents that can water the plants"
    )
    parser.add_argument(
        "--num_plants", required=True, help="the number of plants to water"
    )
    args = parser.parse_args()
    return args


def generate_multiple_problems(
    num_taps: int, num_agents: int, num_plants: int, output_folder: Path
):
    for i in range(1, num_taps + 1):
        for j in range(1, num_agents + 1):
            for k in range(1, num_plants + 1):
                instance_name = f"{i}_{j}_{k}"
                with open(
                    output_folder
                    / f"pfile{instance_name}_{random.randint(0, 100)}.pddl",
                    "wt",
                ) as problem_file:
                    problem_file.write(
                        generate_instance(f"instance_{instance_name}", i, j, k)
                    )


def main():
    generate_multiple_problems(
        10, 10, 10, Path("C:\Argaman\Planning\Minecraft\more_domains\plant_watering")
    )


if __name__ == "__main__":
    main()
