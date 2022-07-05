import string
from pathlib import Path


def get_problem_template(template_file_path: Path) -> string.Template:
    """

    :return:
    """
    with open(template_file_path, "rt") as template_file:
        text = template_file.read()
        return string.Template(text)
