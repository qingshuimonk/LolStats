import os


def read_key():
    """
    Read API key from /data/credential.txt
    :return: API key
    """
    path = os.path.join(os.path.dirname(__file__), 'data')
    f = open(os.path.join(path, 'credential.txt'), 'r')
    key = f.read()
    f.close()
    return key


def get_challenger_league(api_key=read_key(), match_type='RANKED_SOLO_5x5'):
    """
    :param api_key:
    :param match_type:  game queue type, can be RANKED_FLEX_SR, RANKED_FLEX_TT, RANKED_FLEX_SR,
                        RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5
    :return: The object of league information
    """
    import urllib2
    import json
    response = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=' +
                               match_type+'&api_key=' + api_key)
    league = json.load(response)
    return league
