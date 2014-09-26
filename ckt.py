
import re

def parseCkt(cktfile):

    lib = {}

    fh = open(cktfile, "rt")

    with open(cktfile, "rt") as fh:
        for line in fh:

            # strip trailing and leading space chars
            line.strip()

            # skip empty line
            if line.isspace():
                continue

            # print(line, end='')
            if re.match("^ckt", line):
                # print(line)
                a = line.split()
                token, cellName = a[0:2]
                currentCell = {}
                currentCell['instances'] = []
                lib[cellName] = currentCell

                intf = []
                currentCell['interface'] = intf
                for x in a[2:]:
                    intf.append(x)

            if re.match("^i", line):
                currentCell['instances'].append(line.split())

            if re.match("^q", line):
                currentCell['instances'].append(line.split())

    print(lib['top'])

    return lib


if __name__ == "__main__":
    lib = parseCkt("netlist.ckt")
    pass