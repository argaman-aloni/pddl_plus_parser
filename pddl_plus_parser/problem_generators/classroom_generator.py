#!/usr/bin/python3
import argparse
import random
from pathlib import Path
from typing import NoReturn

from pddl_plus_parser.problem_generators import get_problem_template

TEMPLATE_FILE_PATH = Path("classroom_template.pddl")


def generate_instance(instance_name: str, num_students: int) -> str:
    """Generate a single planning problem instance.

    :param instance_name: the name of the problem instance.
    :param num_students: the number of counters in the problem.
    :param max_int: the maximal integer value.
    :return: the string representing the planning problem.
    """
    template = get_problem_template(TEMPLATE_FILE_PATH)
    teacher_cell = random.randint(0, 99)
    legal_cells = list(range(100))
    legal_cells.remove(teacher_cell)
    students_positions = random.sample(legal_cells, num_students)

    task_distribution = [
        random.choice(["painting", "math"]) for _ in range(num_students)
    ]

    if task_distribution.count("painting") == 0:
        task_distribution[0] = "painting"
    if task_distribution.count("math") == 0:
        task_distribution[1] = "math"

    tasks_positions = random.sample(legal_cells, num_students)
    tasks_positions_strs = []
    painting_count = 0
    math_count = 0
    for task_cell, task_type in zip(tasks_positions, task_distribution):
        tasks_positions_strs.append(
            f"(position {task_type[0]}{painting_count if task_type == 'painting' else math_count} cell{task_cell})"
        )
        if task_type == "painting":
            painting_count += 1
        else:
            math_count += 1

    template_mapping = {
        "instance_name": instance_name,
        "domain_name": "classroom",
        "cells_list": " ".join([f"cell{i}" for i in range(100)]),
        "students_list": " ".join([f"s{i}" for i in range(num_students)]),
        "painting_list": " ".join(
            [f"p{i}" for i in range(task_distribution.count("painting"))]
        ),
        "math_tasks_list": " ".join(
            [f"m{i}" for i in range(task_distribution.count("math"))]
        ),
        "teacher_initial_position": f"(position homerooomteacher cell{teacher_cell})",
        "students_initial_positions": "\n\t".join(
            [
                f"(position s{i} cell{student_cell})"
                for i, student_cell in enumerate(students_positions)
            ]
        ),
        "tasks_initial_positions": "\n\t".join(tasks_positions_strs),
        "initial_students_strengths": "\n\t".join(
            [
                f"(= (strength-remaining s{i}) {random.randint(5, 10)})"
                for i in range(num_students)
            ]
        ),
        "goal_constraints": f"(= (works-collected) {num_students})",
    }
    return template.substitute(template_mapping)


def parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description="Generate counters planning instance")
    parser.add_argument(
        "--max_students",
        required=True,
        help="Maximal number of students possible in the problems",
    )
    parser.add_argument(
        "--output_path",
        required=True,
        help="The path to the output folder where the problems will be saved",
    )
    args = parser.parse_args()
    return args


def generate_multiple_problems(
    max_students: int, output_folder: Path, total_num_problems: int = 200
) -> NoReturn:
    """Generate multiple problems based on the input arguments.

    :param max_students: the maximal number of students possible in the problems.
    :param output_folder: the path to the output folder where the problems will be saved.
    """
    for i in range(total_num_problems):
        num_students = random.randint(3, max_students)
        print(f"Generating problem with {num_students} counters")
        with open(output_folder / f"pfile{i}.pddl", "wt") as problem_file:
            problem_file.write(
                generate_instance(f"instance_{random.randint(0,1000)}", num_students)
            )


def main():
    args = parse_arguments()
    generate_multiple_problems(
        max_students=int(args.max_students), output_folder=Path(args.output_path)
    )


if __name__ == "__main__":
    main()
