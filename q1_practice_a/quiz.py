# NO IMPORTS!

##################################################
##  Problem 1
##################################################

def trailing_weighted_average(S, W):
    A = []

    m = len(S) 
    i = 0
    while i < m:
        average = 0
        for k in range(len(W)):
            if i-k <= 0: 
                average += W[k] * S[0]
            else: 
                average += W[k] * S[i-k]
        i+=1
        A.append(average)

    return A


##################################################
##  Problem 2
##################################################

def all_consecutives(vals, n):

    result = set()
    seq = sorted(vals) # <-- returns a new sorted list from a given iterable, set, tuple, string, dict  
    for i in range(len(seq)-n+1):
        if seq[i]+n-1 == seq[i+n-1]: 
            result.add(tuple(seq[i:i+n]))
    return result 

    # result = set()
    # for a_value in vals:
    #     temp = []
    #     for val in vals:
    #         if val < a_value: continue  
    #         if abs(val - a_value) < n:
    #             temp.append(val)
    #     if len(temp) < n: continue # if not enough numbers
    #     temp.sort()
    #     for i in range(len(temp)-1):
    #         if temp[i]+1 != temp[i+1]: continue # if not consecutive
    #     result.add(tuple(temp))

    # return result


##################################################
##  Problem 3
##################################################

def cost_to_consume(seq1, seq2):

    if not seq1 or not seq2:
        return len(seq1) + len(seq2)

    if seq1[0] == seq2[0]:
        return cost_to_consume(seq1[1:], seq2[1:])

    return 1 + min(cost_to_consume(seq1[1:], seq2[1:]), 
                    cost_to_consume(seq1, seq2[1:]), 
                    cost_to_consume(seq1[1:], seq2))

    # shorter = None
    # longer = None
    # diff = len(seq1) - len(seq2)
    # if diff >= 0:
    #     shorter = seq2
    #     longer = seq1 
    # else: 
    #     diff = abs(diff) # make sure diff is positive
    #     shorter = seq1
    #     longer = seq2

    # compare = []
    # offset = 0 
    # while offset <= diff: 
    #     score = 0 
    #     for i in range(len(shorter)): # compare each position
    #         if longer[i + offset] != shorter[i]: 
    #             score += 1 # if positions differ socre + 1
    #     compare.append((score, offset))
    #     offset += 1
    # compare.sort(key=lambda x: x[0]) # sort by score

    # opt_offset = compare[0][1] # optimal positioning
    # cost = 0
    # for i in range(len(longer)): 
    #     if i == len(shorter): # if shorter is depleted
    #         cost += len(longer) - i # add cost to consume the remaining of longer
    #     elif longer[i + opt_offset] != shorter[i]:
    #         score += 1 # if positions differ socre + 1
        
    # return opt_cost


if __name__ == "__main__":
	pass