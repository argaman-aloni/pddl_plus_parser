import random
import subprocess
import sys
from pathlib import Path


def generate_numeric_problems(
    output_directory: Path, num_probs_per_difficulty: int = 200
):
    """Creates numeric problems for the rovers domain.

        :param output_directory: The directory where the generated problems will be saved.
        :param num_probs_per_difficulty: The number of problems to generate per difficulty level. Default is 200.
    """
    print("generating problems for the rovers domain...")
    for i in range(num_probs_per_difficulty):
        # Generate problems for the easy difficulty
        problem_name = f"pfile{i}.pddl"
        problem_path = output_directory / problem_name
        prob_num = random.randint(1, 1000)
        seed = random.randint(1, 4)
        num_rovers = random.randint(4, 8)
        num_waypoints = random.randint(2, 5)
        num_objectives = random.randint(1, 5)
        num_cameras = random.randint(1, 5)
        generate_problem_command = f"./rovergen {prob_num} -n {seed} {num_rovers} {num_waypoints} {num_objectives} {num_cameras}"
        print(f"generating problem {problem_name}...")
        result = subprocess.check_output(generate_problem_command, shell=True)
        _export_problem(problem_path, result)


def generate_strips_problems(
    output_directory: Path, num_probs_per_difficulty: int = 200
):
    """Creates numeric problems for the rovers domain.

        :param output_directory: The directory where the generated problems will be saved.
        :param num_probs_per_difficulty: The number of problems to generate per difficulty level. Default is 200.
    """
    print("generating problems for the rovers domain...")
    for i in range(num_probs_per_difficulty):
        # Generate problems for the easy difficulty
        problem_name = f"pfile{i}.pddl"
        problem_path = output_directory / problem_name
        seed = random.randint(1, 100)
        num_rovers = random.randint(2, 10)
        num_waypoints = random.randint(2, 10)
        num_objectives = random.randint(1, 5)
        num_cameras = random.randint(1, 5)
        num_goals = random.randint(1, 5)
        generate_problem_command = f"./rovergen {seed} {num_rovers} {num_waypoints} {num_objectives} {num_cameras} {num_goals}"
        print(f"generating problem {problem_name}...")
        try:
            result = subprocess.check_output(generate_problem_command, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            continue

        _export_problem(problem_path, result)


def _export_problem(problem_path, result):
    with open(problem_path, "wt") as problem_file:
        problem_content = result.decode("utf-8")
        for line in problem_content.split("\n"):
            if "define" in line:
                problem_file.write(line + "\n")
                continue

            problem_file.write(line.lower() + "\n")


def main():
    output_directory = sys.argv[1]
    if sys.argv[2] == "numeric":
        generate_numeric_problems(Path(output_directory))

    elif sys.argv[2] == "strips":
        generate_strips_problems(Path(output_directory))


if __name__ == "__main__":
    main()
