################################################################################
################################################################################
#                                                                              #
#                  Udacity FullStack WebDeveloper Nanodegree                   #
#                                                                              #
#                                                                              #
#                            Tournament Project                                #
#                                                                              #
################################################################################
################################################################################
##                                                                            ##
## This is the readme for the Tournament Project, second project required for ##
## obtaining the full stack web developer nano degree from udacity:           ##
##                                                                            ##
##   http://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004 ##
##                                                                            ##
################################################################################


 > Description
--------------------------------------------------------------------------------

 - The aim of this project is to create an api to access and  manage data from a 
   tournament based on the swiss pairings system.

 - The tournament.sql file contains the sql statements for preparing the 
   database. 

 - The api code is contained in the tournament.py file, and allows you to
   register new players, count the players registered, delete all matches and
   players records, count players registered, view the player standings, report
   a match and request the swiss pairings for the round.

 - It is important to note that this implementation only supports one tournament
   and a even number of players. Also, it does not care if a match between two
   given players has already happened or not.


 > Requirements
-------------------------------------------------------------------------------

 - Python
    -> https://www.python.org/downloads/
 
 - psycopg -- python module for connecting with postgresql databases
    -> http://initd.org/psycopg/
    
 - PostgreSQL
    -> http://www.postgresql.org/


 > Instructions
-------------------------------------------------------------------------------

 - First of all, prepare your database:
    -> After installing and configuring postgresql, you will need to connect to
       it and import the schema from the .sql file, as follows:

            $ psql
            => create database tournament;
            => \c tournament
            => \i tournament.sql
            CREATE TABLE
            CREATE TABLE
            CREATE VIEW
            CREATE VIEW
    
    -> The standings view created above may be used to get the player standings.

    -> Also, the pairings view already selects the players that are to play each
       other in the next round in accordance with the order in the standings.
            
 - Now that your database is prepared, you may use any of the app 
   functionalities from a python interpreter. e.g. using the command line to
   start playing a new tournament:
            
            $ python
            >>> from tournament import *
            >>> registerPlayer("Markov Chaney") 
            >>> registerPlayer("Joe Malik") 
            >>> registerPlayer("Mao Tsu-hsi")
            >>> registerPlayer("Atlanta Hope")
            >>> countPlayers()
            4L
            >>> playerStandings()   # returns (id, name, wins, matches) 
                                    # for each player    

            [(4, 'Atlanta Hope', 0L, 0L), (3, 'Mao Tsu-hsi', 0L, 0L), 
            (2, 'Joe Malik', 0L, 0L), (1, 'Markov Chaney', 0L, 0L)]

            >>> swissPairings() # returns (id_1, name_1, id_2, name_2) for each
                                # match to occur this round

            [(4, 'Atlanta Hope', 3, 'Mao Tsu-hsi').
            (2, 'Joe Malik', 1, 'Markov Chaney)]

            >>> reportMatch(4, 3)
            >>> reportMatch(2, 1)
            >>> playerStandings()
            [(4, 'Atlanta Hope', 1L, 1L), (2, 'Joe Malik', 1L, 1L), 
            (3, 'Mao Tsu-hsi', 0L, 1L), (1, 'Markov Chaney', 0L, 1L)]

            # And so it goes...
            # If you wish to start a new tournament, simply delete all players
            # and matches records, as follows:

            >>> deletePlayers()
            >>> deleteMatches()

            # And start over...

 - To run the test suite, simply execute the following from a terminal emulator:

            $ python tournament_test.py


 > Author
-------------------------------------------------------------------------------
 - Tito Lins
   -> Contact: <titolins@outlook.com> or <tito@blinx.com.br>
   -> Github: https://github.com/titolins

################################################################################
################################################################################
