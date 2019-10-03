#regrade

import copy
import math
import re
import sys


class Vertex:

    def __init__(self, x, y):
        self.x = float(x)

        self.y = float(y)

        self.id = -1

        self.intersect = False

    def __str__(self):
        return '  %s:\t(%.2f,%.2f)' % (self.id, self.x, self.y)

    def __hash__(self):
        return ('x:%s,y:%s' % (self.x, self.y)).__hash__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line:

    def __init__(self, v1, v2):
        self.start = v1

        self.end = v2

    def __str__(self):
        return '  <%s,%s>' % (self.start.id, self.end.id)

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return self.start != other.start or self.end != other.end


class Street:

    def __init__(self, name, vertex):

        self.name = name

        self.line = []

        self.vertex = []

        self.initLineAndVertex(vertex)

    def initLineAndVertex(self, vertex):

        if len(vertex) >= 2:

            for i in range(len(vertex) - 1):
                self.line.append(Line(vertex[i], vertex[i + 1]))

            self.vertex = vertex

        else:

            print("Error: a street must have 2 vertices or more!")

    def addPointToLine(self, line, vertex):

        if (line.start == vertex) or (line.end == vertex):
            if line.start == vertex:
                line.start.intersect = True
            if line.end == vertex:
                line.end.intersect = True
            return None

        newLine1 = Line(line.start, vertex)

        newLine2 = Line(vertex, line.end)

        newLine = []

        for i in range(len(self.line)):

            if self.line[i] != line:

                newLine.append(self.line[i])

            else:

                newLine.append(newLine1)

                newLine.append(newLine2)

        self.line = newLine

        newVertex = []

        for i in range(len(self.vertex)):

            newVertex.append(self.vertex[i])

            if self.vertex[i] == line.start:

                if newVertex.count(vertex) == 0:
                    newVertex.append(vertex)

        self.vertex = newVertex


class InterLine:

    def __init__(self, line):
        self.v1 = line.start

        self.v2 = line.end

        self.a = self.v1.y - self.v2.y

        self.b = self.v2.x - self.v1.x

        self.c = self.v1.x * self.v2.y - self.v1.y * self.v2.x


