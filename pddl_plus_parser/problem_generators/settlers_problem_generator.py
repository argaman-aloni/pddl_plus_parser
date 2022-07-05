import enum
import random
import sys
from collections import OrderedDict
from queue import Queue


class typeStatus(enum.Enum):
    OFF = 0
    ON = 1


typing = typeStatus
st = str()

class probTypes(enum.Enum):
    STRIPS = 0
    NUMERIC = 1
    SIMPLETIME = 2
    TIMED = 3
    COMPLEX = 4
    HARDNUMERIC = 5


probType = probTypes

def rnd(limit=-1):
    if limit == -1:
        return float(random.random())
    return int(limit * random.random())

class ProblemObject:
    class OutStatus(enum.Enum):
        OBJECT = 0
        INIT = 1
        GOAL = 2
    def object(self):
        raise NotImplementedError
    def init(self):
        raise NotImplementedError
    def goal(self):
        raise NotImplementedError
    def write(self):
        global outStatus
        if outStatus == ProblemObject.OutStatus.OBJECT:
            self.object()
        elif outStatus == ProblemObject.OutStatus.INIT:
            self.init()
        elif outStatus == ProblemObject.OutStatus.GOAL:
            self.goal()
    @classmethod
    def Objects(self):
        global outStatus
        outStatus = ProblemObject.OutStatus.OBJECT
    @classmethod
    def Inits(self):
        global outStatus
        outStatus = ProblemObject.OutStatus.INIT
    @classmethod
    def Goals(self):
        global outStatus
        outStatus = ProblemObject.OutStatus.GOAL
    
outStatus = ProblemObject.OutStatus.OBJECT

class IOManipulator(object):
    def __init__(self, function=None):
        self.function = function
    def do(self, output):
        self.function(output)
def do_endl(stream):
    stream.output.write('\n')
endl = IOManipulator(do_endl)

class OStream(object):
    def __init__(self, output=None):
        if output is None:
            output = sys.stdout
        self.output = output
        self.format = '%s'
    def __lshift__(self, thing):
        if isinstance(thing, IOManipulator):
            self.output.write(thing)
            return OStream()
        else:
            self.output.write(self.format % thing)
            self.format = '%s'
        return OStream()


seaZones = [set() for _ in range(4)]

id = 0

class Place(ProblemObject):
	
    def __init__(self):
        global id
        self.__place = id
        id += 1
        self.__mountain = rnd(10) < 3
        self.__woodland = rnd(10) < 6
        self.__metalliferous = rnd(10) < 2
        self.__bycoast = rnd(10) < 5
        self.__seaZone = rnd(4)
        global seaZones
        if self.__bycoast: 
            seaZones[self.__seaZone].add(self.__place)

    def makeMountain(self):
        self.__mountain = True
    def makeWoodland(self):
        self.__woodland = True
    def makeMetalliferous(self):
        self.__metalliferous = True

    def object(self):
        global typing
        global st
        st += f"\tlocation{self.__place}"
        if typing == typeStatus.ON:
            st += " - place"
        st += "\n"
    def init(self):
        global typing
        global st
        if typing == typeStatus.OFF:
            st += f"\t(place location{self.__place})\n"
        if self.__mountain:
            st += f"\t(mountain location{self.__place})\n"
        if self.__woodland:
            st += f"\t(woodland location{self.__place})\n"
        if self.__bycoast:
            st += f"\t(by-coast location{self.__place})\n"
        if self.__metalliferous:
            st += f"\t(metalliferous location{self.__place})\n"
        st += f"\t(= (housing location{self.__place}) 0)\n" + \
            f"\t(= (available wood location{self.__place}) 0)\n" + \
            f"\t(= (available timber location{self.__place}) 0)\n" + \
            f"\t(= (available ore location{self.__place}) 0)\n" + \
            f"\t(= (available stone location{self.__place}) 0)\n" + \
            f"\t(= (available iron location{self.__place}) 0)\n" + \
            f"\t(= (available coal location{self.__place}) 0)\n"
    def goal(self):
        pass
    def __str__(self):
        return st


class Goal(ProblemObject):
    def __del__(self):
        pass
    def object(self):
        raise NotImplementedError
    def init(self):
        raise NotImplementedError

def random_select(s):
    i = rnd(len(s))
    for val in s:
        while i > 0:
            i-=1
        return val
    return val

links = set()

class RailLink(Goal):
    def __init__(self, g, nlocs, length):
        self.start = rnd(nlocs)
        self.__locs = list()
        self.__locs.append(self.start)
        for i in range(length):
            if not g[self.start]: return # graph g int -> set
            self.start = random_select(g[self.start])
            if self.__locs[len(self.__locs) - 1] != self.start:
                self.__locs.append(self.start)
    def goal(self):
        global st
        global links
        for i in range(len(self.__locs) - 1):
            if (self.__locs[i], self.__locs[i+1]) not in links:
                st += f"\t(connected-by-rail location{self.__locs[i]} location{self.__locs[i+1]})\n"
                links.add((self.__locs[i], self.__locs[i+1]))
    def __repr__(self):
        return st

allBuildings = set()
numBuildings = 3
buildingName = ["coal-stack", "sawmill", "ironworks"]

class Building(Goal):
    def __init__(self, nlocs):
        global allBuildings
        global numBuildings
        global buildingName
        self.__building = rnd(numBuildings)
        self.__loc = rnd(nlocs) 
        while self.__loc < nlocs:
            while self in allBuildings and self.__building < numBuildings:
                self.__building+=1
                if self.__building < numBuildings:
                    break
            self.__loc+=1
            self.__building = 0
        allBuildings.add(self)
    def __hash__(self):
        return hash((self.__building, self.__loc))
    def __eq__(self, b):
        return self.__building == b.__building and self.__loc == b.__loc
    def __lt__(self, b):
        return self.__loc < b.loc or (self.__loc == b.loc and self.__building < b.building)
    def goal(self):
        global buildingName
        global st
        st += f"\t(has-{buildingName[self.__building]} location{self.__loc})\n"
    def __repr__(self):
        return st

