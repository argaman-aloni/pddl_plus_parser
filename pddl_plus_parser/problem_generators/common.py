import string
from pathlib import Path


def get_problem_template(template_file_path: Path) -> string.Template:
    """Extract the template object from the template file.

    :return: the template object.
    """
    with open(template_file_path, "rt") as template_file:
        text = template_file.read()
        return string.Template(text)
