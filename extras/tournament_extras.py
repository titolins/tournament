#!/usr/bin/env python
#
# tournament_extras.py -- implementation of a Swiss-system tournament
# 
# This file contains the methods corresponding to the extra credits requirements
#

import psycopg2

from random import randrange

# Defining static values for the indexes of the playerStandings() return value.
# For example, consider the following:
#
#   standings = playerStandings()
# 
# You may now print all the players info  with the following for loop (using the
# statics instead of the raw index numbers makes for a clearer code):
#
#   for player in standings:
#       print player[ID], player[NAME], player[WINS], player[MATCHES]
#
ID = 0
NAME = 1
MATCHES = 2
WINS = 3
DRAWS = 4
BYES = 5


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    sql = "delete from matches"
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    sql = "delete from players"
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    sql = "select count(*) from players where tournament_id = (%s)"
    tournamentId = getCurrentTournament()

    conn = connect()
    c = conn.cursor()
    c.execute(sql, (tournamentId,))
    row = c.fetchall()
    conn.close()
    return row[0][0]
     

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    sql = "insert into players (name, tournament_id) values (%s, %s)"
    tournamentId = getCurrentTournament()

    conn = connect()
    c = conn.cursor()
    c.execute(sql, (name, tournamentId,)) 
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    sql = "select * from standings"
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.close()
    return rows


def getCurrentTournament():
    """Returns the id of the current played tournament
    """
    sql = "select max(id) from tournaments"
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.close()
    return rows[0][0]


def startNewTournament():
    """Creates a new tournament in the db
    """
    sql = "insert into tournaments default values"
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()


def getMatches():
    """Returns a list of tuples containing the players and winner of each match
    reported.

    """
    sql = "select * from matches"
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.close()

    return rows


def getMaxByeCount():
    """Returns the greater number of byes any player has been awarded with
    """
    sql = "select max(byes) from standings"
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.close()

    return rows[0][0]


def getNumOfPlayersWithMaxByes():
    """Returns the number of players awarded with the greater number of bys
    """
    sql = """
    select count(id) from standings where byes = (select max(byes) from 
    standings)
    """
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.close

    return rows[0][0]

def getMinScore():
    """Returns the minimum score from a player in the standings
    """
    sql = "select min(wins) from standings"
    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.close
    return rows[0][0]


