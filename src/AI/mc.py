from time import time
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

        # if there is no parent node, state.player (1 or 2) is the player running 
        # the mcts algorithm and we want to have the other player as the root node player
        if parent is None : 
            self.player =  3 - state.player
        else:
            self.player = 3 - self.parent.player

class MC():

    def __init__(self, timeLimit=None, iterationLimit=None, rolloutPolicy=randomPolicy):
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
        self.rollout = rolloutPolicy


    def search(self, initialState, needDetails=False):
        self.root = treeNode(initialState, None)
        actions = self.root.state.actions
        # init each node
        for action in actions:
            root_state = deepcopy(self.root.state)
            root_state.takeAction(action, root_state.currplayer)
            node = treeNode(root_state, self.root)
            self.root.children[action] = node
            self.executeRound(node)

        if self.limitType == 'time':
            timeLimit = time() + self.timeLimit / (1000 * len(actions))
            for child in self.root.children.values():
                while time.time() < timeLimit:
                    self.executeRound(child)
        else:
            nb_iter = int(self.searchLimit / len(actions))
            for child in self.root.children.values():
                for i in range(nb_iter):
                    self.executeRound(child)
                    
        bestChild = self.getBestChild(self.root)
        action = (action for action, node in self.root.children.items() if node is bestChild).__next__()

        if needDetails:
            for node, info in self.root.children.items():
                print(node,':',info.totalReward, info.numVisits, round(info.totalReward/info.numVisits,2))
            print(action)
            return action
            
        return action

    def executeRound(self, node):
        state = deepcopy(node.state)
        reward = self.rollout(state)
        self.backpropogate(node, reward)

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = child.totalReward / child.numVisits
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)
