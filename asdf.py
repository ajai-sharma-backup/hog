def str_base(number,base):
    def digit_to_char(digit):
        if digit < 10:
            return str(digit)
        return chr(ord('a') + digit - 10)
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)

def chances(num_rolls, dice):
    data = {}
    for n in range(dice**num_rolls):
        print(n)
        combo = str_base(n, dice)
        if '0' in combo:
            result = 1
        else:
            result = sum([int(d) + 1 for d in combo])
        try:
            data[result] += 1
        except: 
            data[result] = 1
    data = {key : value/(dice**num_rolls -1) for key, value in data.items()}
    for i in data.items():
        print("{}:  {}".format(i))
    return data

chances(10, 6)
