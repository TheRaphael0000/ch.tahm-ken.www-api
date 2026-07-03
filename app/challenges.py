from .riot_api_routes import account_by_riot_id, challenges_player_data, champion_masteries, summoner, league_entries


def challenges_players_data(region: str, gameNamesTags: str):
    accounts = []
    gameNamesParsed = [tuple(gameNameTag.split("-"))
                       for gameNameTag in set(gameNamesTags.split(","))]

    if len(gameNamesParsed) > 7:
        return accounts

    for gameNameTag in gameNamesParsed:
        if len(gameNameTag) != 2:
            continue

        gameName, tagLine = gameNameTag
        try:
            data = {}
            data["region"] = region
            data["account"] = account_by_riot_id(gameName, tagLine)
            puuid = data["account"]["puuid"]
            data["challenges"] = challenges_player_data(puuid, region)
            data["summoner"] = summoner(puuid, region)
            data["champion_masteries"] = champion_masteries(puuid, region)
            data["league_entries"] = league_entries(puuid, region)
            accounts.append(data)
        except Exception as e:
            print(e)
            pass
    return accounts
