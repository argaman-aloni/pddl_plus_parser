import enum
import random
import sys


class typeStatus(enum.Enum):
    OFF = 0
    ON = 1


typing = typeStatus


def rnd(limit):
    return 1 + int(limit * random.random())


def rnd2(limit):
    return limit / 2 + rnd(limit / 2)


def rnd3(locs, limit):
    return int(locs * (1.0 + ((limit - 1) * random.random())))


class locatable:
    def __init__(self, locs=-1):
        if locs == -1:
            self.location = 0
        else:
            self.location = rnd(locs)


class Truck(locatable):
    def __init__(self, locs, maxc):
        locatable.__init__(self, locs)
        self.capacity = rnd2(maxc)
        self.speed = rnd(10)


class Pallet(locatable):
    def __init__(self, locs):
        locatable.__init__(self, locs)
        self.topcrate = 0
        self.dtopcrate = 0

maxWeight = 0

class Crate(locatable):

    def __init__(self, ps, maxw):
        locatable.__init__(self)
        self.pallet = rnd(ps)
        self.weight = rnd(maxw)
        self.dpallet = 0
        self.dsurface = 0
        self.surface = int()
        global maxWeight
        maxWeight = self.weight if self.weight > maxWeight else maxWeight

class Hoist(locatable):
    def __init__(self, locs):
        locatable.__init__(self, locs)
        self.powr = rnd(10)


class Map:
    def __init__(self, locs):
        self.distances = []
        for i in range(locs):
            self.distances.append(list())
            for j in range(locs):
                self.distances[i].append(rnd(10))


class DepotDescriptor:
    class ProblemType(enum.Enum):
        STRIPS = 0
        NUMERIC = 1
        SIMPLETIMED = 2
        TIMED = 3

    def __init__(self, dps, dsts, trks, plts, hsts, crts, tp=ProblemType.STRIPS, mxwt=0, mxcp=0):
        self.numDepots = dps
        self.numDistributors = dsts
        self.numTrucks = trks
        self.numPallets = plts
        self.numHoists = hsts
        self.numCrates = crts
        self.probtype = tp
        self.maxCapacity = mxcp
        self.maxWeight = mxwt


