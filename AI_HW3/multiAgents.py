from util import manhattanDistance
from game import Directions
import random, util
from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        # Begin your code (Part 1)

        def minimax(state, index, agent_count, max_index):
            if state.isWin() or state.isLose() or index == max_index:  # Terminal State or Max Depth reached
                return self.evaluationFunction(state), None  # return the heuristic value
            actions = state.getLegalActions(index % agent_count)  # all legal moves of current player
            scores = [minimax(
                state.getNextState(index % agent_count, act),
                index + 1,
                agent_count,
                max_index
            )[0] for act in actions]  # get every possible action's value
            if (index % agent_count) == 0:  # Max Player
                max_score = max(scores)  # choose the best one
                move = scores.index(max_score)  # and get its corresponding action
                return max_score, actions[move]
            else:  # Min Player
                min_score = min(scores)  # choose the worst one
                move = scores.index(min_score)  # and get its corresponding action
                return min_score, actions[move]

        num = gameState.getNumAgents()
        score, action = minimax(gameState, 0, num, self.depth * num)
        # maxIndex (total rounds) = depth (turns) * num (players)

        return action

        # raise NotImplementedError("To be implemented")
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        # Begin your code (Part 2)

        def alpha_beta(state, index, agent_count, max_index, alpha, beta):
            if state.isWin() or state.isLose() or index == max_index:  # Terminal State or Max Depth reached
                return self.evaluationFunction(state), None  # return the heuristic value
            actions = state.getLegalActions(index % agent_count)  # all legal moves of current player
            if (index % agent_count) == 0:  # Max Player
                val = (-0xffffffff, None)  # init val = -inf
                for act in actions:
                    v = alpha_beta(
                        state.getNextState(index % agent_count, act),
                        index + 1,
                        agent_count,
                        max_index,
                        alpha,
                        beta
                    )  # v = value(successor)
                    if v[0] > val[0]:  # val = max(v, val)
                        val = v[0], act  # max value and its action
                    if val[0] > beta:  # beta prune
                        return val
                    alpha = max(alpha, val[0])  # update alpha
                return val
            else:  # Min Player
                val = (0xffffffff, None)  # init val = inf
                for act in actions:
                    v = alpha_beta(
                        state.getNextState(index % agent_count, act),
                        index + 1,
                        agent_count,
                        max_index,
                        alpha,
                        beta
                    )  # v = value(successor)
                    if v[0] < val[0]:  # val = min(v, val)
                        val = v[0], act  # min value and its action
                    if val[0] < alpha:  # alpha prune
                        return val
                    beta = min(beta, val[0])  # update beta
                return val

        num = gameState.getNumAgents()
        score, action = alpha_beta(gameState, 0, num, self.depth * num, -0xffffffff, 0xffffffff)
        # Alpha-Beta(state, alpha = -inf, beta = inf)

        return action

        # raise NotImplementedError("To be implemented")
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        # Begin your code (Part 3)

        def expectimax(state, index, agent_count, max_index):
            if state.isWin() or state.isLose() or index == max_index:  # Terminal State or Max Depth reached
                return self.evaluationFunction(state), None  # return the heuristic value
            actions = state.getLegalActions(index % agent_count)  # all legal moves of current player
            scores = [expectimax(
                state.getNextState(index % agent_count, act),
                index + 1,
                agent_count,
                max_index
            )[0] for act in actions]  # get every possible action's value
            if (index % agent_count) == 0:  # Max Player
                max_score = max(scores)  # choose the best one
                move = scores.index(max_score)  # and get its corresponding action
                return max_score, actions[move]
            else:  # Chance Player
                avg_score = sum(scores) / len(actions)  # calculate the average value of all possible moves
                return avg_score, None

        num = gameState.getNumAgents()
        score, action = expectimax(gameState, 0, num, self.depth * num)

        return action

        # raise NotImplementedError("To be implemented")
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)

    pos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()

    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates if ghostState.scaredTimer > 0]
    capsules = currentGameState.getCapsules()
    foods = currentGameState.getFood().asList()

    nearestGhostDist = min([manhattanDistance(pos, state.getPosition()) for state in ghostStates])
    nearestScaredGhostDist = -1 if not scaredTimes else min(
        [manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates if ghost.scaredTimer > 0])
    nearestFoodDist = 0 if not foods else min([manhattanDistance(pos, food) for food in foods])
    nearestCapsuleDist = 0 if not capsules else min([manhattanDistance(pos, capsule) for capsule in capsules])

    if nearestGhostDist <= 1 and nearestScaredGhostDist == -1:  # the least willing result, DIE
        return -0xffff  # huge penalty

    if nearestScaredGhostDist != -1:
        """
        if there is a scared ghost,
        then eating capsules and foods are not that important.
        start chasing ghosts instead.
        scared ghost distance (as close as possible, the most important, so times -50)
        food and capsule distance (as close as possible, so times -5)
        """
        return nearestScaredGhostDist * -50 + nearestFoodDist * -5 + nearestCapsuleDist * -5
    else:
        """
        normal time, game over when touching a ghost.
        so nearest ghost distant is an factor, but not that important.
        trying to get close to foods and capsules are the most valuable factor,
        also the count doesn't changes a lot, so it needs a big multiplier, say 1000.
        ghost distance (as far as possible, not that important, so / 10)
        food and capsule distance (as close as possible, so times -10)
        # of capsules and foods (as small as possible, very important, so * -1000)
        """
        return nearestGhostDist / 10 + nearestFoodDist * -10 + nearestCapsuleDist * -10 + \
            len(capsules) * -1000 + len(foods) * -1000

    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)


# Abbreviation
better = betterEvaluationFunction
