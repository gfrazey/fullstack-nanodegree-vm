#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    conn.commit()
    c.execute("UPDATE standings SET s_matches = 0, s_wins = 0, s_losses = 0 ")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM standings")
    conn.commit()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(player_id) FROM players")
    player_count = c.fetchone()[0]
    conn.close()
    return player_count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn =connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (player_name) VALUES(%s)", (name,))
    conn.commit()
    c.execute("INSERT INTO standings (s_player_name) VALUES(%s)", (name,))
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
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT s_player_id, s_player_name, s_wins, s_matches FROM standings ORDER BY s_wins DESC")
    standings = [(str(row[0]), str(row[1]), row[2], row[3]) for row in c.fetchall()]
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    
    c.execute("INSERT INTO matches (match_winner,match_loser) VALUES (%s,%s)" , (winner,loser,))
    c.execute("UPDATE standings SET s_matches = s_matches + 1, s_wins = s_wins + 1 WHERE s_player_id = " + str(winner) + "")
    c.execute("UPDATE standings SET s_matches = s_matches + 1, s_losses = s_losses + 1 WHERE s_player_id = " + str(loser) + "")
    
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    
    c.execute("SELECT count(*) as num FROM standings")
    records = [{'num': int(row[0])} for row in c.fetchall()]
    length = records[0]['num']
    pairs = []

    for i in range(0,length/2):
        c.execute("SELECT * FROM (SELECT a.s_player_id, a.s_player_name, b.s_player_id, b.s_player_name FROM standings a, standings b WHERE (a.s_player_id != b.s_player_id AND a.s_wins >= b.s_wins) ORDER BY a.s_wins, b.s_wins DESC LIMIT 1 OFFSET " + str(i*2)+ ") AS pairing")
        
        pair = [(str(row[0]), str(row[1]), str(row[2]), str(row[3])) for row in c.fetchall()]
        
        pairs = pairs + pair

    
    conn.close()
    return pairs    

