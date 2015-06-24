-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (id serial primary key, name text);

create table matches (id_1 integer, id_2 integer, winner integer);

-- standings view returns the current standings of the players
-- the standings include player id, name, wins and matches
create view standings as 
    select players.id, players.name, sum(case when matches.winner = players.id 
    then 1 else 0 end) as wins, sum(case when matches.id_1 = players.id or 
    matches.id_2 = players.id then 1 else 0 end) as matches from players left 
    join matches on players.id = matches.id_1 or players.id = matches.id_2 group 
    by players.id order by wins desc;

-- pairings view returns the regular pairings (as ordered by the standings view),
-- indicating the id and name of the players that are to play against each other
-- (id1, name1, id2, name2), but does not consider other factors (such as rematches) 
-- does not work with odd number of players.

create view pairings as
    select a.first_id, a.first_name, a.second_id, a.second_name from (select 
    s.id as first_id, s.name as first_name, lead(s.id) over(order by s.wins 
    desc) as second_id, lead(s.name) over(order by s.wins desc) as second_name 
    from standings as s) as a join (select s.id as first_id, lead(s.id) 
    over(order by s.wins desc) as second_id from standings as s) as b on 
    a.first_id != b.second_id and a.second_id != b.first_id and b.first_id != 
    a.first_id;

