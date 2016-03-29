#!/usr/bin/python
#filename: recommendations.py
#author: warrior
#mail: 15933533880@163.com

#test data someone's evaluate on some films at dic form
critics = {
        'Lisa Rose':{
            'Lady in the water':2.5, 'Snakes on a plane':3.5, 
            'Just my luck':3.0, 'Superman returns':3.5,
            'You, me and dupree':2.5, 'The night listenser':3.0
            },
        'Gene Seymour':{
            'Lady in the water':3.0, 'Snakes on a plane':3.5, 
            'Just my luck':1.5, 'Superman returns':5.0,
            'You, me and dupree':3.0 ,'The night listenser':3.5
            },
        'Michael Phillips':{
            'Lady in the water':2.5, 'Snakes on a plane':3.0, 
            'You, me and dupree':3.5, 'The night listenser':4.0 
            },
        'Claudia puig':{
            'Snakes on a plane':3.5, 
            'Superman returns':4.0,
            'You, me and dupree':2.5, 'The night listenser':4.5
            },
        'Mick LaSalle':{
            'Lady in the water':3.0, 'Snakes on a plane':4.0, 
            'Just my luck':2.0, 'Superman returns':3.0,
            'You, me and dupree':3.0, 'The night listenser':2.0
            },
        'Jack Matthews':{
            'Lady in the water':3.0, 'Snakes on a plane':4.0, 
            'Superman returns':5.0,
            'You, me and dupree':3.5 ,'The night listenser':4.0
            },
        'Toby':{
            'Snakes on a plane':4.5, 
            'Just my luck':4.5, 'Superman returns':4.0,
            'You, me and dupree':1.0, 'The night listenser':2.5
            }
        }

#calculate the similar distance
#input: 
#   prefs,person1,person2
#output:
#   distance of similar of evaluate

from math import sqrt
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    if len(si) == 0: return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2)
        for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))

#calculate the similar coefficient
#input: 
#   prefs,person1,person2
#output:
#   return the pearson similar coefficient
def sim_pearson(prefs,p1,p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    
    n = len(si)

    if n==0: return 1

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])


    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])

    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])


    num = pSum-(sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

    if den == 0 :   
        return 0
    else :
        r = num/den

    return r

#get the top similar ones
#input: 
#   prefs,person,n,similarity
#output:
#   return top similar n persons 
def topMatches(prefs,person,n=3,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other) 
            for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]




#get the top evaluate ones
#input: 
#   prefs,person,n,similarity
#output:
#   return top evaluate n ones
def getRecommendations(prefs, person, n=3,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        if other == person : continue
        sim = similarity(prefs,person,other)

        if sim<=0:continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim

                simSums.setdefault(item,0)
                simSums[item]+=sim

    rankings = [(total/simSums[item],item) for item ,total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings[0:3]

#transform the item of dic
#input: 
#   dic
#output:
#   return the transformed dic
def transformDic(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            result[item][person] = prefs[person][item]

    return result





