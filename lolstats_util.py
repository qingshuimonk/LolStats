from lolcrawler_util import *
import pickle
import datetime


def get_usrid_from_league(league):
    """
    get user id from a league and put them into a list
    :param league: LeagueDto: an object contains league information
    :return: usrid
    """
    entries = league['entries']
    usrid = []
    for entry in entries:
        usrid.append(entry['playerOrTeamId'])
    usrid = list(set(usrid))
    return usrid


def get_matchid_from_matchlist(matchlist, role={'SOLO', 'NONE', 'DUO', 'DUO_CARRY', 'DUO_SUPPORT'},
                               lane={'TOP', 'JUNGLE', 'MID', 'BOTTOM'}):
    matchid = []
    for match in matchlist['matches']:
        if match['role'] in role and match['lane'] in lane:
            matchid.append(match['matchId'])
    return list(set(matchid))


class PlayerMatchHistory:
    def __init__(self, summoner_name, region='na'):
        # match stats
        self.match_list = []
        self.kill = []
        self.death = []
        self.assist = []
        self.gold = []
        self.minions = []
        self.neutralM = []
        self.neutralM_enemy = []
        self.neutralM_team = []
        self.damage = []
        self.damage_m = []
        self.damage_p = []
        self.damage_taken = []
        self.vision_ward = []
        self.ward_place = []

        self.summoner_name = summoner_name
        self.summoner_id = get_summoner_info(name=summoner_name, region=region)[summoner_name.lower()]['id']
        self.region = region
        self.rank_type = ''
        self.season = ''

    def get_match_stats(self, ranked_queue, season, role, lane, save=True):
        self.rank_type = ranked_queue
        self.season = season
        all_match = get_matchlist_by_summoner(self.summoner_id, rankedQueues=ranked_queue, seasons=season,
                                              region=self.region)
        match_list = get_matchid_from_matchlist(all_match, role=role, lane=lane)
        self.match_list = match_list
        from tqdm import tqdm
        pbar = tqdm(total=len(self.match_list))
        for match_id in self.match_list:
            matchinfo = get_matchinfo_by_matchid(match_id, region=self.region)
            # find corresponding participant id
            for pid, participant in enumerate(matchinfo['participantIdentities']):
                if participant['player']['summonerId'] == self.summoner_id:
                    participant_id = pid
            # find corresponding stats
            stats = matchinfo['participants'][participant_id]['stats']
            self.kill.append(stats['kills'])
            self.death.append(stats['deaths'])
            self.assist.append(stats['assists'])
            self.gold.append(stats['goldEarned'])
            self.minions.append(stats['minionsKilled'])
            self.neutralM.append(stats['neutralMinionsKilled'])
            self.neutralM_enemy.append(stats['neutralMinionsKilledEnemyJungle'])
            self.neutralM_team.append(stats['neutralMinionsKilledTeamJungle'])
            self.damage_m.append(stats['magicDamageDealtToChampions'])
            self.damage_p.append(stats['physicalDamageDealtToChampions'])
            self.damage.append(stats['totalDamageDealtToChampions'])
            self.damage_taken.append(stats['totalDamageTaken'])
            self.vision_ward.append(stats['visionWardsBoughtInGame'])
            self.ward_place.append(stats['wardsPlaced'])
            pbar.update(1)
            from time import sleep
            sleep(1.5)
        pbar.close()

        if save:
            path = os.path.join(os.path.dirname(__file__), 'data')
            if not os.path.exists(path):
                os.makedirs(path)
            f = open(os.path.join(path, '%s_%s_%s.pickle' % (self.summoner_name, self.rank_type, self.season)), 'wb')
            pickle.dump(self, f)
            f.close()


def unix_time_millis(dt):
    """
    convert human read time to epoch time in milliseconds
    :param dt:  datetime
    :return:    epoch time in milliseconds
    """
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0
