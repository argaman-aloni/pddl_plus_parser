# To change this license    header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
# !/usr/bin/python3
import argparse
import itertools
import random
from enum import Enum
from pathlib import Path

import networkx as nx

from .common import get_problem_template

TEMPLATE_FILE_PATH = Path("farmland_template.pddl")


class GraphGeneratorTypes(Enum):
    star = 1
    strogaz = 2


def generate_adjacent_graph(graph_generator: GraphGeneratorTypes, num_farms: int) -> nx.Graph:
    """

    :param graph_generator:
    :param num_farms:
    :return:
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
    """

    :param instance_name:
    :param num_farms:
    :param num_units:
    :param graph_generator:
    :return:
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
    """

    :return:
    """
    parser = argparse.ArgumentParser(description="Generate farmland planning instance")
    parser.add_argument("--random_seed", required=False, help="Set RNG seed", default="1229")
    parser.add_argument("--num_farms", required=True, help="Number of farms")
    parser.add_argument("--num_units", required=True, help="Maximum Number of Units")
    parser.add_argument("--graph_generator", required=False,
                        help="Graph Generator between star (default) or strogatz or ladder",
                        default=GraphGeneratorTypes.star)

    args = parser.parse_args()
    args.random_seed = int(args.random_seed)

    if args.random_seed is not None:
        random.seed(args.random_seed)
        print(";; Setting seed to {0}".format(args.random_seed))

    return args


def generate_multiple_problems(min_farms, max_farms, min_num_units, max_num_units):
    farms_range = [i for i in range(min_farms, max_farms + 1)]
    units_range = [i for i in range(min_num_units, max_num_units + 1)]
    for num_farms, num_units in itertools.product(farms_range, units_range):
        with open(f"/sise/home/mordocha/numeric_planning/domains/farmland/pfile{num_farms}_{num_units}.pddl",
                  "wt") as problem_file:
            problem_file.write(generate_instance(f"instance_{num_farms}_{num_units}", num_farms, num_units,
                                                 GraphGeneratorTypes.star))

        # print(generate_instance(f"instance_{num_farms}_{num_units}", num_farms, num_units,
        # GraphGeneratorTypes.star))
        #     'instance_' + str(args.num_farms) + '_' + str(args.num_units) + '_' + str(args.random_seed) + '_' + str(
        #         args.graph_generator), int(args.num_farms), int(args.num_units), args.graph_generator))


def main():
    generate_multiple_problems(10, 15, 10, 20)
    # args = parse_arguments()
    # generate_instance(
    #     'instance_' + str(args.num_farms) + '_' + str(args.num_units) + '_' + str(args.random_seed) + '_' + str(
    #         args.graph_generator), int(args.num_farms), int(args.num_units), args.graph_generator)


if __name__ == '__main__':
    main()
