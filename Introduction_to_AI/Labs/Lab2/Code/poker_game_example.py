import poker_environment as pe_
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
import copy

"""
Player class
"""


class PokerPlayer(object):
    def __init__(self, current_hand_=None, stack_=300, action_=None, action_value_=None):
        self.current_hand = current_hand_
        self.current_hand_type = []
        self.current_hand_strength = []
        self.stack = stack_
        self.action = action_
        self.action_value = action_value_

    """
    identify agent hand and evaluate it's strength
    """

    def evaluate_hand(self):
        self.current_hand_type = pe_.identify_hand(self.current_hand)
        self.current_hand_strength = pe_.Types[self.current_hand_type[0]] * len(pe_.Ranks) + pe_.Ranks[
            self.current_hand_type[1]]

    """
    return possible actions, fold if there is not enough money...
    """

    def get_actions(self):
        actions_ = []
        for _action_ in AGENT_ACTIONS:
            # If bet more or same as he owns in his stack, automatically folds
            if _action_[:3] == 'BET' and int(_action_[3:]) >= (self.stack):
                actions_.append('FOLD')
            else:
                actions_.append(_action_)
        return set(actions_)


"""
Game State class
"""


class GameState(object):
    def __init__(self,
                 nn_current_hand_=None,
                 nn_current_bidding_=None,
                 phase_=None,
                 pot_=None,
                 acting_agent_=None,
                 parent_state_=None,
                 children_state_=None,
                 agent_=None,
                 opponent_=None):

        self.nn_current_hand = nn_current_hand_
        self.nn_current_bidding = nn_current_bidding_
        self.phase = phase_
        self.pot = pot_
        self.acting_agent = acting_agent_
        self.parent_state = parent_state_
        self.children = children_state_
        self.agent = agent_
        self.opponent = opponent_
        self.showdown_info = None
        self.hands = 1

    """
    draw 10 cards randomly from a deck
    """

    def dealing_cards(self):

        if self.nn_current_hand >= 20:
            print("random hand  ", self.nn_current_hand)
            # randomly generated hands
            agent_hand, opponent_hand = pe_.generate_2hands()
        else:
            # fixed_hands or use the function below
            print("fixed hand ", self.nn_current_hand)
            agent_hand, opponent_hand = pe_.fixed_hands[self.nn_current_hand]
        self.agent.current_hand = agent_hand
        self.agent.evaluate_hand()
        self.opponent.current_hand = opponent_hand
        self.opponent.evaluate_hand()

    """
    draw 10 cards from a fixed sequence of hands
    """

    def dealing_cards_fixed(self):
        self.agent.current_hand = pe_.fixed_hands[self.nn_current_hand][0]
        self.agent.evaluate_hand()
        self.opponent.current_hand = pe_.fixed_hands[self.nn_current_hand][1]
        self.opponent.evaluate_hand()

    """
    SHOWDOWN phase, assign pot to players
    """

    def showdown(self):

        if self.agent.current_hand_strength == self.opponent.current_hand_strength:
            self.showdown_info = 'draw'
            if self.acting_agent == 'agent':
                self.agent.stack += (self.pot - 5) / 2. + 5
                self.opponent.stack += (self.pot - 5) / 2.
            else:
                self.agent.stack += (self.pot - 5) / 2.
                self.opponent.stack += (self.pot - 5) / 2. + 5
        elif self.agent.current_hand_strength > self.opponent.current_hand_strength:
            self.showdown_info = 'agent win'
            self.agent.stack += self.pot
        else:
            self.showdown_info = 'opponent win'
            self.opponent.stack += self.pot

    # print out necessary information of this game state
    def print_state_info(self):

        print('************* state info **************')
        print('nn_current_hand', self.nn_current_hand)
        print('nn_current_bidding', self.nn_current_bidding)
        print('phase', self.phase)
        print('pot', self.pot)
        print('acting_agent', self.acting_agent)
        """
        print('parent_state', self.parent_state)
        print('children', self.children)
        print('agent', self.agent)
        print('opponent', self.opponent)
        """
        if self.phase == 'SHOWDOWN':
            print('---------- showdown ----------')
            print('agent.current_hand', self.agent.current_hand)
            print(self.agent.current_hand_type, self.agent.current_hand_strength)
            print('opponent.current_hand', self.opponent.current_hand)
            print(self.opponent.current_hand_type, self.opponent.current_hand_strength)
            print('showdown_info', self.showdown_info)

        print('----- agent -----')
        print('agent.current_hand', self.agent.current_hand)
        print('agent.current_hand_type', self.agent.current_hand_type)
        print('agent.current_hand_strength', self.agent.current_hand_strength)
        print('agent.stack', self.agent.stack)
        print('agent.action', self.agent.action)
        print('agent.action_value', self.agent.action_value)

        print('----- opponent -----')
        print('opponent.current_hand', self.opponent.current_hand)
        print('opponent.current_hand_type', self.opponent.current_hand_type)
        print('opponent.current_hand_strength', self.opponent.current_hand_strength)
        print('opponent.stack', self.opponent.stack)
        print('opponent.action', self.opponent.action)
        print('opponent.action_value', self.opponent.action_value)
        print('**************** end ******************')