places = set()

class Housing(Goal):
    def __init__(self, nlocs):
        global places
        if not places:
            for i in range(nlocs):
                places.add(i)
        self.__place = random_select(places)
        self.__quantity = rnd(2) + 1
        places.remove(self.__place)
    def goal(self):
        global st
        st += f"\t(>= (housing location{self.__place}) {self.__quantity})\n"
    def __repr__(self):
        return st


class Map(ProblemObject):
    def __explore(self, g, start, reached):
        togo = Queue()
        togo.put(start)
        reached.add(start) #set
        while not togo.empty():
            loc = togo.get()
            for i in g[loc]:
                if i not in reached:
                    togo.put(i)
                    reached.add(i)

    def __connect(self, g): 
        reached = set()
        start = rnd(self.__places)
        self.__explore(g, start, reached)
        while len(reached) != self.__places:
            next = int()
            for i in range(self.__places):
                if i not in reached:
                    next = i
                    break
            g[start].add(next)
            start = next
            self.__explore(g, start, reached)
    def __init__(self, s, ngs): 
        self.__places = s
        self.__Places = list()
        self.__road = OrderedDict()
        self.__goals = list()
        for _ in range(s):
            self.__Places.append(Place())
            for _ in range(4):
                f = rnd(s)
                t = rnd(s)
                if t not in self.__road:
                    self.__road[t] = set()
                if f not in self.__road[t]:
                    if f not in self.__road:
                        self.__road[f] = set()
                    self.__road[f].add(t)
        self.__connect(self.__road)
        self.__Places[rnd(self.__places)].makeMountain()
        self.__Places[rnd(self.__places)].makeWoodland()
        self.__Places[rnd(self.__places)].makeMetalliferous()

        for _ in range(ngs):
            if rnd(10) < 3:
                self.__goals.append(RailLink(self.__road, self.__places, int(ngs/3)))
            else:
                if rnd(10) < 3:
                    self.__goals.append(Housing(self.__places))
                else:
                    self.__goals.append(Building(self.__places))
    def __del__(self):
        for i in self.__goals:
            del i

    def object(self):
        global st
        for p in self.__Places:
            p.object()
    def init(self):
        global seaZones
        global typing
        global st
        for p in self.__Places:
            p.init()
        if typing == typeStatus.OFF:
            st += "\t(resource iron)\n\t(resource wood)\n\t(resource timber)\n\t(resource ore)\n\t(resource stone)\n\t(resource coal)\n"
		
        for k, v in self.__road.items():
            for ele in v:
                if k == ele:
                    continue
                if ele in self.__road:
                    if ele in self.__road:
                        if k in self.__road[ele]:
                            continue

                st += f"\t(connected-by-land location{k} location{ele})\n\t(connected-by-land location{ele} location{k})\n"
        for i in range(4):
            for idx, s in enumerate(seaZones[i]):
                for t in [t1 for index, t1 in enumerate(seaZones[i]) if index > idx]:
                    st += f"\t(connected-by-sea location{s} location{t})\n\t(connected-by-sea location{t} location{s})\n"

    def goal(self):
        global st
        for i in self.__goals:
            i.goal()
    def __repr__(self):
        return st

ID = 0

class Vehicle(ProblemObject):
    def __init__(self):
        global ID
        self.__vnum = ID + 1
        ID +=1
    def object(self):
        global st
        global typing
        st += f"\tvehicle{self.__vnum}"
        if typing == typeStatus.ON:
            st += " - vehicle"
        st += "\n"
    def init(self):
        global typing
        global st
        if typing == typeStatus.OFF:
            st += f"\t(vehicle vehicle{self.__vnum})\n"
        st += f"\t(potential vehicle{self.__vnum})\n"
    def goal(self):
        pass
    def __repr__(self):
        return st

def main(argc, argv):
    global typing
    global probType
    typing = typeStatus.ON;
    probType = probTypes.STRIPS;
    global o
    global st
    if argc < 4:
        print("Usage: settlers [-u] <seed> #<locations> #<goals> #<vehicles>\n\n\tThe number of vehicles is the number of \"potential\" vehicles.\n\n\t-u: Untyped\n\n")
        exit(0)
    argv = argv[1:]
    argc -= 1
    if argv[0][0] == '-':
        if argv[0][1] == 'u': 
            typing = typeStatus.OFF
        argv = argv[1:]
        argc -= 1
    random.seed(int(argv[0]))
    p = Map(int(argv[1]),int(argv[2]))
    carts = list()
    for _ in range(int(argv[3])):
        carts.append(Vehicle())
    print("(define (problem settlers)\n(:domain civ)\n(:objects\n",end='')
    p.write()
    o << st
    st = ''
    for c in carts:
        c.write()
        o << st
        st = ''
    print(")\n(:init\n\t(= (resource-use) 0)\n\t(= (labour) 0)\n\t(= (pollution) 0)\n",end='')
    ProblemObject.Inits()
    p.write()
    o << st
    st = ''
    for c in carts:
        c.write()
        o << st
        st = ''
    print(")\n(:goal (and\n",end='')
    ProblemObject.Goals()
    p.write()
    o << st
    st = ''
    print(f"\t)\n)\n\n(:metric minimize (+ (+ (* {rnd(4)} (pollution)) (* {rnd(4)} (resource-use))) (* {rnd(4)} (labour))))\n)\n",end='')

o = OStream()

if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    main(argc, argv)