def selectRoundPlayers():
    """Returns a list of tuples containing the current standings of players.

    If there is a odd number of players, one of them will be chosen to get a
    bye round, which counts as a win. The standings will then be modified, 
    removing the chosen player from it and returning the rest.

    A player may only be awarded with a bye if all other players have a equal
    or greater number of byes.
    """
    # get the number of players registered
    numOfPlayers = countPlayers()
    # get the current standings
    standings = playerStandings()

    # if there is a even number of players, there is no need for awarding anyone
    # a bye, so we simply return the current standings
    if (numOfPlayers % 2 == 0):
        return standings

    # else, we need to choose a player to be awarded with a bye turn
    else:

        # first we get the greater number of byes any player has been awarded 
        # with as of now
        byeThreshold = getMaxByeCount()

        # then we get the number of players which received the greater number of 
        # byes
        numOfPlayersWithMaxByes = getNumOfPlayersWithMaxByes()

        # then we create a list which will receive the ids of the players that 
        # may be awarded a bye turn
        eligibleIds = []

        # if all players have received the max number of byes, then anyone is
        # suitable for receiving a bye
        if numOfPlayersWithMaxByes == numOfPlayers:
            # anyone can receive a bye, so we add all ids to the list 
            for player in standings:
                eligibleIds.append(player[ID])

        # otherwise, we have to check which players are eligible to receive a
        # bye turn (which are those closer to the minScore that have 
        # byes < byeThreshold)
        else:
            players = []
            minScore = getMinScore()
            for player in standings:
                if player[BYES] < byeThreshold:
                   # this player may be eligible for receiving a bye this round
                   players.append(player)
                   #eligibleIds.append(player[ID])

            # then we select the players with lesser wins from those selected
            # above
            while len(eligibleIds) == 0:
                for player in players:
                    if player[WINS] == minScore:
                        eligibleIds.append(player[ID])
                minScore += 1


        # choose the player who will get a bye turn
        # if there is only one eligible id, then that is the one
        if (len(eligibleIds) == 1):
            selectedId = eligibleIds[0]

        # else, choose a random id from the list of ids
        else:
            selectedId = eligibleIds[randrange(len(eligibleIds))]

        # we have to iterate through the standings once again to remove
        # the chosen player from the standings to be returned. 
        for i in xrange(0, len(standings)):
            if (standings[i][ID] == selectedId):
                standings.remove(standings[i])
                # then we append only the selected id to the end of the standings
                # at the swisspairings method we will retrieve this to report
                # the bye match
                standings.append(selectedId)
                break
            

        return standings


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    This method complies with the extra credits requirements, meaning that it
    does not repeat matches and also takes into account a odd number of players. 
      
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name

        or

        An empty list, if the tournament is over
    """

    # first, we get the standings
    standings = selectRoundPlayers()

    # then, we check if the tournament has ended
    if isTournamentOver():
        return []

    # if there are more matches to be played, we check if we have a even or odd 
    # number of players
    numOfPlayer = countPlayers()
    if countPlayers() % 2 == 0:
        hasOddPlayers = False
    else:
        hasOddPlayers = True
        # if odd, we grab the id of the player elected to get a bye
        selectedByeId = standings.pop()

    # then we get the matches. we need this to check if we have a valid pair
    matches = getMatches()

    validPairings = False

    offsetCount = 0

    while not validPairings:
        pairings = []
        for i in xrange(0, len(standings)):
            firstPlayer = standings[i]

            # we start by assuming that we have a valid first player
            validFirstPlayer = True

            # then we check if player hasn't already been paired
            for firstId, firstName, secondId, secondName in pairings:
                if firstPlayer[ID] == firstId or firstPlayer[ID] == secondId:
                    # if he has been paired, we increment the index counter,
                    # set the valid to false and break the pairings loop
                    validFirstPlayer = False
                    break
            
            # if we do not have a valid first player we have to continue and
            # chose another one
            if not validFirstPlayer:
                continue

            # if we have a valid first player, we choose the second player
            for j in xrange(offsetCount, len(standings)):
                secondPlayer = standings[j]

                # if we get the same player, we just skip
                if firstPlayer[ID] == secondPlayer[ID]:
                    continue

                # same things as for the first player (check if it has already been
                # paired)
                validSecondPlayer = True
                for firstId, firstName, secondId, secondName in pairings:
                    if (secondPlayer[ID] == firstId or 
                        secondPlayer[ID] == secondId):

                        validSecondPlayer = False

                if not validSecondPlayer:
                    continue

                else:
                    break

            # now we should have two players who have not been paired yet for this
            # round, but we still need to check if they already have played against
            # each other

            validPair = True
            for firstId, secondId, winner in matches:
                if ((firstPlayer[ID] == firstId and secondPlayer[ID] == secondId) or
                    (firstPlayer[ID] == secondId and secondPlayer[ID] == firstId)):
                    validPair = False

            # if the selected players have not played against each other, we create
            # the pair tuple and append to the list of pairings
            if validPair:
                pair = (firstPlayer[ID], firstPlayer[NAME], secondPlayer[ID], 
                        secondPlayer[NAME])
                pairings.append(pair)

            # if they have played, skip and start over
            else:
                continue

        # we lastly check if we have the correct number of pairings. If we dont,
        # it means that the regular pairing (one player against the other
        # immediatelly after him in the standings) does not work. If that's the
        # case, we clear the pairings list and start over, but now we increment
        # the offset for chosing the second player
        if len(pairings) != len(standings)/2:
            validPairings = False
            offsetCount += 1
            if offsetCount >= len(standings):
                offsetCount = 0
        else:
            validPairings = True
            break

    # lastly, we have to report the bye match if we have a odd number of players
    if hasOddPlayers:
        reportMatch(selectedByeId, -1, selectedByeId)

    return pairings
                         

def reportMatch(id_1, id_2, result):
    """Records the outcome of a single match between two players. This is the
    extra credits version, meaning that it supports draws. 

    Args:
      id_1:  the id number of the first player
      id_2:  the id number of the second player or -1 if it is a bye round
      result: the id of the winner or -1 if it is a bye round or 0 if it is a
              draw
    """
    sql = "insert into matches (id_1, id_2, winner) values (%s, %s, %s)"
    conn = connect()
    c = conn.cursor()
    c.execute(sql, (id_1, id_2, result,))
    conn.commit()
    conn.close()


def isTournamentOver():
    """ Returns True if all players have played all rounds, False otherwise
    """
    standings = playerStandings()
    numOfRoundsToEnd = rounds(countPlayers())

    for player in standings:
        if player[MATCHES] < numOfRoundsToEnd:
            return False

    return True


def rounds(numOfPlayers):
    """ returns the number of rounds a tournament must have based of number of
    players.
    taken from:
    http://magic.wizards.com/en/game-info/products/magic-online/swiss-pairings
    """
    if numOfPlayers <= 2:
        numOfRounds = 1
    elif numOfPlayers <= 4:
        numOfRounds = 2
    elif numOfPlayers <= 8:
        numOfRounds = 3
    elif numOfPlayers <= 16:
        numOfRounds = 4
    elif numOfPlayers <= 32:
        numOfRounds = 5
    elif numOfPlayers <= 64:
        numOfRounds = 6
    elif numOfPlayers <= 128:
        numOfRounds = 7
    elif numOfPlayers <= 212:
        numOfRounds = 8
    elif numOfPlayers <= 384:
        numOfRounds = 9
    elif numOfPlayers <= 672:
        numOfRounds = 10
    elif numOfPlayers <= 1248:
        numOfRounds = 11
    elif numOfPlayers <= 2272:
        numOfRounds = 12
    else:
        numOfRounds = 13

    return numOfRounds


def printWinner():
    """Prints the tournament winner if the tournament has ended. Else, prints a
    message warning that the tournament is not yet over.
    """
    if isTournamentOver():
        print 'Winner id =', playerStandings()[0][0]
    else:
        print 'Tournament not over yet'
