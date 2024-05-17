import random
import subprocess
import sys
from pathlib import Path


def generate_problems(output_directory: Path, num_probs_per_difficulty: int = 100):
    # The following code is a part of the driverlog_generator.py file
    # It is used to generate problems for the driverlog domain
    # The code is used to generate problems for learning purposes
    # It is not used in the main application
    print("generating problems for the polynomial driverlog domain...")
    for i in range(num_probs_per_difficulty):
        # Generate problems for the easy difficulty
        problem_name = f"pfile{i}.pddl"
        problem_path = output_directory / problem_name
        generate_problem_command = f"./dlgen -h {random.randint(1, 100)} 3 {random.randint(2, 4)} {random.randint(2, 10)} {random.randint(2, 5)} 100 > {problem_path}"
        print(f"generating problem {problem_name}...")
        subprocess.check_output(generate_problem_command, shell=True)

    for i in range(num_probs_per_difficulty):
        # Generate problems for the medium difficulty
        problem_name = f"pfile{num_probs_per_difficulty + i}.pddl"
        problem_path = output_directory / problem_name
        generate_problem_command = f"./dlgen -h {random.randint(1, 100)} {random.randint(5, 15)} {random.randint(3, 5)} {random.randint(3, 15)} {random.randint(3, 8)} 100 > {problem_path}"
        print(f"generating problem {problem_name}...")
        subprocess.check_output(generate_problem_command, shell=True)


def main():
    output_directory = sys.argv[1]
    generate_problems(Path(output_directory))


if __name__ == "__main__":
    main()