class Depot:
    def __init__(self, s, d, f):
        self.__seed = s
        self.__probtype = d.probtype
        random.seed(s)
        self.__numDepots = d.numDepots
        self.__numDistributors = d.numDistributors
        self.numTrucks = d.numTrucks
        self.locs = self.__numDepots + self.__numDistributors
        self.__m = Map(self.locs)
        self.numPallets = max(d.numPallets, self.locs)
        self.numHoists = max(d.numHoists, self.locs)
        self.__trucks = []
        self.__pallets = []
        self.__hoists = []
        self.__crates = []
        self.file = f
        for i in range(self.numTrucks):
            t = Truck(self.locs, d.maxCapacity)
            self.__trucks.append(t)
        for i in range(self.numHoists):
            h = Hoist(self.locs)
            if i < self.locs:
                h.location = i + 1
            self.__hoists.append(h)
        for i in range(self.numPallets):
            p = Pallet(self.locs)
            if i < self.locs:
                p.location = i + 1
            self.__pallets.append(p)
        for i in range(d.numCrates):
            c = Crate(self.numPallets, d.maxWeight)
            c.location = self.__pallets[c.pallet - 1].location
            c.surface = self.__pallets[c.pallet - 1].topcrate
            self.__pallets[c.pallet - 1].topcrate = i + 1
            self.__crates.append(c)
        for i in range(2 * d.numCrates):
            c = rnd(d.numCrates) - 1
            if self.__crates[c].dpallet:
                continue
            self.__crates[c].dpallet = rnd(self.numPallets)
            self.__crates[c].dsurface = self.__pallets[self.__crates[c].dpallet - 1].dtopcrate
            self.__pallets[self.__crates[c].dpallet - 1].dtopcrate = c + 1

    def __location(self, i):
        if type(i) != int:
            i = i.location - 1
        if i < self.__numDepots:
            self.file.write(f"depot{i}")
        else:
            self.file.write(f"distributor{i - self.__numDepots}")


    def __del__(self):
        del self.__m

    def write(self):  
        global maxWeight
        self.file.write(
            f"(define (problem depotprob{self.__seed}) (:domain Depot)\n(:objects\n\t")
        for i in range(self.__numDepots):
            self.file.write(f"depot{i} ")
        if typing == typeStatus.ON:
            self.file.write("- Depot\n\t")
        for i in range(self.__numDistributors):
            self.file.write(f"distributor{i} ")
        if typing == typeStatus.ON:
            self.file.write("- Distributor\n\t")
        for i in range(len(self.__trucks)):
            self.file.write(f"truck{i} ")
        if typing == typeStatus.ON:
            self.file.write("- Truck\n\t")
        for i in range(len(self.__pallets)):
            self.file.write(f"pallet{i} ")
        if typing == typeStatus.ON:
            self.file.write("- Pallet\n\t")
        for i in range(len(self.__crates)):
            self.file.write(f"crate{i} ")
        if typing == typeStatus.ON:
            self.file.write("- Crate\n\t")
        for i in range(len(self.__hoists)):
            self.file.write(f"hoist{i} ")
        if typing == typeStatus.ON:
            self.file.write("- Hoist")
        self.file.write(")\n(:init\n")
        for i in range(len(self.__pallets)):
            if typing == typeStatus.OFF:
                self.file.write(f"\t(pallet pallet{i})\n")
                self.file.write(f"\t(surface pallet{i})\n")
            self.file.write(f"\t(at pallet{i} ")
            self.__location(self.__pallets[i])
            self.file.write(")\n\t(clear ")
            if self.__pallets[i].topcrate:
                self.file.write(
                    f"crate{self.__pallets[i].topcrate - 1})\n")
            else:
                self.file.write(f"pallet{i})\n")
        for i in range(len(self.__trucks)):
            if typing == typeStatus.OFF:
                self.file.write(f"\t(truck truck{i})\n")
            self.file.write(f"\t(at truck{i} ")
            self.__location(self.__trucks[i])
            self.file.write(")\n")
            if self.__probtype == DepotDescriptor.ProblemType.TIMED:
                self.file.write(
                    f"\t(= (speed truck{i}) {self.__trucks[i].speed})\n")
            if self.__probtype == DepotDescriptor.ProblemType.NUMERIC:
                self.file.write(
                    f"\t(= (current_load truck{i}) 0)\n\t(= (load_limit truck{i}) ")
                if ((2 * self.__trucks[i].capacity) < maxWeight) or i == 0:
                    self.file.write(
                        f"{str(self.__trucks[i].capacity + maxWeight)})\n")
                else:
                    self.file.write(
                        f"{str(self.__trucks[i].capacity)})\n")
        for i in range(len(self.__hoists)):
            if typing == typeStatus.OFF:
                self.file.write(f"\t(hoist hoist{i})\n")
            self.file.write(f"\t(at hoist{i} ")
            self.__location(self.__hoists[i])
            self.file.write(f")\n\t(available hoist{i})\n")
            if self.__probtype == DepotDescriptor.ProblemType.TIMED:
                self.file.write(
                    f"\t(= (power hoist{i}) {self.__hoists[i].powr})\n")
        for i in range(len(self.__crates)):
            if typing == typeStatus.OFF:
                self.file.write(f"\t(crate crate{i})\n")
                self.file.write(f"\t(surface crate{i})\n")
            self.file.write(f"\t(at crate{i} ")
            self.__location(self.__crates[i])
            self.file.write(f")\n\t(on crate{i} ")
            if self.__crates[i].surface:
                self.file.write(
                    f"crate{self.__crates[i].surface - 1})\n")
            else:
                self.file.write(
                    f"pallet{self.__crates[i].pallet - 1})\n")
            if self.__probtype == DepotDescriptor.ProblemType.NUMERIC or self.__probtype == DepotDescriptor.ProblemType.TIMED:
                self.file.write(
                    f"\t(= (weight crate{i}) {self.__crates[i].weight})\n")
        if typing == typeStatus.OFF:
            for i in range(self.__numDepots + self.__numDistributors):
                self.file.write("\t(place ")
                self.__location(i)
                self.file.write(")\n")
        if self.__probtype == DepotDescriptor.ProblemType.TIMED:
            for i in range(len(self.__m.distances)):
                for j in range(len(self.__m.distances[i])):
                    self.file.write("\t(= (distance ")
                    self.__location(i)
                    self.file.write(" ")
                    self.__location(j)
                    self.file.write(") ")
                    if j != i:
                        self.file.write(
                            f"{self.__m.distances[i][j]})\n")
                    else:
                        self.file.write("0)\n")

        if self.__probtype == DepotDescriptor.ProblemType.NUMERIC:
            self.file.write("\t(= (fuel-cost) 0)\n")

        self.file.write(")\n\n(:goal (and\n")
        for i in range(len(self.__crates)):
            if self.__crates[i].dpallet:
                if self.__crates[i].dsurface:
                    self.file.write(
                        f"\t\t(on crate{i} crate{self.__crates[i].dsurface - 1})\n")
                else:
                    self.file.write(
                        f"\t\t(on crate{i} pallet{self.__crates[i].dpallet - 1})\n")
        self.file.write("\t)\n)")
        if self.__probtype != DepotDescriptor.ProblemType.STRIPS and self.__probtype != DepotDescriptor.ProblemType.NUMERIC:
            self.file.write("\n\n(:metric minimize (total-time))")
        if self.__probtype == DepotDescriptor.ProblemType.NUMERIC:
            if rnd(10) < 4:
                self.file.write("\n\n(:metric minimize (fuel-cost))")
            else:
                self.file.write("\n\n(:metric minimize (total-time))")
        self.file.write(")\n")


