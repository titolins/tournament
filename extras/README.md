################################################################################
################################################################################
#                                                                              #
#                  Udacity FullStack WebDeveloper Nanodegree                   #
#                                                                              #
#                            Tournament Project                                #
#                                                                              #
################################################################################
################################################################################

#### This is the readme for the Tournament Project, second project required for
obtaining the full stack web developer nano degree from udacity:         

##### http://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004 


 > Description
--------------------------------------------------------------------------------

 - The aim of this project is to create an api to access and  manage data from a 
   tournament based on the swiss pairings system.

 - The tournament_extras.sql file contains the sql statements for preparing the 
   database. 

 - The api code is contained in the tournament_extras.py file, and allows you to
   register new players, count the players registered, delete all matches and
   players records, count players registered, view the player standings, report
   a match, request the swiss pairings for the round, etc.

 - This is the extra credits implementation of the tournament api and as such it 
   has a few extra functionalities. For example, it supports a odd number of 
   players, more than one tournament, does not repeat matches, etc.

 - To support odd players, we have to give a player a 'bye' match every round.
   A bye match counts as a win, but does not count as a opponent match win. To
   pick the player who is awarded with a bye turn, we first select the players
   with lesser score and byes. If a player has more wins than the minimum win
   count from any other player in the tournament, he will not be eligible to be
   awarded with a bye match unless his bye count is lesser than every other one.


 > Requirements
--------------------------------------------------------------------------------

 - Python
    * https://www.python.org/downloads/
 
 - psycopg -- python module for connecting with postgresql databases
    * http://initd.org/psycopg/
    
 - PostgreSQL
    * http://www.postgresql.org/


 > Instructions
--------------------------------------------------------------------------------

 - First of all, prepare your database:
    * After installing and configuring postgresql, you will need to connect to
      it and import the schema from the .sql file, as follows:

            `
            $ psql
            => create database tournament;
            => \c tournament
            => \i tournament_extras.sql
            CREATE TABLE
            CREATE TABLE
            CREATE TABLE
            CREATE VIEW
            `

    * The standings view created above may be used to get the player standings.
            
 - Now that your database is prepared, you may use any of the app 
   functionalities from a python interpreter. e.g. using the command line start
   playing a new tournament:
            
            `
            $ python
            >>> from tournament_extras import *

            >>> # **IMPORTANT** Don't forget to start a tournament before
            >>> # registering the players
            >>> startNewTournament()

            >>> registerPlayer("Markov Chaney") 
            >>> registerPlayer("Joe Malik") 
            >>> registerPlayer("Mao Tsu-hsi")
            >>> registerPlayer("Atlanta Hope")
            >>> registerPlayer("Melpomene Murray")
            >>> countPlayers()
            5L
            >>> playerStandings()   # returns (id, name, matches, wins, draws 
                                    # and byes) for each player    

            # id |    name    |  m | w | d | b |
            [(4, 'Atlanta Hope', 0L, 0L, 0L, 0L), 
            (3, 'Mao Tsu-hsi', 0L, 0L, 0L, 0L), 
            (2, 'Joe Malik', 0L, 0L, 0L, 0L), 
            (1, 'Markov Chaney', 0L, 0L, 0L, 0L),
            (5, "Melpomene Murray", 0L, 0L, 0L, 0L)]

            >>> swissPairings() # returns (id_1, name_1, id_2, name_2) for each
                                # match to occur the next round

            [(4, 'Atlanta Hope', 3, 'Mao Tsu-hsi').
            (2, 'Joe Malik', 1, 'Markov Chaney)]

            >>> # As you may have noted, player 5 is not in the pairings. The
            >>> # reason for this is that he was the player awarded with a 'bye'
            >>> # swissPairings() already reports his bye match, so there is no
            >>> # need for you to do that.

            >>> reportMatch(4, 3, 4)  # reportMatch() takes three arguments:
            >>> reportMatch(2, 1, 0)  # (firstPlayerId, secondPlayerId, result)
                                      # result is the id of the winner or 0, if 
                                      # it is a tie
            >>> playerStandings()
            
            # id |   name      | m | w | d | b
            [(4, 'Atlanta Hope', 1L, 1L, 0L, 0L), 
            (5, "Melpomene Murray", 1L, 1L, 0L, 1L),
            (2, 'Joe Malik', 1L, 0L, 1L, 0L), 
            (1, 'Markov Chaney', 1L, 0L, 1L, 0L),
            (3, 'Mao Tsu-hsi', 1L, 0L, 0L, 0L)] 

            # And so it goes...
            # If you wish to start a new tournament: 
            
            >>> startNewTournament()

            # And start over...
            `

     - There is a really simple test suit i used mainly to test the odd number
       of players. It starts a tournament and reports all matches until we have
       a winner. To run it, simply execute the following from a terminal 
       emulator:

            `
            $ python test_extras.py
            `

 > Author
--------------------------------------------------------------------------------
 - Tito Lins
   * Contact: <titolins@outlook.com> or <tito@blinx.com.br>
   * Github: https://github.com/titolins

################################################################################
################################################################################