# copy given state in the argument
def copy_state(game_state):
    _state = copy.copy(game_state)
    _state.agent = copy.copy(game_state.agent)
    _state.opponent = copy.copy(game_state.opponent)
    return _state


def get_next_states(last_state):
    if last_state.phase == 'SHOWDOWN' or last_state.acting_agent == 'opponent' or last_state.phase == 'INIT_DEALING':

        # NEW BETTING ROUND, AGENT ACT FIRST

        states = []

        for _action_ in last_state.agent.get_actions():

            _state_ = copy_state(last_state)
            _state_.acting_agent = 'agent'

            if last_state.phase == 'SHOWDOWN' or last_state.phase == 'INIT_DEALING':
                # _state_.dealing_cards()
                _state_.dealing_cards_fixed()

            if _action_ == 'CALL':

                _state_.phase = 'SHOWDOWN'
                _state_.agent.action = _action_
                _state_.agent.action_value = 5
                _state_.agent.stack -= 5
                _state_.pot += 5

                _state_.showdown()

                _state_.nn_current_hand += 1
                _state_.nn_current_bidding = 0
                _state_.pot = 0
                _state_.parent_state = last_state
                _state_.hands += 1
                states.append(_state_)

            elif _action_ == 'FOLD':

                _state_.phase = 'SHOWDOWN'
                _state_.agent.action = _action_
                _state_.opponent.stack += _state_.pot

                _state_.nn_current_hand += 1
                _state_.nn_current_bidding = 0
                _state_.pot = 0
                _state_.parent_state = last_state
                _state_.hands += 1
                states.append(_state_)


            elif _action_ in BETTING_ACTIONS:

                _state_.phase = 'BIDDING'
                _state_.agent.action = _action_
                _state_.agent.action_value = int(_action_[3:])
                _state_.agent.stack -= int(_action_[3:])
                _state_.pot += int(_action_[3:])

                _state_.nn_current_bidding += 1
                _state_.parent_state = last_state
                states.append(_state_)

            else:

                print('...unknown action...')
                exit()

        return states

    elif last_state.phase == 'BIDDING' and last_state.acting_agent == 'agent':

        states = []
        _state_ = copy_state(last_state)
        _state_.acting_agent = 'opponent'

        opponent_action, opponent_action_value = pe_.poker_strategy_example(last_state.opponent.current_hand_type[0],
                                                                            last_state.opponent.current_hand_type[1],
                                                                            last_state.opponent.stack,
                                                                            last_state.agent.action,
                                                                            last_state.agent.action_value,
                                                                            last_state.agent.stack,
                                                                            last_state.pot,
                                                                            last_state.nn_current_bidding)

        if opponent_action == 'CALL':

            _state_.phase = 'SHOWDOWN'
            _state_.opponent.action = opponent_action
            _state_.opponent.action_value = 5
            _state_.opponent.stack -= 5
            _state_.pot += 5

            _state_.showdown()

            _state_.nn_current_hand += 1
            _state_.nn_current_bidding = 0
            _state_.pot = 0
            _state_.parent_state = last_state
            _state_.hands += 1
            states.append(_state_)

        elif opponent_action == 'FOLD':

            _state_.phase = 'SHOWDOWN'

            _state_.opponent.action = opponent_action
            _state_.agent.stack += _state_.pot

            _state_.nn_current_hand += 1
            _state_.nn_current_bidding = 0
            _state_.pot = 0
            _state_.parent_state = last_state
            _state_.hands += 1
            states.append(_state_)

        elif opponent_action + str(opponent_action_value) in BETTING_ACTIONS:

            _state_.phase = 'BIDDING'

            _state_.opponent.action = opponent_action
            _state_.opponent.action_value = opponent_action_value
            _state_.opponent.stack -= opponent_action_value
            _state_.pot += opponent_action_value

            _state_.nn_current_bidding += 1
            _state_.parent_state = last_state
            states.append(_state_)

        else:
            print('unknown_action')
            exit()
        return states


