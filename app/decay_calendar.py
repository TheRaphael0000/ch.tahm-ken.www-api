from .riot_api_routes import account_by_riot_id, league_entries, matches_ids, summoner, match
from dataclasses import dataclass
from datetime import datetime, timedelta
from ics import Calendar, Event
import io


@dataclass
class DecayRules:
    BANKED_DAYS_PER_MATCH: int
    MAXIMUM_BANKED_DAYS: int
    INITIAL_DAYS_BEFORE_DECAY:int
    LP_LOST_ON_DECAY: int

APEX_RULE = DecayRules(1, 14, 14, 75)
DECAY_RULES = {
    "DIAMOND": DecayRules(7, 28, 28, 50),
    "MASTER": APEX_RULE,
    "GRANDMASTER": APEX_RULE,
    "CHALLENGER": APEX_RULE,
}

QUEUE_TYPE_MAP = {
    "RANKED_SOLO_5x5": 420,
    "RANKED_FLEX_SR": 440,
}

def decay_calendar(region:str, gameNameTag: str):
    calendar = Calendar()

    try:
        gameName, tagLine = gameNameTag.split("-")
        account = account_by_riot_id(gameName, tagLine)
        puuid = account["puuid"]
        league_entries_ = league_entries(puuid, region)

        for league_entry in league_entries_:
            tier = league_entry.get("tier")
            queueType = league_entry.get("queueType")
            if queueType not in QUEUE_TYPE_MAP:
                continue
            if tier not in DECAY_RULES:
                continue
            rule = DECAY_RULES.get(tier)

            decay_date = compute_queue_decay(league_entry)

            e = Event()
            e.name = f"Decay {account.get("gameName")}#{account.get("tagLine")} ({queueType})"
            e.description = f"Current: {league_entry.get("tier")} {league_entry.get("rank")} {league_entry.get("leaguePoints")}LP\n Decay: {rule.LP_LOST_ON_DECAY}LP"
            e.begin = decay_date
            calendar.events.add(e)

        return calendar.serialize()

    except Exception as e:
        print(e)
        pass

def compute_queue_decay(league_entry):
    queue_id = QUEUE_TYPE_MAP.get(league_entry.get("queueType"))
    puuid = league_entry.get("puuid")
    rules = DECAY_RULES.get(league_entry["tier"])
    matches_ids_ = matches_ids(puuid, queue=queue_id)

    banked_days = timedelta()
    now = datetime.now()
    max_time = now -  timedelta(days=rules.INITIAL_DAYS_BEFORE_DECAY)

    for m in matches_ids_:
        match_ = match(m)
        gameEndTimestamp = datetime.fromtimestamp(match_.get("info").get("gameEndTimestamp") / 1000.0)

        if gameEndTimestamp < max_time:
            break

        banked_days += timedelta(days=rules.BANKED_DAYS_PER_MATCH)

    last_match = match(matches_ids_[0])
    last_match_gameEndTimestamp = datetime.fromtimestamp(last_match.get("info").get("gameEndTimestamp") / 1000.0)

    decay_date = last_match_gameEndTimestamp + banked_days

    return decay_date