import random
import subprocess
import sys
from pathlib import Path


def generate_problems(output_directory: Path, num_probs_per_difficulty: int = 100):
    # The following code is a part of the driverlog_generator.py file
    # It is used to generate problems for the driverlog domain
    # The code is used to generate problems for learning purposes
    # It is not used in the main application
    print("generating problems for the satellite domain...")
    for i in range(num_probs_per_difficulty):
        # Generate problems for the easy difficulty
        problem_name = f"pfile{i}.pddl"
        problem_path = output_directory / problem_name
        generate_problem_command = f"./satgen -n {random.randint(1, 100)} {random.randint(1, 4)} 3 {random.randint(3, 4)} {random.randint(3, 5)} {random.randint(4, 10)} > {problem_path}"
        print(f"generating problem {problem_name}...")
        subprocess.check_output(generate_problem_command, shell=True)

    for i in range(num_probs_per_difficulty):
        # Generate problems for the medium difficulty
        problem_name = f"pfile{num_probs_per_difficulty + i}.pddl"
        problem_path = output_directory / problem_name
        generate_problem_command = f"./satgen -n {random.randint(1, 100)} 5 3 {random.randint(3, 5)} {random.randint(3, 5)} {random.randint(10, 25)} > {problem_path}"
        print(f"generating problem {problem_name}...")
        subprocess.check_output(generate_problem_command, shell=True)


def main():
    output_directory = sys.argv[1]
    generate_problems(Path(output_directory))


if __name__ == "__main__":
    main()
