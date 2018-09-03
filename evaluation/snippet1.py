import random
        
# roll dice, with variable a the number of sides of the dice
# and variable b the times you may roll the dice
def roll_dice(a, b):
    number_of_dice_to_roll = 0
    while number_of_dice_to_roll < b:
        print random.randint(0, a)
        number_of_dice_to_roll = number_of_dice_to_roll + 1
    return "That's all!"

# returns a new list with the cumulative sum of a list
def cumulative_sum(number_list):
    # number_list is a list of numbers
    new_list = []
    sum = 0
    for i in number_list:
        sum += i
        new_list.append(sum)
        
    return new_list

# sum_of_list takes a list as a argument and sums all the elements
def sum_of_list(n):
    sum = 0
    for i in n:
        sum += i
    
    return sum

# finds the position of a element in a list that is equal with a value
def find_position(a, b):
    positie = 0
    while positie < len(b):
        if b[positie] == a:
            return positie + 1 # er wordt er 1 bij opgeteld want het gaat om de plaats
        positie = positie + 1
            
    return None        

# finds maximum value of a list
def find_maximum(list):
    max_number = 0
    for i in list:
        # tweede variabele, zo werkt de code ook voor negatieve elementen in de lijst
        max_number2 = i 
        # or statement vervangt de waarde van max_number ten alle tijde door eerste element in de lijst
        if max_number2 > max_number or max_number == 0 and i != 0: 
            max_number = max_number2
    
    return max_number