"""
successor function for generating next state(s)
"""


def call(last_state, action):
    # state = copy_state(last_state)
    last_state.phase = 'SHOWDOWN'

    if last_state.acting_agent == "agent":
        last_state.agent.action = action
        last_state.agent.action_value = 5
        last_state.agent.stack -= 5
    else:
        last_state.opponent.action = action
        last_state.opponent.action_value = 5
        last_state.opponent.stack -= 5

    last_state.pot += 5

    last_state.showdown()

    last_state.nn_current_hand += 1
    last_state.nn_current_bidding = 0
    last_state.pot = 0
    last_state.parent_state = last_state

    return last_state


def fold(last_state, action):
    # state = copy_state(last_state)
    last_state.phase = 'SHOWDOWN'

    if last_state.acting_agent == "agent":
        last_state.opponent.action = action
        last_state.agent.stack += last_state.pot
    else:
        last_state.agent.action = action
        last_state.opponent.stack += last_state.pot

    last_state.nn_current_hand += 1
    last_state.nn_current_bidding = 0
    last_state.pot = 0
    last_state.parent_state = last_state

    return last_state


def bet(last_state, action, opponent_action_value):
    # state = copy_state(last_state)

    last_state.phase = 'BIDDING'

    if last_state.acting_agent == "agent":
        last_state.agent.action = action
        last_state.agent.action_value = int(action[3:])
        last_state.agent.stack -= int(action[3:])
        last_state.pot += int(action[3:])
    else:
        last_state.opponent.action = action + str(opponent_action_value)
        last_state.opponent.action_value = opponent_action_value
        last_state.opponent.stack -= opponent_action_value
        last_state.pot += opponent_action_value

    last_state.nn_current_bidding += 1
    last_state.parent_state = last_state

    return last_state


def play(current_state, action, opponent_action_value):
    if action == "CALL":
        state = call(current_state, action)
        return state

    elif action == "FOLD":
        state = fold(current_state, action)
        return state

    elif opponent_action_value is False:
        if action in BETTING_ACTIONS:
            state = bet(current_state, action, False)
            return state
    elif opponent_action_value:
        state = bet(current_state, action, opponent_action_value)
        return state

    else:
        print('unknown_action')
        return current_state


def successor_bfs(gameState):
    gameState.acting_agent = "agent"
    states = [gameState]

    current_player = gameState.agent

    hands = 0
    nb_bidding = 0

    while len(states) != 0:
        current_state = states.pop(0)

        current_state.print_state_info()
        print()

        if hands == MAX_HANDS or current_state.agent.stack >= 500:
            return states, current_state, hands, nb_bidding

        if current_state.phase == 'SHOWDOWN' or current_state.phase == 'INIT_DEALING' or current_state.acting_agent == "opponent":
            if current_state.phase == 'SHOWDOWN' or current_state.phase == 'INIT_DEALING':
                current_state.dealing_cards()
                # current_state.dealing_cards_fixed()
                hands += 1
            if current_state.phase == "BIDDING":
                nb_bidding += 1

            current_state.acting_agent = "agent"
            for action in current_player.get_actions():
                current_state = play(current_state, action, False)
                states.append(current_state)

            current_player = current_state.opponent

        elif current_state.phase == "BIDDING" and current_state.acting_agent == "agent":
            nb_bidding += 1
            current_state.acting_agent = "opponent"
            opponent_action, opponent_action_value = pe_.poker_strategy_example(
                current_state.opponent.current_hand_type[0],
                current_state.opponent.current_hand_type[1],
                current_state.opponent.stack,
                current_state.agent.action,
                current_state.agent.action_value,
                current_state.agent.stack,
                current_state.pot,
                current_state.nn_current_bidding)

            current_state = play(current_state, opponent_action, opponent_action_value)
            states.append(current_state)
            current_player = current_state.agent

    return False


