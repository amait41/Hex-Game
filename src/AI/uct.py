import os
import time
from math import log, sqrt
import random
from copy import deepcopy

def randomPolicy(state):
    while not state.isTerminal():
        try:
            action = random.choice(state.actions)
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: \n" + str(state))
        state.takeAction(action, state.currplayer)
    return state.getReward()


class treeNode():

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}
        if parent is None : 
            self.player =  3 - state.player
        else:
            self.player = 3 - self.parent.player

    def __str__(self):
        parent = f'Parent: {self.parent}\n'
        numVisits = f'numVisits: {self.numVisits}\n'
        totalReward = f'totalReward: {self.totalReward}\n'
        children = f'children: { {action for action in self.children.keys()} }\n'
        return parent + numVisits + totalReward + children

    def isFullyExpanded(self):
        return len(self.state.actions)==len(self.children)


class UCT():

    n = 1
    
    def __init__(self, explorationConstant, timeLimit=None, iterationLimit=None, 
                                                        rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each UCT search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.iterationLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy


    def search(self, initialState,  needDetails, root=None):

        self.root = treeNode(initialState, None) if root==None else root

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.iterationLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        action = (action for action, node in self.root.children.items() if node is bestChild).__next__()

        if needDetails:
            print(f'Color: {3 - self.root.player}')
            for node, info in self.root.children.items():
                print(node,':',info.totalReward, info.numVisits, round(info.totalReward/info.numVisits,2))
            print(f'Best action: {action}')
            print(f'Root numVisits: {self.root.numVisits}')
            return deepcopy(bestChild), action
        else:
            return deepcopy(bestChild), action

    def executeRound(self):
        """
        Execute a selection-expansion-simulation-backpropagation round.
        """
        node = self.selectNode(self.root)
        state = deepcopy(node.state)
        reward = self.rollout(state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.state.isTerminal():
            if node.isFullyExpanded():
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        while actions!=[]:
            action = random.choice(actions)
            if action not in node.children.keys():
                node_state = deepcopy(node.state)
                node_state.takeAction(action, node_state.currplayer)
                newNode = treeNode(node_state, node)
                node.children[action] = newNode
                return newNode
        raise Exception("No actions available after this node")

    def backpropogate(self, node, reward):
        """
        Returns 1 if the winner is the player who is running the UCT algorithm
        else return 0.
        """
        while node is not None:
            node.numVisits += 1
            node.totalReward += (reward == 1) * (node.player != self.root.player)
            node = node.parent

    def getBestChild(self, node, explorationValue):
        return self.ucb1(node,explorationValue)
        #return self.egreedy(node)
    
    def egreedy(self,node,c=0.2,d=0.01):
        e = min(1, c*len(node.state.actions)/d**2*n)
        n+=1
        if random.random()<1-e:
            return self.ucb1(node,0)
        else:
            return random.choice(node.children)

    def ucb1(self,node,explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = child.totalReward / child.numVisits + explorationValue * sqrt(
                log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)
