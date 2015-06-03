"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from pascal import get_probabilities

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    result = 0
    for i in range(num_rolls):
        roll = dice()
        if roll == 1:
            for j in range(num_rolls - i - 1):
                dice()
            return 1
        else: result += roll
    return result


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'

    if num_rolls == 0:
        return 1 + max([int(c) for c in str(opponent_score)])
    else:
        return roll_dice(num_rolls, dice)

# Playing a game

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """

    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    scorelist = [0, 0]
    stratlist = [strategy0, strategy1]
    

    while max(scorelist) < 100:
        score, opponent_score = scorelist[who], scorelist[other(who)]
        strat = stratlist[who]
        num_rolls = strat(score, opponent_score)
        dice = select_dice(score, opponent_score)
        scorelist[who] += take_turn(num_rolls, opponent_score, dice)
        if max(scorelist) == 2*min(scorelist):
            scorelist[0], scorelist[1] = scorelist[1], scorelist[0]
        who = other(who)
    return scorelist[0], scorelist[1]

#######################
# Phase 2: Strategies #
#######################

# Basic Strategy


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=10000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """

    def averaged(*args):
        total = 0
        for i in range(num_samples):
            total += fn(*args)
        return total/num_samples
    return averaged

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """

    average_list = []
    for n in range(1, 11):
        average = make_averaged(roll_dice)(n, dice)
        print('{} dice scores {} on average'.format(n, average))
        average_list.append(average)
    return average_list.index(max(average_list)) + 1


def max_scoring_num_rolls_noprint(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """

    average_list = []
    for n in range(1, 11):
        average = make_averaged(roll_dice)(n, dice)
        #print('{} dice scores {} on average'.format(n, average))
        average_list.append(average)
    return average_list.index(max(average_list)) + 1


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if []: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if []: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if []: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))



# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """

    if (max([int(a) for a in str(opponent_score)]) + 1) >= margin:
        return 0
    else:
        return num_rolls

debug = 0
bacon = lambda x: max([int(a) + 1 for a in str(x)])

def swap_check(score, opponent_score):
    '''Returns the score after swap if a swap occurs, and False if no 
    swap occurs'''
    if debug: print('Bacon:', bacon(opponent_score))
    score_after_bacon = score + bacon(opponent_score)

    if max(score_after_bacon, opponent_score) == 2* min(score_after_bacon, opponent_score):
        return opponent_score
    else:
        return False

def good_swap_check(score, opponent_score):
    swap_value = swap_check(score, opponent_score)
    return swap_value > score
    

def hogwild_check(score, opponent_score):
    return (score + opponent_score) % 7 == 0

def swap_strategy(score, opponent_score, margin=8, num_rolls=8):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """

    score_after_bacon = score + bacon(opponent_score)
    swap_value = swap_check(score, opponent_score)

    if debug: print('Swap value:', swap_value)

    #If rolling 0 would result in a beneficial swap, do it.
    if swap_value and swap_value > score_after_bacon:
        if debug: print(' #If rolling 0 would result in a beneficial swap, do it.')
        return 0
    #If rolling 0 would not result in a swap, but would score above the margin, do it.
    elif (not swap_value) and (bacon(opponent_score) > margin):
        if debug: print(' #If rolling 0 would not result in a swap, but would score above the margin, do it.')
        return 0
    #In all other cases, roll the default number of times.
    else:
        if debug: print(' #In all other cases, roll the default number of times.')
        return num_rolls

def get_value(roll, score, opponent_score):
    '''
    Returns the value of a given roll, taking into account the special rules.
    '''
    HOG_WILD_VALUE = 0
    new_score = roll + score
    if swap_check(new_score, opponent_score):
        if new_score > opponent_score:
            return 0
        else:
            return (opponent_score - new_score) - (score - opponent_score)
    elif (new_score + opponent_score) % 7 == 0:
        return roll + HOG_WILD_VALUE
    else:
        return roll


#probability_dict_dict = {}
#for num_rolls in range(1, 11):
#    for dice in (4, 6):
#        probability_dict_dict[(num_rolls, dice)] = get_probabilities(num_rolls, dice)
#
#with open('probdict.py', mode = 'w') as dict_file:
#    dict_file.write(r'probability_dict_dict =\ ')
#    dict_file.write(str(probability_dict_dict))

from probdict import probability_dict_dict

def average_value(num_rolls, dice, score, opponent_score):
    if num_rolls == 0:
        return get_value(bacon(opponent_score), score, opponent_score)
    else:
        average = 0
        probability_dict = probability_dict_dict[(num_rolls, dice)]
        for roll in probability_dict.keys():
            average += get_value(roll, score, opponent_score) * probability_dict[roll]
        return average

def get_five_average(score, opponent_score):
    return average_value(5, 4 if (score + opponent_score)%7 == 0 else 6, score, opponent_score)

def get_future_value(roll, score, opponent_score):
    present_value = get_value(roll, score, opponent_score)
    return present_value - get_five_average(opponent_score, score+present_value)

def average_future_value(num_rolls, dice, score, opponent_score):
    if num_rolls == 0:
        return get_future_value(bacon(opponent_score), score, opponent_score)
    else:
        average = 0
        probability_dict = probability_dict_dict[(num_rolls, dice)]
        for roll in probability_dict.keys():
            average += get_future_value(roll, score, opponent_score) * probability_dict[roll]
        return average

    
#average_dict = {}
#
#for num_rolls in range(11):
#    print(num_rolls)
#    for dice in (4, 6):
#        for score in range(100):
#            for opponent_score in range(100):
#                average_dict[(num_rolls, dice, score, opponent_score)] =\
#                        average_future_value(num_rolls, dice, score, opponent_score)
#
#with open('average_dict.py', mode = 'w') as dict_file:
#    dict_file.write(r'average_dict =')
#    dict_file.write(str(average_dict))


from average_dict import average_dict



def final_strategy_shit(score, opponent_score):
    """A brief description of my strategy.
    """

    
    dice = 4 if (score + opponent_score)%7 == 0 else 6
    average_list = []
    for n in range(11):
        average_list.append(average_dict[(n, dice, score, opponent_score)])
    return average_list.index(max(average_list))
def final_strategy(score, opponent_score):
    final = final_strategy_shit(score, opponent_score)
    terrible = average_value(final, 4 if (score + opponent_score)%7==0 else 7, score, opponent_score)
    def bacon_threshold():
        return -2 if opponent_score >= score else 0

    if good_swap_check(score + bacon(opponent_score), opponent_score) or\
            (score + bacon(opponent_score) + opponent_score) % 7 == 0 or\
            bacon(opponent_score) > terrible + bacon_threshold():
        return 0
    else: return final

    

    
run_experiments()
    



##########################
# Command Line Interface #
##########################


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
