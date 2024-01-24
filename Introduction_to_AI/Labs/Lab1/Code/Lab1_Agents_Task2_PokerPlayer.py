# Please feel free to work with your own code structure

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
import random

# 2 example poker hands
example_hand1 = ['Ad', '2s', '2c']
example_hand2 = ['5s', '5c', '5d']


# Randomly generate two hands of n cards
def generate_2hands(nn_card=3):
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['s', 'h', 'd', 'c']

    # Generate all possible combinations
    all_possibilities = [rank + suit for rank in ranks for suit in suits]
    lengthall = len(all_possibilities)
    boollist = [False] * lengthall
    i = 0
    hand1 = []
    hand2 = []
    while i < nn_card * 2:
        randomnum = random.randint(1, lengthall) - 1

        if not boollist[randomnum]:
            boollist[randomnum] = True
            if i < nn_card:
                hand1.append(all_possibilities[randomnum])
            else:
                hand2.append(all_possibilities[randomnum])
            i += 1

    return hand1, hand2


rank_values = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12,
               'A': 13}
rank_comb = {'high': 0, 'pair': 13, 'three': 26}


# identify hand category using IF-THEN rule
def identify_hand(hand_):
    for c1 in hand_:
        for c2 in hand_:
            for c3 in hand_:
                if (c1[0] == c2[0]) and (c3[0] == c2[0]) and (c1[1] < c2[1]) and (c2[1] < c3[1]) and (c1[1] < c3[1]):
                    return dict(name='three', rank=c1[0], suit1=c1[1], suit2=c2[1], suit3=c3[1])

    for c1 in hand_:
        for c2 in hand_:
            if (c1[0] == c2[0]) and (c1[1] < c2[1]):
                return dict(name='pair', rank=c1[0], suit1=c1[1], suit2=c2[1])

    high = 0
    for i in range(0, len(hand_)):
        if rank_values[hand_[i][0]] > rank_values[hand_[high][0]]:
            high = i

    return dict(name='high', rank=hand_[high][0], suit1=hand_[high][1])


# Print out the result
def analyse_hand(hand_):
    hand_ident = identify_hand(hand_)

    score = rank_comb[hand_ident['name']] + rank_values[hand_ident['rank']]
    return score


class RandomAgent():
    def act(self, hand_score, beting_):
        return random.randint(0, 50)


class FixedAgent():
    def act(self, hand_score, beting_):
        return 25


class ReflexAgent():
    def act(self, hand_score, beting_):
        return int(round((50 / 39))) * hand_score


# writing your test code here


#########################
#      Game flow        #
#########################
agent1 = RandomAgent()
agent2 = ReflexAgent()
total_pot1 = 0
total_pot2 = 0
for i in range(0, 500):

    #########################
    # phase 1: Card Dealing #
    #########################
    hand1, hand2 = generate_2hands()

    score1 = analyse_hand(hand1)
    score2 = analyse_hand(hand2)
    #########################
    # phase 2:   Bidding    #
    #########################
    hand_pot = 0
    bet1 = -1
    bet2 = -1
    for i in range(0, 3):
        bet1 = agent1.act(score1, None)
        bet2 = agent2.act(score2, None)

        hand_pot += bet2 + bet1
    # Sensing, resoning & decision making, and acting

    #########################
    # phase 2:   Showdown   #
    #########################
    if (score1 != score2):
        if (score1 > score2):
            total_pot1 += hand_pot
        else:
            total_pot2 += hand_pot

print('Agent 1 pot: ', total_pot1)
print('Agent 2 pot: ', total_pot2)
