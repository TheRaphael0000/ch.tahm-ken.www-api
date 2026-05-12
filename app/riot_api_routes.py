from .riot_api import query
from urllib.parse import urlencode

def account_by_riot_id(gameName, tagLine):
    return query(f"/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}")

def champion_masteries(puuid, region):
    return query(f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}", region, expire=600)

def challenges_player_data(puuid, region):
    return query(f"/lol/challenges/v1/player-data/{puuid}", region, expire=10)

def summoner(puuid, region):
    return query(f"/lol/summoner/v4/summoners/by-puuid/{puuid}", region, expire=86400)

def league_entries(puuid, region):
    return query(f"/lol/league/v4/entries/by-puuid/{puuid}", region, expire=86400)

def matches_ids(puuid, **args):
    arguments = urlencode(args, doseq=True)
    return query(f"/lol/match/v5/matches/by-puuid/{puuid}/ids?{arguments}", expire=600)

def match(matchId):
    return query(f"/lol/match/v5/matches/{matchId}", expire=60*60*24*7)