def successor_dfs(gameState, nb_nodes_extended=0, max_depth=10000):
    gameState.acting_agent = "agent"
    states = [gameState]

    current_player = gameState.agent

    hands = 0
    nb_bidding = 0

    while len(states) != 0:
        current_state = states.pop(-1)

        current_state.print_state_info()
        print()

        if hands == MAX_HANDS or current_state.agent.stack >= 500 or nb_nodes_extended > max_depth:
            return states, current_state, hands, nb_nodes_extended, nb_bidding

        if current_state.phase == 'SHOWDOWN' or current_state.phase == 'INIT_DEALING' or current_state.acting_agent == "opponent":
            if current_state.phase == 'SHOWDOWN' or current_state.phase == 'INIT_DEALING':
                current_state.dealing_cards()
                # current_state.dealing_cards_fixed()
                hands += 1
            if current_state.phase == "BIDDING":
                nb_bidding += 1

            current_state.acting_agent = "agent"
            for action in current_player.get_actions():
                current_state = play(current_state, action, False)
                states.append(current_state)

            current_player = current_state.opponent

        elif current_state.phase == "BIDDING" and current_state.acting_agent == "agent":
            nb_bidding += 1
            current_state.acting_agent = "opponent"
            opponent_action, opponent_action_value = pe_.poker_strategy_example(
                current_state.opponent.current_hand_type[0],
                current_state.opponent.current_hand_type[1],
                current_state.opponent.stack,
                current_state.agent.action,
                current_state.agent.action_value,
                current_state.agent.stack,
                current_state.pot,
                current_state.nn_current_bidding)

            current_state = play(current_state, opponent_action, opponent_action_value)
            states.append(current_state)
            current_player = current_state.agent

        nb_nodes_extended += len(states)

    return False


def init_game():
    # initialize 2 agents and a game_state
    agent = PokerPlayer(current_hand_=None, stack_=INIT_AGENT_STACK, action_=None, action_value_=None)
    opponent = PokerPlayer(current_hand_=None, stack_=INIT_AGENT_STACK, action_=None, action_value_=None)

    init_state = GameState(nn_current_hand_=0,
                           nn_current_bidding_=0,
                           phase_='INIT_DEALING',
                           pot_=0,
                           acting_agent_=None,
                           agent_=agent,
                           opponent_=opponent,
                           )
    return agent, opponent, init_state


def run_bfs():
    agent, opponent, init_state = init_game()
    return successor_bfs(init_state)


def run_dfs():
    agent, opponent, init_state = init_game()
    return successor_dfs(init_state)


MAX_HANDS = 4
INIT_AGENT_STACK = 400

bfs_states, bfs_end_state_, bfs_hands, bfs_nb_bidding = run_bfs()
dfs_states, dfs_end_state_, dfs_hands, nb_nodes_extended, dfs_nb_bidding = run_dfs()

print("BFS done")
print(f"Total of hands : {bfs_hands} ; Number of bidding: {bfs_nb_bidding}")
print(f"Agent stack: {bfs_end_state_.agent.stack} ; Opponent stack: {bfs_end_state_.opponent.stack}")

print()
print("DFS done")
print(f"Total of hands : {dfs_hands} ; Number of bidding: {dfs_nb_bidding}")
print(f"Agent stack: {dfs_end_state_.agent.stack} ; Opponent stack: {dfs_end_state_.opponent.stack}")
print(f"Expanded nodes: {nb_nodes_extended}")

exit()
