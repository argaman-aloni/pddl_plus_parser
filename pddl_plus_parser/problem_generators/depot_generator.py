import random
import subprocess
import sys
from pathlib import Path


def generate_problems(output_directory: Path, num_probs_per_difficulty: int = 50):
    print("generating problems for the depot domain...")
    for i in range(num_probs_per_difficulty):
        # Generate problems for the easy difficulty
        problem_name = f"pfile{i}.pddl"
        problem_path = output_directory / problem_name
        generate_problem_command = f"./depotgen {random.randint(1, 100)} -n -w 100 -c 400 1 2 2 3 3 {random.randint(2, 15)} > {problem_path}"
        print(f"generating problem {problem_name}...")
        subprocess.check_output(generate_problem_command, shell=True)

    for i in range(num_probs_per_difficulty):
        # Generate problems for the medium difficulty
        problem_name = f"pfile{num_probs_per_difficulty + i}.pddl"
        problem_path = output_directory / problem_name
        generate_problem_command = f"./depotgen {random.randint(1, 100)} -n -w 100 -c 400 3 3 2 {random.randint(6, 15)} {random.randint(6, 15)} {random.randint(2, 30)} > {problem_path}"
        print(f"generating problem {problem_name}...")
        subprocess.check_output(generate_problem_command, shell=True)


def main():
    output_directory = sys.argv[1]
    generate_problems(Path(output_directory))


if __name__ == "__main__":
    main()
