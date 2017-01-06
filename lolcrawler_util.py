import os
import urllib2
import json


def read_key():
    """
    Read API key from /data/credential.txt
    :return:            API key
    """
    path = os.path.join(os.path.dirname(__file__), 'data')
    f = open(os.path.join(path, 'credential.txt'), 'r')
    key = f.read()
    f.close()
    return key


def get_challenger_league(api_key=read_key(), match_type='RANKED_SOLO_5x5'):
    """
    :param api_key:
    :param match_type:  Game queue type, can be RANKED_FLEX_SR, RANKED_FLEX_TT, RANKED_FLEX_SR,
                        RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5
    :return:            The object of league information
    """
    response = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=' +
                               match_type+'&api_key=' + api_key)
    league = json.load(response)
    return league


def get_summoner_info(api_key=read_key(), name='IEEERoy', region='na'):
    """
    :param api_key:
    :param name:        Name of the summoner, using my name as default here
    :param region:      Region to execute search
    :return:            Summoner Object
    """
    response = urllib2.urlopen('https://'+region+'.api.pvp.net/api/lol/'+region+'/v1.4/summoner/by-name/'
                               +name+'?api_key=' + api_key)
    summoner = json.load(response)
    return summoner


def get_matchlist_by_summoner(summoner_id, api_key=read_key(), region='na', **kwargs):
    """
    :param summoner_id: ID of a summoner
    :param api_key:
    :param region:
    :param kwargs:      Can be championIds, rankedQueues, seasons, beginTime, endTime, beginIndex, endIndex
    :return:
    """
    request_rul = 'https://'+region+'.api.pvp.net/api/lol/'+region+'/v2.2/matchlist/by-summoner/'+str(summoner_id)+'?'
    for key, value in kwargs.iteritems():
        request_rul += '%s=%s&' % (key, value)
    request_rul += 'api_key='+api_key

    response = urllib2.urlopen(request_rul)
    matchlist = json.load(response)
    return matchlist


def get_matchinfo_by_matchid(matchid, api_key=read_key(), region='na'):
    """
    :param matchid:     ID of a match
    :param api_key:
    :param region:
    :return:
    """
    response = urllib2.urlopen('https://'+region+'.api.pvp.net/api/lol/'+region+'/v2.2/match/'+str(matchid)+
                               '?api_key=' + api_key)
    matchinfo = json.load(response)
    return matchinfo
