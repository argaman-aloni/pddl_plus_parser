"""Problem generator for the zeno-travel domain."""
import argparse
import random
from enum import Enum
from typing import List, Optional, Any, Dict

import numpy

MAX_RAND = 10 ** 6
random.seed(42)


class AllowedDomainTypes(Enum):
    """Enum for the allowed domain types."""
    STRIPS = 1
    NUMERIC = 2


class CityMap:
    """Defines the map of the problem."""
    num_locations: int
    num_distances: int
    map: numpy.ndarray
    domain_type: AllowedDomainTypes

    def __init__(self, num_locations: int, num_distances: int, domain_type: AllowedDomainTypes):
        self.domain_type = domain_type
        self.num_locations = num_locations
        self.num_distances = num_distances
        self.map = numpy.zeros((num_locations, num_distances))
        for i in range(num_locations):
            for j in range(i + 1, num_locations):
                self.map[i][j] = random.randint(0, num_distances // 2) + num_distances / 2
                self.map[j][i] = self.map[i][j]

    def define_city_map(self) -> List[str]:
        """

        :return:
        """
        map_str = []
        if self.domain_type == AllowedDomainTypes.NUMERIC:
            for i in range(self.num_locations):
                for j in range(self.num_locations):
                    map_str.append(f"\t(= (distance city{i} city{j}) {int(self.map[i][j])})")

        return map_str

    def define_city_objects(self) -> List[str]:
        """

        :return:
        """
        return [f"\tcity{i} - city" for i in range(self.num_locations)]


class Locatable:
    location: int
    destination: int
    interesting: bool
    id: int

    def __init__(self, num_location: int):
        self.location = random.randint(0, num_location)
        self.destination = random.randint(0, num_location)
        self.interesting = True


class Airplane(Locatable):
    """Defines the airplane."""
    id: int
    airplane_data: Dict[str, Any]
    domain_type: AllowedDomainTypes
    num_planes: int

    def __init__(self, id: int, num_locations: int, num_distances: int, num_planes: int,
                 domain_type: AllowedDomainTypes):
        super(Airplane, self).__init__(num_locations)
        self.id = id
        self.num_planes = num_planes
        slow_burn_rate = random.randint(1, 5)
        slow_speed = random.randint(0, 100) + 100
        self.airplane_data = {
            "slow_burn_rate": random.randint(1, 5),
            # "slow_speed": random.randint(0, 100) + 100,
            "fuel": random.randint(0, slow_burn_rate * num_distances),
            "capacity": random.randint(0, int(2.1 * random.random()) * slow_burn_rate * num_distances),
            # "fast_speed": random.randint(0, int(1.0 + random.random() * 2) * slow_speed),
            "fast_burn_rate": random.randint(0, int(2.0 + random.random() * 2) * slow_burn_rate),
            "refuel_rate": 2 * random.randint(0, slow_burn_rate * num_distances),
            "zoom_limit": 1 + random.randint(0, 10)
        }
        self.domain_type = domain_type
        if random.randint(0, 10) < 7:
            self.interesting = False

    def define_airplane_object(self) -> str:
        """

        :return:
        """
        return f"\tplane{self.id} - aircraft"

    def define_airplane_map(self) -> List[str]:
        """"""
        airplane_map = [f"\t(at plane{self.id} city{self.location})"]
        if self.domain_type == AllowedDomainTypes.NUMERIC:
            for field_name, field_value in self.airplane_data.items():
                airplane_map.append(f"\t(= ({field_name} plane{self.id}) {field_value})")

            airplane_map.append(f"\t(= (onboard plane{self.id}) 0)")

        return airplane_map

    def define_airplane_goal(self) -> Optional[str]:
        """

        :return:
        """
        if self.interesting:
            return f"\t(at plane{self.id} city{self.destination})"

        return None


class Person(Locatable):
    """Defines the person."""
    id: int
    person_data: Dict[str, Any]
    domain_type: AllowedDomainTypes
    num_people: int

    def __init__(self, id: int, num_people: int, domain_type: AllowedDomainTypes):
        super(Person, self).__init__(num_people)
        self.id = id
        self.num_people = num_people
        self.domain_type = domain_type
        if random.randint(0, 100) < 3:
            self.interesting = False

    def define_person_object(self) -> str:
        """

        :return:
        """
        return f"\tperson{self.id} - person"

    def define_person_map(self) -> str:
        """"""
        return f"\t(at person{self.id} city{self.location})"

    def define_person_goal(self) -> Optional[str]:
        """

        :return:
        """
        if self.interesting:
            return f"\t(at person{self.id} city{self.destination})"

        return None


class ZenoTravelGenerator:
    """Problem generator for the zeno-travel domain."""

    num_people: int
    num_planes: int
    people: List[Person]
    airplanes: List[Airplane]
    cities_map: CityMap
    domain_type: AllowedDomainTypes

    def __init__(self, domain_type: AllowedDomainTypes, number_people: int, number_airplanes: int, num_locations: int):
        """Initialize the generator."""
        self.num_people = number_people
        self.num_planes = number_airplanes
        self.domain_type = domain_type
        self.cities_map = CityMap(num_locations=num_locations, num_distances=100, domain_type=domain_type)
        self.people = [Person(id=index, num_people=number_people, domain_type=domain_type) for index in
                       range(number_people)]
        self.airplanes = [Airplane(id=index, num_locations=num_locations, num_distances=100, domain_type=domain_type,
                                   num_planes=number_airplanes) for index in range(number_airplanes)]

    def generate_problem(self) -> str:
        """Generate the problem."""
        problem = [f"(define (problem ZTRAVEL-{self.num_people}-{self.num_planes})",
                   "\t(:domain zeno-travel)", "(:objects"]
        for person in self.people:
            problem.append(person.define_person_object())

        for airplane in self.airplanes:
            problem.append(airplane.define_airplane_object())

        problem.extend(self.cities_map.define_city_objects())
        problem.append("\t)\n(:init")
        if self.domain_type == AllowedDomainTypes.STRIPS:
            for i in range(7):
                problem.append(f"\tfl{i} - flevel")

        for airplane in self.airplanes:
            problem.extend(airplane.define_airplane_map())

        for person in self.people:
            problem.append(person.define_person_map())

        problem.extend(self.cities_map.define_city_map())
        if self.domain_type == AllowedDomainTypes.NUMERIC:
            problem.append("\t(= (total-fuel-used) 0)")

        problem.append(")\n(:goal (and")
        for airplane in self.airplanes:
            goal = airplane.define_airplane_goal()
            if goal is not None:
                problem.append(goal)

        for person in self.people:
            goal = person.define_person_goal()
            if goal is not None:
                problem.append(goal)

        problem.append("\t))\n")
        if self.domain_type == AllowedDomainTypes.NUMERIC:
            # define the metric function
            value1 = random.randint(0, 5) + 1
            value2 = random.randint(0, 5) + 1
            problem.append(f"(:metric minimize (+ (* {value2} (total-time))  (* {value1} (total-fuel-used))))")

        problem.append(")")

        return "\n".join(problem)


def parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description="Generate a single zenotravel planning problem.")
    parser.add_argument("--number_people", required=True, help="The number of people in the problem.", type=int)
    parser.add_argument("--number_airplanes", required=True, help="The number of airplanes in the problem.", type=int)
    parser.add_argument("--num_locations", required=True, help="The number of locations in the problem.", type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    generator = ZenoTravelGenerator(domain_type=AllowedDomainTypes.NUMERIC,
                                    number_people=args.number_people,
                                    number_airplanes=args.number_airplanes,
                                    num_locations=args.num_locations)
    print(generator.generate_problem())
