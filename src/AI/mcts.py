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

        #if there is no parent node, state.player (1 or 2) is the player running the mcts algorithm and we want to have the other player as the root node player
        if parent is None : 
            self.player =  3 - state.player
        else:
            self.player = 3 - self.parent.player

    def isFullyExpanded(self):
        return len(self.state.actions)==len(self.children)


class MCTS():

    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=sqrt(2),
                 rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, initialState, needDetails):
        self.root = treeNode(initialState, None)
        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()
        
        bestChild = self.getBestChild(self.root, 0)
        action=(action for action, node in self.root.children.items() if node is bestChild).__next__()

        if needDetails:
            for node, info in self.root.children.items():
                print(node,':',info.totalReward, info.numVisits, round(info.totalReward/info.numVisits,2))
            return action
        else:
            return action

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
        Returns 1 if the winner is the player who is running the mcts algorithm
        else return 0.
        """
        while node is not None:
            node.numVisits += 1
            node.totalReward += (reward == 1) * (node.player != self.root.player)
            node = node.parent

    def getBestChild(self, node, explorationValue):
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
