-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;

\c tournament

CREATE TABLE players(
	player_id SERIAL UNIQUE PRIMARY KEY,
	player_name TEXT UNIQUE
);

CREATE TABLE matches(
	match_id SERIAL UNIQUE PRIMARY KEY,
	match_winner INTEGER REFERENCES players(player_id),
	match_loser INTEGER REFERENCES players(player_id)
);

CREATE TABLE standings(
	standing_id SERIAL UNIQUE PRIMARY KEY,
	s_player_id SERIAL REFERENCES players(player_id),
	s_player_name TEXT REFERENCES players(player_name),
	s_matches INTEGER DEFAULT 0,
	s_wins INTEGER DEFAULT 0,
	s_losses INTEGER DEFAULT 0
);
