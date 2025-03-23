#!/usr/bin/python3
import argparse
import random
from pathlib import Path
from typing import NoReturn

from pddl_plus_parser.problem_generators import get_problem_template

TEMPLATE_FILE_PATH = Path("preschool_template.pddl")


def generate_instance(instance_name: str, num_students: int) -> str:
    """Generate a single planning problem instance.

    :param instance_name: the name of the problem instance.
    :param num_students: the number of counters in the problem.
    :param max_int: the maximal integer value.
    :return: the string representing the planning problem.
    """
    template = get_problem_template(TEMPLATE_FILE_PATH)
    teacher_x = random.randint(0, 100)
    teacher_y = random.randint(0, 100)
    students_positions = []
    for i in range(num_students):
        x_student = random.randint(0, 100)
        y_student = random.randint(0, 100)
        while x_student == teacher_x and y_student == teacher_y:
            x_student = random.randint(0, 100)
            y_student = random.randint(0, 100)

        students_positions.append((x_student, y_student))

    template_mapping = {
        "instance_name": instance_name,
        "domain_name": "pre-schooler",
        "counters_list": " ".join([f"c{i}" for i in range(2 * num_students)]),
        "students_list": " ".join([f"s{i}" for i in range(num_students)]),
        "teacher_initial_position": f"(= (x-teacher teacher) {teacher_x})\n\t(= (y-teacher teacher) {teacher_y})",
        "students_initial_positions": "\n\t".join(
            [
                f"(= (x-student s{i}) {x})\n\t(= (y-student s{i}) {y})"
                for i, (x, y) in enumerate(students_positions)
            ]
        ),
        "counters_initial_values": "\n\t".join(
            [
                f"(= (value c{2 * i} s{i}) 0)\n\t(= (value c{2 * i + 1} s{i}) 0)"
                for i in range(num_students)
            ]
        ),
        "goal_constraints": "\n\t".join(
            [f"(question-answered s{i})" for i in range(num_students)]
        ),
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
        num_students = random.randint(1, max_students)
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
