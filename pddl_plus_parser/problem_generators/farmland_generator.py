# To change this license    header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
# !/usr/bin/python3
import argparse
import itertools
import random
from enum import Enum
from pathlib import Path
from typing import NoReturn

import networkx as nx

from pddl_plus_parser.problem_generators import get_problem_template

TEMPLATE_FILE_PATH = Path("farmland_template.pddl")


class GraphGeneratorTypes(Enum):
    star = 1
    strogaz = 2


def generate_adjacent_graph(graph_generator: GraphGeneratorTypes, num_farms: int) -> nx.Graph:
    """Generates the graph of farms where there are adjacent farms represented in a graph.

    :param graph_generator: the type of graph generator to use.
    :param num_farms: the number of farms in the graph.
    :return: the graph of farms.
    """
    if graph_generator == GraphGeneratorTypes.star:
        G = nx.star_graph(num_farms - 1)

    elif graph_generator == GraphGeneratorTypes.strogaz:
        G = nx.connected_watts_strogatz_graph(num_farms, k=min(2, num_farms - 1), tries=10000, p=0.5)

    else:
        G = nx.ladder_graph(num_farms // 2)
    return G


def generate_instance(
        instance_name: str, num_farms: int, num_units: int, graph_generator: GraphGeneratorTypes) -> str:
    """Generates the farmland planning problem instance.

    :param instance_name: the name of the problem instance.
    :param num_farms: the number of farms in the problem.
    :param num_units: the number of units in the problem.
    :param graph_generator: the type of generator to use to generate the adjacent graph.
    :return: the string representation of the problem instance.
    """
    template = get_problem_template(TEMPLATE_FILE_PATH)
    template_mapping = {"instance_name": instance_name, "domain_name": "farmland"}

    G = generate_adjacent_graph(graph_generator, num_farms)

    source = random.randint(0, num_farms - 1)
    farms_init_fluents = []
    farms_reward_bound = ["(>= "]
    farms_goal_fluents = []
    adjacents = []
    farms = " ".join([f"farm{i} " for i in range(num_farms)])
    for i in range(num_farms):
        weight_bound = "{0:.1f}".format(random.random() + 1.0) if i != source else 1.0
        init_fluent = f"(= (x farm{i}) {str(random.randint(0, 1))})\n\t\t" if i != source else \
            f"(= (x farm{i}) {num_units})\n\t\t"
        farms_init_fluents.append(init_fluent)
        farms_reward_bound.append(f"(+ (* {weight_bound} (x farm{i}))")
        farms_goal_fluents.append(f"(>= (x farm{i}) 1)\n\t\t\t")

        for element in G[i]:
            adjacents.append(f"(adj farm{i} farm{str(element)})\n\t\t")

    farms_reward_bound.append(" 0")
    farms_reward_bound.append(")" * num_farms)
    farms_reward_bound.append(f" {str(num_units * 1.4)})")

    template_mapping['farm_name_list'] = farms
    template_mapping['farm_init_allocation'] = "".join(farms_init_fluents)
    template_mapping['farm_connections'] = "".join(adjacents)
    template_mapping['farm_final_requirement'] = "".join(farms_goal_fluents)
    template_mapping['overall_reward_bound'] = "".join(farms_reward_bound)

    return template.substitute(template_mapping)


def parse_arguments() -> argparse.Namespace:
    """Parses the command line arguments."""
    parser = argparse.ArgumentParser(description="Generate farmland planning instance")
    parser.add_argument("--min_farms", required=True, help="The minimal number of farms possible in a planning problem")
    parser.add_argument("--max_farms", required=True, help="The maximal number of farms possible in a planning problem")
    parser.add_argument("--min_num_units", required=True, help="Minimal number of units")
    parser.add_argument("--max_num_units", required=True, help="Maximal number of units")
    parser.add_argument("--output_folder", required=True, help="The path to the output folder")
    parser.add_argument("--graph_generator", required=False,
                        help="Graph Generator between star (default) or strogatz or ladder",
                        default=GraphGeneratorTypes.star)
    return parser.parse_args()


def generate_multiple_problems(min_farms: int, max_farms: int, min_num_units: int, max_num_units: int,
                               output_folder: Path,
                               graph_generator: GraphGeneratorTypes = GraphGeneratorTypes.star,
                               total_num_problems: int = 200) -> NoReturn:
    """Generate multiple problems based on the input arguments.

    :param min_farms: the minimal number of farms possible in a planning problem.
    :param max_farms: the maximal number of farms possible in a planning problem.
    :param min_num_units: the minimal number of units.
    :param max_num_units: the maximal number of units.
    :param output_folder: the path to the output folder where the planning problems will be saved.
    :param graph_generator: the type of graph generator to use.
    """
    farms_range = [i for i in range(min_farms, max_farms + 1)]
    units_range = [i for i in range(min_num_units, max_num_units + 1)]
    for i in range(total_num_problems):
        num_farms = random.choice(farms_range)
        num_units = random.choice(units_range)
        print(f"Generating problem with {num_farms} farms and {num_units} units")
        with open(output_folder / f"pfile{i}.pddl", "wt") as problem_file:
            problem_file.write(generate_instance(f"instance_{num_farms}_{num_units}", num_farms, num_units,
                                                 graph_generator))


def main():
    args = parse_arguments()
    generate_multiple_problems(min_farms=int(args.min_farms),
                               max_farms=int(args.max_farms),
                               min_num_units=int(args.min_num_units),
                               max_num_units=int(args.max_num_units),
                               output_folder=Path(args.output_folder),
                               graph_generator=args.graph_generator)


if __name__ == '__main__':
    main()
