
from abc import ABC, abstractmethod
from checkersboard import *
from checkersboard import extract_features, calculate_reward


class Agent(ABC):

    def __init__(self, is_learning_agent=False):
        self.is_learning_agent = is_learning_agent
        self.has_been_learning_agent = is_learning_agent

    def get_action(self, state):
        pass


class Human(Agent):

    def __init__(self):
        Agent.__init__(self)


    def get_action(self, state):

        start = [int(pos) for pos in input("Enter starting row: ").split(" ")]
        start = [int(pos) for pos in input("Enter starting col position: ").split(" ")]
        end = [int(pos) for pos in input("Enter ending row: ").split(" ")]
        end = [int(pos) for pos in input("Enter ending col: ").split(" ")]

        ends = []
        i=1
        while i < len(end):
            ends.append([end[i-1], end[i]])
            i += 2

        action = [start] + ends
        return action


class AlphaBetaAgent(Agent):

    def __init__(self, depth):
        Agent.__init__(self, is_learning_agent=False)
        self.depth = depth

    def evaluation_function(self, state, agent=True):

        agent_ind = 0 if agent else 1
        other_ind = 1 - agent_ind

        if state.is_game_over():
            if agent and state.is_first_agent_win():
                return 500

            if not agent and state.is_second_agent_win():
                return 500

            return -500

        pieces_and_kings = state.get_pieces_and_kings()
        return pieces_and_kings[agent_ind] + 2 * pieces_and_kings[agent_ind + 2] - \
        (pieces_and_kings[other_ind] + 2 * pieces_and_kings[other_ind + 2])

    def get_action(self, state):

        def mini_max(state, depth, agent, A, B):
            if agent >= state.get_num_agents():
                agent = 0

            depth += 1
            if depth == self.depth or state.is_game_over():
                return [None, self.evaluation_function(state, max_agent)]
            elif agent == 0:
                return maximum(state, depth, agent, A, B)
            else:
                return minimum(state, depth, agent, A, B)

        def maximum(state, depth, agent, A, B):
            output = [None, -float("inf")]
            actions_list = state.get_legal_actions()

            if not actions_list:
                return [None, self.evaluation_function(state, max_agent)]

            for action in actions_list:
                current = state.generate_successor(action)
                val = mini_max(current, depth, agent + 1, A, B)

                check = val[1]

                if check > output[1]:
                    output = [action, check]

                if check > B:
                    return [action, check]

                A = max(A, check)

            return output

        def minimum(state, depth, agent, A, B):
            output = [None, float("inf")]
            actions_list = state.get_legal_actions()

            if not actions_list:
                return [None, self.evaluation_function(state, max_agent)]

            for action in actions_list:
                current = state.generate_successor(action)
                val = mini_max(current, depth, agent+1, A, B)

                check = val[1]

                if check < output[1]:
                    output = [action, check]

                if check < A:
                    return [action, check]

                B = min(B, check)

            return output

        max_agent = state.is_first_agent_turn()
        output = mini_max(state, -1, 0, -float("inf"), float("inf"))
        return output[0]


class ReinforcementLearningAgent(Agent):

    def __init__(self, is_learning_agent=True):
        Agent.__init__(self, is_learning_agent)

        self.episodes_so_far = 0

    def get_action(self, state):

        pass

    def update(self, state, action, next_state, reward):
        pass

    def start_episode(self):
        self.prev_state = None
        self.prev_action = None

        self.episode_rewards = 0.0


    def stop_episode(self):
        pass


    def start_learning(self):
        pass


    def stop_learning(self):
        pass


    def observe_transition(self, state, action, next_state, reward, next_action=None):
        pass


    def observation_function(self, state):
        pass


    def do_action(self, state, action):
        
        self.prev_state = state
        self.prev_action = action


class QLearningAgent(ReinforcementLearningAgent):
    def __init__(self, alpha=0.01, gamma=0.1, epsilon=0.5, is_learning_agent=True, weights=None):
        ReinforcementLearningAgent.__init__(self, is_learning_agent=is_learning_agent)
        self.original_alpha = alpha
        self.original_epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        if not is_learning_agent:
            self.epsilon = 0.0
            self.alpha = 0.0
        
        else:
                raise Exception("Invalid weights " + weights)

    def start_learning(self):
        self.alpha = self.original_alpha
        self.epsilon = self.original_epsilon
        self.is_learning_agent = True

    def stop_learning(self):
        self.alpha = 0.0
        self.epsilon = 0.0
        self.is_learning_agent = False

    def get_q_value(self, state, action, features):
        q_value = np.dot(self.weights, features)
        return q_value


    def compute_value_from_q_values(self, state):

        actions = state.get_legal_actions()

        if not actions:
            return 0.0

        q_values = \
        [self.get_q_value(state, action, extract_features(state, action)) for action in actions]

        return max(q_values)


    def compute_action_from_q_values(self, state, actions):

        if not actions:
            return None


        arg_max = np.argmax([self.get_q_value(state, action, checkers_features(state, action)) 
            for action in actions])

        return actions[arg_max]


    def get_action(self, state):
        legal_actions = state.get_legal_actions()
        action = None

        if not legal_actions:
            return None

        else:
            action = self.compute_action_from_q_values(state, legal_actions)

        self.do_action(state, action)
        return action


    def update(self, state, action, next_state, reward):

        features = extract_features(state, action)

        expected = reward + self.gamma * self.compute_value_from_q_values(next_state)
        current = self.get_q_value(state, action, features)

        temporal_difference = expected - current
