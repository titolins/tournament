#!/usr/bin/env python
#
# Test cases for the tournament_extras.py

from tournament_extras import *


def beginTournamentOfFive():
    startNewTournament();
    registerPlayer("a")
    registerPlayer("b")
    registerPlayer("c")
    registerPlayer("d")
    registerPlayer("e")
    print("tournament of five begun!")


def beginTournamentOfSeven():
    startNewTournament();
    registerPlayer("a")
    registerPlayer("b")
    registerPlayer("c")
    registerPlayer("d")
    registerPlayer("e")
    registerPlayer("f")
    registerPlayer("g")
    print("tournament of seven begun!")


def beginTournamentOfNine():
    startNewTournament();
    registerPlayer("a")
    registerPlayer("b")
    registerPlayer("c")
    registerPlayer("d")
    registerPlayer("e")
    registerPlayer("f")
    registerPlayer("g")
    registerPlayer("h")
    registerPlayer("i")
    print("tournament of nine begun!")


def playTournament():
    pairings = swissPairings()
    while len(pairings) != 0:
        for firstId, firstName, secondId, secondName in pairings:
            reportMatch(firstId, secondId, firstId)

        pairings = swissPairings()


def checkForRepeatedMatches():
    matches = getMatches();
    counter = 0
    for i in xrange(0, len(matches)):
        for j in xrange(i+1, len(matches)):
            if ((matches[i][0] == matches[j][0] and matches[i][1] == matches[j][1]) or
                (matches[i][0] == matches[j][1] and matches[i][1] == matches[j][0])):
                print 'Match repeated'
                counter += 1

    if counter == 0:
        print 'No repeated matches'
        return False
    else:
        print counter, 'repeated matches'
        return True


if __name__ == '__main__':
    beginTournamentOfNine()
    playTournament()
    tournamentHasRepeatedMatches = checkForRepeatedMatches()
    if tournamentHasRepeatedMatches:
        print 'Error! Tournament invalid. Repeated matches'
    else:
        print 'Tournament well played and over!'
        printWinner()


