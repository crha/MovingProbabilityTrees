import decimal
import math

# return a map that contains the key of how many success were obtained and the probability as its odds of occuring
# a hashmap variable will add the pair if it does not exist or add it the probability to its existing probability if it does
#
# depth is how deep the recursion goes, ie: how many coin flips we do
# start percent is just the success rate percent we start at
# max percent is the highest that the success rate can go
# min percent is the lowest that the success rate can go
# success change is what is added to the success rate if the node succeeds
# failure change is what is added to the succes rate if the node fails
#
# we return a hashmap that contains the number of successes as a key and the probability we can attain that amount of successes as its value
def probabilities(depth, start_percent, max_percent, min_percent, success_change, failure_change):
    max_percent = min(max_percent, decimal.Decimal(str("1.0")))
    min_percent = max(min_percent, decimal.Decimal(str("0.0")))

    output_map = {}
    start_percent = decimal.Decimal(str(start_percent))
    max_percent = decimal.Decimal(str(max_percent))
    min_percent = decimal.Decimal(str(min_percent))
    success_change = decimal.Decimal(str(success_change))
    failure_change = decimal.Decimal(str(failure_change))
    total_percent = decimal.Decimal(str(1))
    probabilities_helper(depth, start_percent, max_percent, min_percent, success_change, failure_change, total_percent, output_map, 0)
    return output_map
    


# current percent is the current success rate percent
# total percent is the total probability that we take this exact route to the current node
# output map is just the map that contains a key of successes and its values are the probability we can attain that amount of successes
# successes are just to keep track of how many successes we have achieved so far
#
# nothing to return
def probabilities_helper(depth, current_percent, max_percent, min_percent, success_change, failure_change, total_percent, output_map, successes):
    # print("depth: " + str(depth))
    # print("current_percent: " + str(current_percent))
    # print("total_percent: " + str(total_percent))
    # print("successes: " + str(successes))
    # print()

    if depth <= 0:
        if successes in output_map:
            output_map[successes] += total_percent
        else:
            output_map[successes] = total_percent
        return
    
    if current_percent < min_percent:
        current_percent = min_percent
    elif current_percent > max_percent:
        current_percent = max_percent

    #success node
    probabilities_helper(depth-1, current_percent+success_change, max_percent, min_percent, success_change, failure_change, total_percent*current_percent, output_map, successes+1)
    
    #failure node
    probabilities_helper(depth-1, current_percent+failure_change, max_percent, min_percent, success_change, failure_change, total_percent*(decimal.Decimal(str(1)) - current_percent), output_map, successes)



def calc_stats(map):
    # Calculate the mean (expected value)
    mean = sum(successes * prob for successes, prob in map.items())

    # Calculate the variance
    variance = sum(prob * ((successes - mean) ** 2) for successes, prob in map.items())

    # Calculate the standard deviation
    standard_deviation = math.sqrt(variance)

    return standard_deviation, variance, mean



def calc_iqr(map):
    total = decimal.Decimal("0.0")
    sorted_probabilities = []
    q1,q2,q3 = -1,-1,-1

    for i in map.keys():
        sorted_probabilities.append([i,map[i]])
    sorted_probabilities = sorted(sorted_probabilities, key=lambda x: x[0], reverse=False)

    for probs in sorted_probabilities:
        total += probs[1]
        if total > decimal.Decimal("0.25") and q1==-1:
            q1 = probs[0]
        elif total > decimal.Decimal("0.50") and q2==-1:
            q2 = probs[0]
        elif total > decimal.Decimal("0.75") and q3==-1:
            q3 = probs[0]

    return q1,q2,q3