def usage():
    print("Usage: gdep <seed> [-s|-t|-n|-w <weight>|-c <capacity>|-f <filename>]\n\t\t<#depots> <#distributors> <#trucks> <#pallets> <#hoists> <#crates>\n\n\tOptions:\n\tu: untyped\n\ts: simple-time\n\tt: time\n\tn: numeric\n\tw: provide maximum weight for crates\n\tc: maximum capacity for trucks\n\tf: optional file for output\n\n\tAll numbers are integers.\n\n")
    exit(0)


def commandLine(seed, filename, argc, argv):
    probtype = DepotDescriptor.ProblemType.STRIPS
    global typing
    wgt = 1
    cap = 1
    nxt = 0
    val = [0 for _ in range(6)]

    if argc <= 0:
        usage()

    seed = int(argv[0])
    argc -= 1
    argv = argv[1:]

    while argc > 0:
        if argv[0][0] == '-':
            o = argv[0][1]
            if o == 't':
                probtype = DepotDescriptor.ProblemType.TIMED
            elif o == 's':
                probtype = DepotDescriptor.ProblemType.SIMPLETIMED
            elif o == 'n':
                probtype = DepotDescriptor.ProblemType.NUMERIC
            elif o == 'u':
                typing = typeStatus.OFF
            else:
                argc -= 1
                argv = argv[1:]
                if argc < 0:
                    usage()
                if o == 'w':
                    wgt = int(argv[0])
                elif o == 'c':
                    cap = int(argv[0])
                elif o == 'f':
                    filename = argv[0]
                else:
                    usage()
            argc -= 1
            argv = argv[1:]
        else:
            if nxt == 6:
                usage()
            val[nxt] = int(argv[0])
            nxt += 1
            argv = argv[1:]
            argc -= 1
    if nxt < 6:
        usage()
    return DepotDescriptor(val[0], val[1], val[2], val[3], val[4], val[5], probtype, wgt, cap), filename, seed


def main(argc, argv):
    global typing
    typing = typeStatus.ON
    seed = int()
    filename = ''
    d, filename, seed = commandLine(seed, filename, argc - 1, argv[1:])
    if filename != '':
        f = open(filename, 'w')
        dp = Depot(seed, d, f)
        dp.write()
        f.close()


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    main(argc, argv)
