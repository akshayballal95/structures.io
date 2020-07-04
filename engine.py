from geo.geometry import Node, Beam, Truss

import numpy as np

# node1 = Node(0, 0)
# node2 = Node(3, 4)
# node3 = Node(6, 0)
# node4 = Node(9, 4)
# node5 = Node(12, 0)
# beam1 = Beam(node1, node2)
# beam2 = Beam(node2, node3)
# beam3 = Beam(node3, node1)
# beam4 = Beam(node3, node4)
# beam5 = Beam(node4, node5)
# beam6 = Beam(node5, node3)
# beam7 = Beam(node2, node4)
# fixedNode = node1
# rollingNode = node5

# fixedNode.reactionX = 1
# fixedNode.reactionY = 1

# rollingNode.rollingReaction = 1

# node2.extForceY = -1
# node4.extForceX = 2
# node3.extForceY = -3

def trussMaker (JSON_Truss):
    nodes = []
    beams = []
    for JSON_Beam in JSON_Truss['beams']:
        node1 = Node(int(JSON_Beam['start']['x']), int(JSON_Beam['start']['y']))
        node2 = Node(int(JSON_Beam['end']['x']), int(JSON_Beam['end']['y']))
        beam = Beam(node1, node2)
        beams.append(beam)
        if node1 not in nodes:
            nodes.append(node1)
        if node2 not in nodes:
            nodes.append(node2)
    
    fixedNode = Node(int(JSON_Truss['fixed_joint']['x']), int(JSON_Truss['fixed_joint']['y']))
    rollingNode = Node(int(JSON_Truss['rolling_joint']['x']), int(JSON_Truss['rolling_joint']['y']))
    for node in nodes: 
        if fixedNode==node:
            node.reactionX=1
            node.reactionY=1

        if rollingNode == node:
            node.rollingReaction = 1

    for force in JSON_Truss['external_forces']:
        joint = force['joint']
        forceX = int(force['force']['dirX'])
        forceY = int(force['force']['dirY'])
        node_joint = Node(int(joint['x']), int(joint['y']))

        for node in nodes:
            if node==node_joint:
                node.extForceX = forceX
                node.extForceY = forceY


    truss = Truss(beams,nodes)
    return truss


def defineTruss():
    node1 = Node(0,0)
    node2 = Node(4,0)
    node3 = Node(8,0)
    node4 = Node(12,0)
    node5 = Node(4,-3)
    node6 = Node(8,-3)

    beam1 = Beam(node1, node2)
    beam2 = Beam(node2, node3)
    beam3 = Beam(node3, node4)
    beam4 = Beam(node1, node5)
    beam5 = Beam(node2, node6)
    beam6 = Beam(node4, node6)
    beam7 = Beam(node2, node5)
    beam8 = Beam(node3, node6)
    beam9 = Beam(node5, node6)

    node1.reactionX = 1
    node1.reactionY = 1
    node6.rollingReaction = 1

    node2.extForceY = -200
    node3.extForceY = -400
    node4.extForceY = -300

    truss = Truss([beam1, beam2, beam3, beam4, beam5, beam6, beam7,beam8, beam9], [node1, node2, node3, node4, node5,node6])
    return truss

def solve(truss):
    
    # truss = defineTruss()
    truss.solveTruss()

    beamForcesDict = {}

    # for i in range(0,len(truss.beams)):
    #     beamForcesDict["beam_{}".format(i+1)] = round(truss.beamForces[i],2)

    # for i in range(len(truss.beams),len(truss.beamForces)):
    #     beamForcesDict["reaction_{}".format(i-len(truss.beams)+1)]=round(truss.beamForces[i],2)

    beamForcesDict['forces'] = ','.join(map(str,truss.beamForces[0:len(truss.beams)]))
    beamForcesDict['reactions'] = ','.join(map(str,truss.beamForces[len(truss.beams):]))
    # truss.visualizeTruss()
    

    return beamForcesDict