#!/usr/bin/python3
import argparse
import itertools
import random
from pathlib import Path

from pddl_plus_parser.problem_generators import get_problem_template

TEMPLATE_FILE_PATH = Path("counters_template.pddl")


def generate_instance(instance_name: str, num_counters: int, max_int: int) -> str:
    template = get_problem_template(TEMPLATE_FILE_PATH)
    template_mapping = {
        "instance_name": instance_name,
        "domain_name": "fo-counters-rnd",
        "counters_list": " ".join([f"c{i}" for i in range(num_counters)]),
        "counters_initial_values": "\n\t".join(
            [f"(= (value c{i}) {random.randint(0, max_int)})" for i in range(num_counters)]),
        "counters_rate_values": "\n\t".join([f"(= (rate_value c{i}) 0)" for i in range(num_counters)]),
        "max_int_value": max_int,
        "counters_final_values": "\n\t".join(
            [f"(<= (+ (value c{i}) 1) (value c{i + 1}))" for i in range(num_counters - 1)])
    }
    return template.substitute(template_mapping)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate sailing planning instance")
    parser.add_argument("--num_counters", required=True, help="number of counters in the problems")
    parser.add_argument("--max_int", required=True, help="Maximal integer value")
    args = parser.parse_args()
    return args


def generate_multiple_problems(
        min_counters: int, max_counters: int, max_int: int, output_folder: Path):
    counters_range = [i for i in range(min_counters, max_counters + 1)]
    for num_counters in counters_range:
        with open(output_folder / f"pfile{num_counters}_{random.randint(0, 100)}.pddl", "wt") as problem_file:
            problem_file.write(
                generate_instance(f"instance_{num_counters}_{max_int}", num_counters, max_int))


def main():
    generate_multiple_problems(2, 40, 100, Path("C:\Argaman\Planning\Minecraft\more_domains\counters"))


if __name__ == '__main__':
    main()
