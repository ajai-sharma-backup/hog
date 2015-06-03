def generalized_pascal(n, rows):
    '''
    Generates n rows of a generalized pascal's triangle with 
    first row n long. Each entry is the sum of n entries above it.
    The entries relate to the probability of rolling a number in hog.
    '''
    def get_entry(row, index):
        '''Returns the entry for indices 0<=index<=len, and 0 for other numbers.'''
        try: 
            if index < 0:
                raise ValueError
            else:
                return row[index]
        except:
            return 0
    def get_next_row(row, n=n):
        new_row = []
        for i in range(len(row) + n - 1):
            new_entry = sum([get_entry(row, i - k) for k in range(n)])
            new_row.append(new_entry)
        return new_row
            
    triangle = [[1] * n]
    for i in range(rows-1):
        triangle.append(get_next_row(triangle[-1]))

    return triangle


def print_triangle(triangle):
    for line in triangle:
        for n in line:
            print(n, end=' ' )
        print('\n')
        
def sanity_check(rolls, dice):
    print('Dice: ', dice, 'Rolls: ', rolls)
    pascal = generalized_pascal(dice - 1, rolls )
    try:
        assert len(pascal[0]) == dice - 1
        pascal_list = pascal[-1]

        prob_list = [n/(dice**rolls) for n in pascal_list]

        result = sum(prob_list) + wun(rolls, dice)
        print(result)
    except:
        print('failure')
        print(pascal)

def get_probabilities(rolls, dice):
    '''
    Returns a dictionary with the probabilities of rolling each number
    in hog, given a number of rolls and a die. 
    '''
    pascal_list = generalized_pascal(dice - 1, rolls )[-1]
    pascal_list = [n/(dice**rolls) for n in pascal_list]
    probability_dict = { n : 0 for n in range(1, rolls*dice + 1) }
    probability_dict[1] = wun(rolls, dice)
    for n in range(len(pascal_list)):
        probability_dict[rolls*dice - n] = pascal_list[n]
    return probability_dict


def wun(rolls, dice):
    w = 1/dice
    for i in range(rolls):
        w = ((dice - 1)*w + 1)/dice
    return w



