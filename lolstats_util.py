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
