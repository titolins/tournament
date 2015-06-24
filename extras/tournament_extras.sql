-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE tournaments (id serial primary key);

CREATE TABLE players (id serial primary key, name text, tournament_id integer
    references tournaments(id));

create table matches (id_1 integer, id_2 integer, winner integer);

-- standings view returns the current standings of the players
-- the standings include player id, player name, wins, draws, byes, matches, 
-- and omw

CREATE VIEW standings AS
    SELECT id, name, matches, wins, draws, byes, (wins-byes) AS omw FROM 
    (SELECT players.id, players.name, COUNT(matches.id_1) AS matches, SUM(CASE 
    WHEN matches.winner = players.id THEN 1 ELSE 0 END) AS wins, SUM(CASE WHEN 
    matches.winner = 0 THEN 1 ELSE 0 END) AS draws, SUM(CASE WHEN players.id = 
    matches.id_1 AND matches.id_2 < 0 THEN 1 ELSE 0 END) AS byes, 
    players.tournament_id FROM players LEFT JOIN matches ON players.id = 
    matches.id_1 OR players.id = matches.id_2 GROUP BY players.id) AS standings 
    WHERE standings.tournament_id = (SELECT MAX(tournaments.id) FROM 
    tournaments) ORDER BY wins DESC, omw DESC, draws DESC;
