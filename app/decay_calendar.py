from .riot_api_routes import account_by_riot_id, league_entries, matches_ids, summoner, match
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone, time
from ics import Calendar, Event


@dataclass
class DecayRules:
    BANKED_DAYS_PER_MATCH: int
    MAXIMUM_BANKED_DAYS: int
    INITIAL_DAYS_BEFORE_DECAY: int
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

QUEUE_TYPE_LABEL = {
    "RANKED_SOLO_5x5": "SOLO",
    "RANKED_FLEX_SR": "FLEX",
}


def decay_calendar(region: str, gameNameTag: str):
    calendar = Calendar()
    calendar.creator = "Tahm-ken.ch - Decay Calendar"

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
            e.name = f"{account.get("gameName")}#{account.get("tagLine")} {QUEUE_TYPE_LABEL.get(queueType)} Decay"
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

    banked_days = 0

    last_match = match(matches_ids_[0])
    last_match_gameEndTimestamp = datetime.fromtimestamp(
        last_match.get("info").get("gameEndTimestamp") / 1000.0, tz=timezone.utc)
    max_time = last_match_gameEndTimestamp - \
        timedelta(days=rules.MAXIMUM_BANKED_DAYS)

    for m in matches_ids_:
        match_ = match(m)
        is_remake = any([p["gameEndedInEarlySurrender"]
                        for p in match_.get("info").get("participants")])
        if is_remake:
            continue

        gameEndTimestamp = datetime.fromtimestamp(match_.get(
            "info").get("gameEndTimestamp") / 1000.0, tz=timezone.utc)

        print(gameEndTimestamp, max_time, banked_days)
        if gameEndTimestamp < max_time:
            # game too old, can't be providing bank days
            break

        banked_days += rules.BANKED_DAYS_PER_MATCH

        if banked_days >= rules.MAXIMUM_BANKED_DAYS:
            # maximal banked days reached
            break

    # to be sure
    banked_days = min(banked_days, rules.MAXIMUM_BANKED_DAYS)

    decay_date = datetime.combine(last_match_gameEndTimestamp.date(
    ) + timedelta(days=banked_days), time(hour=22, minute=45, second=0), tzinfo=timezone.utc)

    return decay_date
