import string
import itertools

__author__ = 'Chris'

import random
import copy




# voters are index with v  (0  to V - 1)
# candidates are index with c (0 to C - 1)
# ranks are indexed with with r (o to C-1)

# preferences[v][c] will be the value voter v assigns candidate c
# holds values
global preferences

# rank[v] will be the ranking of candidates of voter v
# these values will be from 0 to C-1 and the order determines their rank
# holds candidate indices
global rank



# stillIn[c] will be true if candidate c is still in the running, else false
global stillIn


# oRank[c][r] will be the number of time candidate c is ranked r
global oRank

# the majority graph
# mg[c1][c2] is the number of times c1 beats c2 (the number of times c1 ranks above c2 in the overall ranking)
global mg



# constructs a majority graph using the ranking from "rank"
# SEE mg
def constructMajorityGraph():
    global mg
    mg = [None] * len(rank[0])
    for v in range(len(rank)):
        for r1 in range(len(rank[0])):
            c1 = rank[v][r1]
            if mg[c1] is None:
                mg[c1] = [0] * len(rank[0])
            for r2 in range(r1 + 1, len(rank[0])):
                c2 = rank[v][r2]
                mg[c1][c2] +=1




# uses rank to generrate oRank (rank and oRank)
def rankToORank():
    global oRank
    oRank = [None] * len(rank[0])
    for v in range(len(rank)):
        for r in range(len(rank[0])):
            c = rank[v][r]
            if oRank[c] is None:
                oRank[c] = [0] * len(rank[0])
            oRank[c][r] += 1


# Randomly generates preferences for V voters over C candidates
# by assigning each candidate, c (0 to C-1), V randomly generated integers from 0 to maxWeight
def randomInit(V, C, maxWeight):

    maxWeight = int(maxWeight)

    global preferences
    preferences = []

    for v in range(V):
        preferences.append([])
        for c in range(C):
            preferences[v].append(random.randint(0, maxWeight))


# accepts user entered weights for the specified number of voters and canadidates
def userEnterRanks():
    V = int(input('How many voters?  '))
    C = int(input('How many candidates?  '))

    global rank
    rank = []

    for v in range(V):
        ranking = raw_input('Enter voter ' + str(v) +'s preferences as a ranking of the ' + str(C) +' candidates. Must be a list of integers from 0 to ' + str(C-1) + '  ')
        ranking = str.split(ranking)

        assert len(ranking) == C

        rank.append([])
        for cs in range(len(ranking)):
            c = int(ranking[cs])
            assert c <= C
            rank[v].append(c)



# converts preferences(weights assigned to each candidate by each voter)
# to a set of rankings representing the overall preferences for the voters
def prefToRank():

    global rank
    rank = []

    tmp = copy.deepcopy(preferences)
    for v in range(len(preferences)):
        for c in range(len(preferences[0])):
            tmp[v][c] = (c, tmp[v][c])

    # for each voter, sort by the preferences assigned to each candidate
    # then add the candidate index in that order to the rank for each voter

    for v in range(len(preferences)):
        tmp[v].sort(key=lambda tup:tup[1], reverse=True)
        rank.append([])
        for tuple in tmp[v]:
            rank[v].append(tuple[0])


# calculates the slater rank for each permutation of the candidates using the majority graph
# and orders them by the rank
def calcSlater():

    global  slater

    candidates = []
    for c in range(len(rank[0])):
        candidates.append(c)

    perms = itertools.permutations(candidates)

    # keys are permutations of the candidates (possible rankings)
    # values are the slater rank (number of times the permutation disagrees with the majority graph)
    candSlaterRankings = {}
    for possRank in perms:
        for r1 in range(len(possRank)):
            for r2 in range(r1+ 1, len(possRank)):

                c1 = possRank[r1]
                c2 = possRank[r2]

                # in this permutation, c1 beats c2

                # if positive, c1 beats c2 in majority graph
                # if negative, c2 beats c1
                # so if negative slater ranking gets 1 added to it (the ranking disagrees with the majority graph)
              #  print(mg[c1][c2])
               # print(mg[c2][c1])
               # print(' ')
                c1ToC2 = mg[c1][c2] - mg[c2][c1]

                if possRank not in candSlaterRankings:
                    candSlaterRankings[possRank] = 0
                if c1ToC2 < 0:
                    candSlaterRankings[possRank] += 1

    # possible rankings sorted by the slater rank
    # first one is the best

    sortedSlaterRankingsWithRank= sorted(candSlaterRankings.items(), key=lambda x:x[1])

    return sortedSlaterRankingsWithRank

