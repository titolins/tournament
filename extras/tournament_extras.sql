-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table tournaments (id serial primary key);

create table players (id serial primary key, name text, tournament_id integer,
    foreign key (tournament_id) references tournaments(id));

create table matches (id_1 integer, id_2 integer, winner integer);

-- standings view returns the current standings of the players
-- the standings include player id, player name, wins, draws, byes, matches, and
-- omw

create view standings as
    select id, name, matches, wins, draws, byes, (wins-byes) as omw from (select
    players.id, players.name, count(matches.id_1) as matches, sum(case when 
    matches.winner = players.id then 1 else 0 end) as wins, sum(case when 
    matches.winner = 0 then 1 else 0 end) as draws, sum(case when players.id = 
    matches.id_1 and matches.id_2 < 0 then 1 else 0 end) as byes, 
    players.tournament_id from players left join matches on players.id = 
    matches.id_1 or players.id = matches.id_2 group by players.id) as standings 
    where standings.tournament_id = (select max(tournaments.id) from 
    tournaments) order by wins desc, omw desc, draws desc;
