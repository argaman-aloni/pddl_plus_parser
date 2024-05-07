import random
import subprocess
import sys
from pathlib import Path


def generate_problems(output_directory: Path, num_probs_per_difficulty: int = 100):
    print("generating problems for the depot domain...")
    for i in range(num_probs_per_difficulty):
        # Generate problems for the easy difficulty
        problem_name = f"pfile{i}.pddl"
        problem_path = output_directory / problem_name
        generate_problem_command = f"./depotgen {random.randint(1, 100)} -n -w 100 -c 400 1 2 2 3 3 {random.randint(2, 15)}"
        print(f"generating problem {problem_name}...")
        result = subprocess.check_output(generate_problem_command, shell=True)
        _export_problem(problem_path, result)

    for i in range(num_probs_per_difficulty):
        # Generate problems for the medium difficulty
        problem_name = f"pfile{num_probs_per_difficulty + i}.pddl"
        problem_path = output_directory / problem_name
        generate_problem_command = f"./depotgen {random.randint(1, 100)} -n -w 100 -c 400 3 3 2 {random.randint(6, 15)} {random.randint(6, 15)} {random.randint(2, 30)}"
        print(f"generating problem {problem_name}...")
        result = subprocess.check_output(generate_problem_command, shell=True)
        _export_problem(problem_path, result)


def _export_problem(problem_path, result):
    with open(problem_path, "wt") as problem_file:
        problem_file.write(result.decode("utf-8").lower())


def main():
    output_directory = sys.argv[1]
    generate_problems(Path(output_directory))


if __name__ == "__main__":
    main()