# gets the best slater ranking (the one with the fewest differences between it and the majority graph)
# just the first element of the ordered list of permutations
def slaterRankingFromSlaterPerms(sortedSlaterRankingsWithRank):
    return sortedSlaterRankingsWithRank[0][0]


# calculates the borda ranking
# returns a 2D array of length [C][2], C is the number of candidates
# borda[c][1] is the candidate index (c)
# borda[c][0] is the borda weight for the candidate
def calcBorda():

    V = len(rank)
    C = len(rank[0])

    borda = [] * C

    for r in range(C):
        borda.append([0] * 2)
    for r in range(C):
        for v in range(V):
            borda[rank[v][r]][0] += C - r -1
            borda[rank[v][r]][1] = rank[v][r]


    borda.sort(reverse = True)
    return borda

# gets the borda ranking without the weights
def bordaRankingFromBorda(borda):

    C = len(borda)
    ranking = []

    for c in range(C):
        ranking.append(borda[c][1])

    return ranking

# prints a 2D array as a table
def print2DArray(twoDArray, title):

    print(title)
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
      for row in twoDArray]))



V = 3
C = 6
maxWeight = 10



randomInit(V, C, maxWeight)


# prints these randomly generated preferences in a table
print2DArray(preferences, 'Random Preferences:')

# converts
prefToRank()
print2DArray(rank, 'Rank from random Preferences:')


#rankToORank()
#print2DArray(oRank, 'Overall Rank from Rank from random Preferences:')


constructMajorityGraph()

print2DArray(mg, 'Majority Graph from Rank from random preferences:')



print('Slater ranking from random preferences:')
sRankPerms = calcSlater()
print(sRankPerms)
slaterRank = slaterRankingFromSlaterPerms(sRankPerms)
print(slaterRank)

print('Borda ranking from random preferences')
bordaWithWeight = calcBorda()
print(bordaWithWeight)
bordaRank = bordaRankingFromBorda(bordaWithWeight)
print(bordaRank)



print('Slater and Borda Rankings from random preferences')
print('SLATER:')
print(slaterRank)
print('BORDA:')
print(bordaRank)


overallTable = []

slaterRank = list(slaterRank)
slaterRank.insert(0, 'SLATER ')
bordaRank.insert(0, 'BORDA ')


overallTable.append(slaterRank)
overallTable.append(bordaRank)

overallTable = zip(*overallTable)

print('')

print2DArray(overallTable, 'OVERALL from random preferences')

print('\n\n\n')


userEnterRanks()
print2DArray(rank, 'User entered rankings:')




constructMajorityGraph()
print2DArray(mg, 'Majority Graph from user entered rankings:')



print('Slater ranking from user entered rankings:')
sRankPerms = calcSlater()
print(sRankPerms)
slaterRank = slaterRankingFromSlaterPerms(sRankPerms)
print(slaterRank)

print('Borda ranking from user entered rankings')
bordaWithWeight = calcBorda()
print(bordaWithWeight)
bordaRank = bordaRankingFromBorda(bordaWithWeight)
print(bordaRank)



print('Slater and Borda Rankings from user entered rankings:')
print('SLATER:')
print(slaterRank)
print('BORDA:')
print(bordaRank)


overallTable = []

slaterRank = list(slaterRank)
slaterRank.insert(0, 'SLATER ')
bordaRank.insert(0, 'BORDA ')


overallTable.append(slaterRank)
overallTable.append(bordaRank)

overallTable = zip(*overallTable)
print('')
print2DArray(overallTable, 'OVERALL from user enetered rankings')
