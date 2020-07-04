import matplotlib.pyplot as plt
import math
import numpy as np


class Node:
    positionX = 0
    positionY = 0
    reactionX = 0
    reactionY = 0
    extForceX = 0
    extForceY = 0
    reactionX = 0
    reactionY = 0
    rollingReaction = 0

    attachedBeams = []

    def __init__(self, positionX, positionY, *args):
        self.positionX = positionX
        self.positionY = positionY

    def getBeams(self, beams):
        '''creates a list of beams attached to the node'''
        temp = []
        for beam in beams:
            if beam.startNode == self or beam.endNode == self:
                if beam not in temp:
                    temp.append(beam)
        self.attachedBeams = temp

    def getFBD(self, beams):
        """ Creates an equilibrium system of equations by 
        balancing forces in x and y directions"""
        coefficientMatrix = np.zeros((2, len(beams)))
        forceMatrix = np.zeros(2)
        reactionMatrix = np.zeros((2, 3))

        for beam in beams:
            if beam in self.attachedBeams:
                i = beams.index(beam)
                u = beam.getUnitVector()
                if beam.endNode == self:
                    u = -u
                coefficientMatrix[0, i] = u[0]
                coefficientMatrix[1, i] = u[1]

        forceMatrix[0] = self.extForceX
        forceMatrix[1] = self.extForceY

        reactionMatrix[0, 0] = self.reactionX
        reactionMatrix[1, 1] = self.reactionY
        reactionMatrix[1, 2] = self.rollingReaction

        coefficientMatrix = np.hstack((coefficientMatrix, reactionMatrix))

        return coefficientMatrix, forceMatrix

    def whichNode(self):
        for beam in self.attachedBeams:
            if beam.startNode == self:
                print("you are a start node")
            else:
                print("you are an end node")

    def __eq__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.positionX == other.positionX and self.positionY == other.positionY


class Beam:
    startNode = Node(0, 0)
    endNode = Node(0, 0)
    force = 0

    def __init__(self, startNode, endNode):
        self.startNode = startNode
        self.endNode = endNode

    def getUnitVector(self):
        '''returns unit vector along the direction of the beam'''
        x1 = self.startNode.positionX
        x2 = self.endNode.positionX
        y1 = self.startNode.positionY
        y2 = self.endNode.positionY
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        u = np.array([x2-x1, y2-y1])/distance
        return u


class Truss:
    beams = []  # list of beams in the truss
    nodes = []  # list of nodes in the truss

    def __init__(self, beams, nodes):
        self.beams = beams
        self.nodes = nodes
        self.beamForces = np.zeros(len(beams))

        for node in nodes:
            node.getBeams(beams)

    def visualizeTruss(self):

        points = ["A", "B", "C", "D", "E", "F"]

        for beam in self.beams:
            x = [beam.startNode.positionX, beam.endNode.positionX]
            y = [beam.startNode.positionY, beam.endNode.positionY]

            index = self.beams.index(beam)
            forces = "{} kips".format(str(round(self.beamForces[index], 3)))

            xylabel = ((x[0]+x[1])/2, (y[0]+y[1])/2)

            plt.plot(x, y, label=forces)

        for node in self.nodes:
            plt.annotate(points[self.nodes.index(node)],
                         (node.positionX, node.positionY))

        plt.legend()
        plt.show()

    def forceMatrix(self):

        matrix = np.zeros((len(self.nodes)*2, len(self.beams)))
        return matrix

    def solveTruss(self):

        equationsTuple = tuple(
            (node.getFBD(self.beams)[0] for node in self.nodes))
        reactionMatrixTuple = tuple(
            (node.getFBD(self.beams)[1] for node in self.nodes))
        forceMatrixTuple = tuple(
            (node.getFBD(self.beams)[1] for node in self.nodes))

       
        coefficientMatrix = np.vstack(equationsTuple)
        forceMatrix = -np.hstack(forceMatrixTuple)
        print(coefficientMatrix)
        print(forceMatrix)

        self.beamForces = np.linalg.solve(coefficientMatrix, forceMatrix)
        self.beamForces = np.around(self.beamForces, decimals=2)
