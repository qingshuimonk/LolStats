from lolstats_util import PlayerMatchHistory

history = PlayerMatchHistory('PraY8D', 'kr')
history.get_match_stats('TEAM_BUILDER_DRAFT_RANKED_5x5', 'SEASON2016', {'DUO', 'DUO_CARRY'}, {'BOTTOM'}, save=True)