class Graph:

    def __init__(self):

        self.street = {}
        self.endVertex = {}
        self.edge = {}

    def addEndVertex(self, vertex):

        if not self.endVertex.has_key(vertex):
            if idList.has_key(vertex):
                vertex.id = (idList[vertex])
            else:
                vertex.id = (len(idList.keys()) + 1)
                idList[vertex] = vertex.id
            self.endVertex[vertex] = vertex

    def addEdge(self, edge):

        if not edge in self.edge:

            if edge.start != edge.end:
                self.edge[edge] = edge

    def addStreet(self, arg):

        # pattern = r'c \"(.+?)\"(( ?\(\-?\d+,\-?\d+\))+)\s*$'
        pattern = r'a\s+\"(.+?)\"(( ?\(\-?\d+,\-?\d+\))+)\s*$'

        match = re.match(pattern, arg)

        if match:

            streetName = match.group(1).upper()

            for c in str(streetName):
                if (not c.isalpha()) and (not c.isspace()):
                    print("Error: wrong format with street name!")
                    return

            if streetName in self.street:
                print("Error: street already exist!")
                return

            vertexList = re.compile(r'\((\-?\d+),(\-?\d+)\)').findall(str(match.group(2)).strip())

            vertex = []

            for p in vertexList:
                v = Vertex(int(p[0]), int(p[1]))

                vertex.append(v)

            self.street[streetName] = Street(streetName, vertex)

        else:

            print("Error: wrong input format!")

    def changeStreet(self, arg):

        # pattern = r'c \"(.+?)\"(( ?\(\-?\d+,\-?\d+\))+)\s*$'
        pattern = r'c\s+\"(.+?)\"(( ?\(\-?\d+,\-?\d+\))+)\s*$'

        match = re.match(pattern, arg)

        if match:

            streetName = match.group(1).upper()

            for c in str(streetName):
                if (not c.isalpha()) and (not c.isspace()):
                    print("Error: wrong format with street name!")
                    return

            if streetName in self.street:

                vertexList = re.compile(r'\((\-?\d+),(\-?\d+)\)').findall(str(match.group(2)).strip())

                vertex = []

                for p in vertexList:
                    v = Vertex(int(p[0]), int(p[1]))

                    vertex.append(v)

                self.street[streetName] = Street(streetName, vertex)

            else:

                print("Error: street doesn't exist!")

        else:

            print("Error: wrong input format!")

    def removeStreet(self, arg):

        pattern = r'r \"(.+?)\"'

        match = re.match(pattern, arg)

        if match:

            streetName = match.group(1).upper()

            for c in str(streetName):
                if (not c.isalpha()) and (not c.isspace()):
                    print("Error: wrong format with street name!")
                    return

            if streetName in self.street:

                del self.street[streetName]

            else:

                print("Error: street doesn't exist!")

        else:

            print("Error: wrong input format!")

    def initGraph(self):
        tempGraph = copy.deepcopy(self)
        streetName = tempGraph.street.keys()

        for i in range(len(streetName) - 1):
            for j in range(i + 1, len(streetName)):
                s1 = tempGraph.street[streetName[i]]
                s2 = tempGraph.street[streetName[j]]
                for s1l in s1.line:
                    for s2l in s2.line:
                        inter = calcIntersection(s1l, s2l)
                        cover = calcCover(s1l,s2l)
                        if inter:
                            inter.intersect = True
                            s1.addPointToLine(s1l, inter)
                            s2.addPointToLine(s2l, inter)
                        elif cover:
                            s1.addPointToLine(s1l, s2l.start)
                            s1.addPointToLine(s1l, s2l.end)
                            s2.addPointToLine(s1l, s1l.start)
                            s2.addPointToLine(s1l, s1l.end)


        for i in range(len(streetName)):
            st = tempGraph.street[streetName[i]]
            for j in range(len(st.vertex)):
                if st.vertex[j].intersect:
                    tempGraph.addEndVertex(st.vertex[j])

                    if j - 1 >= 0:
                        tempGraph.addEndVertex(st.vertex[j - 1])
                        if tempGraph.endVertex[st.vertex[j - 1]].id > tempGraph.endVertex[st.vertex[j]].id:
                            edge = Line(tempGraph.endVertex[st.vertex[j]], tempGraph.endVertex[st.vertex[j - 1]])
                        else:
                            edge = Line(tempGraph.endVertex[st.vertex[j - 1]], tempGraph.endVertex[st.vertex[j]])
                        tempGraph.addEdge(edge)

                    if j + 1 < len(st.vertex):
                        tempGraph.addEndVertex(st.vertex[j + 1])
                        if tempGraph.endVertex[st.vertex[j]].id > tempGraph.endVertex[st.vertex[j + 1]].id:
                            edge = Line(tempGraph.endVertex[st.vertex[j + 1]], tempGraph.endVertex[st.vertex[j]])
                        else:
                            edge = Line(tempGraph.endVertex[st.vertex[j]], tempGraph.endVertex[st.vertex[j + 1]])
                        tempGraph.addEdge(edge)

        print('V={')
        for v in tempGraph.endVertex:
            print(v)
        print('}')
        print('E={')
        count = 0
        for e in tempGraph.edge:
            count += 1
            if count < len(tempGraph.edge):
                print(str(e) + ',')
            else:
                print(str(e))
        print('}')


def calcIntersection(line1, line2):
    l1 = InterLine(line1)

    l2 = InterLine(line2)

    D = l1.a * l2.b - l2.a * l1.b

    if D != 0:

        inter_x = (l1.b * l2.c - l2.b * l1.c) / D

        inter_y = (l1.c * l2.a - l2.c * l1.a) / D

        inter = Vertex(inter_x, inter_y)

        dist1 = math.sqrt((line1.start.x - inter.x) ** 2 + (line1.start.y - inter.y) ** 2)

        dist2 = math.sqrt((inter.x - line1.end.x) ** 2 + (inter.y - line1.end.y) ** 2)

        dist3 = math.sqrt((line1.start.x - line1.end.x) ** 2 + (line1.start.y - line1.end.y) ** 2)

        dist4 = math.sqrt((line2.start.x - inter.x) ** 2 + (line2.start.y - inter.y) ** 2)

        dist5 = math.sqrt((inter.x - line2.end.x) ** 2 + (inter.y - line2.end.y) ** 2)

        dist6 = math.sqrt((line2.start.x - line2.end.x) ** 2 + (line2.start.y - line2.end.y) ** 2)

        if (dist3 >= dist1 and dist3 >= dist2) and (dist6 >= dist4 and dist6 >= dist5):
            return inter

    return None

def calcCover(line1, line2):
    l1 = InterLine(line1)

    l2 = InterLine(line2)

    D = l1.a * l2.b - l2.a * l1.b

    if D == 0:
        line3 = Line(line1.start, line2.start)
        l3 = InterLine(line3);

        DD = l1.a * l3.b - l3.a * l1.b

        if DD == 0:
            return True

    return False

idList = {}

finalGraph = Graph()

while True:
    try:
        arg = raw_input()

        if arg[0] == "a":

            finalGraph.addStreet(arg)

        elif arg[0] == "c":

            finalGraph.changeStreet(arg)

        elif arg[0] == "r":

            finalGraph.removeStreet(arg)

        elif arg[0] == "g":

            finalGraph.initGraph()

        else:

            print("Error: starting with a, c, r, and g only!")

    except EOFError:

        sys.exit()
