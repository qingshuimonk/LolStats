from lolcrawler_util import read_key, get_challenger_league, get_matchlist_by_summoner
from lolstats_util import get_usrid_from_league, unix_time_millis
import datetime
import time
import os
import pickle
from tqdm import tqdm

api_key = read_key()
league = get_challenger_league(api_key)
usr_id = get_usrid_from_league(league)

start_dt = datetime.datetime(2016, 10, 4, 12, 0, 0)
end_dt = datetime.datetime(2016, 10, 11, 12, 0, 0)
start_time = int(unix_time_millis(start_dt))
end_time = int(unix_time_millis(end_dt))

match_ids = set()
matches = []

# get match ids
pbar = tqdm(total=len(usr_id))
for uid in usr_id:
    match_list = get_matchlist_by_summoner(uid, api_key, seasons='SEASON2016')
    try:
        for match in match_list['matches']:
            match_ids.update([match['matchId']])
            matches.append(match)
        # make sure not exceed rate limit
        time.sleep(5)
    except Exception:
        pass
    pbar.update(1)

path = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(path):
    os.makedirs(path)
f = open(os.path.join(path, 'league_match_history_2016_na.pickle'), 'wb')
pickle.dump(match_ids, f)
pickle.dump(matches, f)
f.close()
