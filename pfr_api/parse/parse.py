from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup

from pfr_api.parse.parser import RowParser, IdentityParser, \
    StrToIntParser, NullableStrToIntParser, \
    NullableStrToFloatParser, StrPercentageToFloatParser, \
    NullableStrPercentageToFloatParser


PARSERS = {
    'year_id': StrToIntParser('year_id'),
    'gs': IdentityParser('gs'),   # TODO make this a boolean

    # Passing
    'pass_cmp': NullableStrToIntParser('pass_cmp'),
    'pass_att': NullableStrToIntParser('pass_att'),
    'pass_cmp_perc': NullableStrPercentageToFloatParser('pass_cmp_perc'),
    'pass_yds': NullableStrToIntParser('pass_yds'),
    'pass_td': NullableStrToIntParser('pass_td'),
    'pass_int': NullableStrToIntParser('pass_int'),
    'pass_rating': NullableStrToFloatParser('pass_rating'),
    'pass_sacked': NullableStrToIntParser('pass_sacked'),
    'pass_sacked_yds': NullableStrToIntParser('pass_sacked_yds'),
    'pass_yds_per_att': NullableStrToFloatParser('pass_yds_per_att'),
    'pass_adj_yds_per_att': NullableStrToFloatParser('pass_adj_yds_per_att'),
    'qb_rec': IdentityParser('qb_rec'),
    'pass_td_perc': NullableStrPercentageToFloatParser('pass_td_perc'),
    'pass_int_perc': NullableStrToFloatParser('pass_int_perc'),
    'pass_first_down': NullableStrToIntParser('pass_first_down'),
    'pass_yds_per_cmp': NullableStrToFloatParser('pass_yds_per_cmp'),
    'pass_yds_per_g': NullableStrToFloatParser('pass_yds_per_g'),
    'qbr': NullableStrToFloatParser('qbr'),
    'pass_net_yds_per_att': NullableStrToFloatParser('pass_net_yds_per_att'),
    'pass_adj_net_yds_per_att': NullableStrToFloatParser('pass_adj_net_yds_per_att'),
    'pass_sacked_perc': StrPercentageToFloatParser('pass_sacked_perc'),
    'comebacks': NullableStrToIntParser('comebacks'),
    'gwd': NullableStrToIntParser('gwd'),
    'av': NullableStrToIntParser('av'),

    # Advanced passing
    'pass_air_yards': NullableStrToIntParser('pass_air_yards'),
    'pass_air_yards_per_cmp': NullableStrToFloatParser('pass_air_yards_per_cmp'),
    'pass_air_yards_per_att': NullableStrToFloatParser('pass_air_yards_per_att'),
    'pass_tgt_yards_per_att': NullableStrToFloatParser('pass_tgt_yards_per_att'),
    'pass_yac': NullableStrToFloatParser('pass_yac'),
    'pass_yac_per_cmp': NullableStrToFloatParser('pass_yac_per_cmp'),
    'pass_drops': NullableStrToFloatParser('pass_drops'),
    'pass_drops_pct': NullableStrPercentageToFloatParser('pass_drops_pct'),
    'pass_poor_throws': NullableStrToFloatParser('pass_poor_throws'),
    'pass_poor_throws_pct': NullableStrPercentageToFloatParser('pass_poor_throws_pct'),
    'pass_blitzed': NullableStrToFloatParser('pass_blitzed'),
    'pass_hurried': NullableStrToFloatParser('pass_hurried'),
    'pass_hits': NullableStrToFloatParser('pass_hits'),
    'rush_scrambles': NullableStrToFloatParser('rush_scrambles'),
    'rush_scrambles_yds_per_att': NullableStrToFloatParser('rush_scrambles_yds_per_att'),

    # Rushing/receiving
    'rush_att': NullableStrToIntParser('rush_att'),
    'rush_yds': NullableStrToIntParser('rush_yds'),
    'rush_yds_per_att': NullableStrToFloatParser('rush_yds_per_att'),
    'rush_td': NullableStrToIntParser('rush_td'),
    'rush_td_perc': NullableStrPercentageToFloatParser('rush_td_perc'),
    'rush_first_down': NullableStrToIntParser('rush_first_down'),
    'rush_long': NullableStrToIntParser('rush_first_down'),
    'rush_yds_per_g': NullableStrToFloatParser('rush_yds_per_g'),
    'rush_att_per_g': NullableStrToFloatParser('rush_att_per_g'),
    'targets': NullableStrToIntParser('targets'),
    'rec': NullableStrToIntParser('rec'),
    'rec_yds': NullableStrToIntParser('rec_yds'),
    'rec_yds_per_rec': NullableStrToFloatParser('rec_yds_per_rec'),
    'rec_td': NullableStrToIntParser('rec_td'),
    'catch_pct': StrPercentageToFloatParser('catch_pct'),
    'rec_yds_per_tgt': NullableStrToFloatParser('rec_yds_per_tgt'),
    'rec_first_down': NullableStrToIntParser('rec_first_down'),
    'rec_long': NullableStrToIntParser('rec_first_down'),
    'rec_yds_per_g': NullableStrToFloatParser('rec_yds_per_g'),
    'rec_att_per_g': NullableStrToFloatParser('rec_att_per_g'),
    'touches': NullableStrToIntParser('touches'),
    'yds_per_touch': NullableStrToIntParser('yds_per_touch'),
    'yds_from_scrimmage': NullableStrToIntParser('yds_from_scrimmage'),
    'rush_receive_td': NullableStrToIntParser('rush_receive_td'),

    # Advanced rushing/receiving
    'rush_yds_before_contact': NullableStrToIntParser('rush_yds_before_contact'),
    'rush_yds_bc_per_rush': NullableStrToFloatParser('rush_yds_bc_per_rush'),
    'rush_yac': NullableStrToIntParser('rush_yac'),
    'rush_yac_per_rush': NullableStrToFloatParser('rush_yac_per_rush'),
    'rush_broken_tackles': NullableStrToIntParser('rush_broken_tackles'),
    'rush_broken_tackles_per_rush': NullableStrToFloatParser('rush_broken_tackles_per_rush'),
    'rec_air_yds': NullableStrToIntParser('rec_air_yds'),
    'rec_air_yds_per_rec': NullableStrToFloatParser('rec_air_yds_per_rec'),
    'rec_yac': NullableStrToIntParser('rec_yac'),
    'rec_yac_per_rac': NullableStrToFloatParser('rec_yac_per_rac'),
    'rec_broken_tackles': NullableStrToIntParser('rec_broken_tackles'),
    'rec_broken_tackles_per_rec': NullableStrToFloatParser('rec_broken_tackles_per_rec'),
    'dropped_passes': NullableStrToIntParser('dropped_passes'),
    'rec_drop_pct': NullableStrPercentageToFloatParser('rec_drop_pct'),

    # Field-position aware
    # Rushing/receiving
    'rush_att_in_10': NullableStrToIntParser('rush_att_in_10'),
    'rush_yds_in_10': NullableStrToIntParser('rush_yds_in_10'),
    'rush_td_in_10': NullableStrToIntParser('rush_td_in_10'),
    'targets_in_10': NullableStrToIntParser('targets_in_10'),
    'rec_in_10': NullableStrToIntParser('rec_in_10'),
    'rec_yds_in_10': NullableStrToIntParser('rec_yds_in_10'),
    'rec_yds_per_rec_in_10': NullableStrToFloatParser('rec_yds_per_rec_in_10'),
    'rec_td_in_10': NullableStrToIntParser('rec_td_in_10'),
    # Passing
    'pass_cmp_in_10': NullableStrToIntParser('pass_cmp_in_10'),
    'pass_att_in_10': NullableStrToIntParser('pass_att_in_10'),
    'pass_yds_in_10': NullableStrToIntParser('pass_yds_in_10'),
    'pass_td_in_10': NullableStrToIntParser('pass_td_in_10'),

    # Misc. offense
    'two_pt_md': NullableStrToIntParser('two_pt_md'),
    'all_td': NullableStrToIntParser('all_td'),
    'scoring': NullableStrToIntParser('scoring'),
    'fumbles': NullableStrToIntParser('fumbles'),
    'fumbles_lost': NullableStrToIntParser('fumbles_lost'),
    'offense': NullableStrToIntParser('offense'),
    'off_pct': NullableStrPercentageToFloatParser('off_pct'),

    # Misc
    'uniform_number': StrToIntParser('uniform_number'),

    # Special teams
    'kick_ret': NullableStrToIntParser('kick_ret'),
    'kick_ret_yds': NullableStrToIntParser('kick_ret_yds'),
    'kick_ret_yds_per_ret': NullableStrToFloatParser('kick_ret_yds_per_ret'),
    'kick_ret_td': NullableStrToIntParser('kick_ret_td'),
    'punt_ret': NullableStrToIntParser('punt_ret'),
    'punt_ret_yds': NullableStrToIntParser('punt_ret_yds'),
    'punt_ret_yds_per_ret': NullableStrToFloatParser('punt_ret_yds_per_ret'),
    'punt_ret_td': NullableStrToIntParser('punt_ret_td'),
    'special_teams': NullableStrToIntParser('special_teams'),
    'st_pct': NullableStrPercentageToFloatParser('st_pct'),

    # defensive
    'sacks': NullableStrToFloatParser('sacks'),
    'tackles_solo': NullableStrToIntParser('tackles_solo'),
    'tackles_assists': NullableStrToIntParser('tackles_assists'),
    'tackles_combined': NullableStrToIntParser('tackles_combined'),
    'tackles_loss': NullableStrToIntParser('tackles_loss'),
    'qb_hits': NullableStrToIntParser('qb_hits'),
    'fumbles_forced': NullableStrToIntParser('fumbles_forced'),
    'fumbles_rec': NullableStrToIntParser('fumbles_rec'),
    'fumbles_rec_yds': NullableStrToIntParser('fumbles_rec_yds'),
    'fumbles_rec_td': NullableStrToIntParser('fumbles_rec_td'),
    'def_int': NullableStrToIntParser('def_int'),
    'def_int_yds': NullableStrToIntParser('def_int_yds'),
    'def_int_td': NullableStrToIntParser('def_int_td'),
    'pass_defended': NullableStrToIntParser('pass_defended'),
    'defense': NullableStrToIntParser('defense'),
    'def_pct': NullableStrPercentageToFloatParser('def_pct'),

    # Fantasy-specific
    'player': IdentityParser('player'),
    'fantasy_pos': IdentityParser('fantasy_pos'),
    'starter_pos': IdentityParser('starter_pos'),
    'g': NullableStrToIntParser('g'),
    # 'gs': _str_to_int_parser('gs'),  TODO how to handle ambiguity
    'two_pt_pass': NullableStrToFloatParser('two_pt_pass'),
    'fantasy_points': NullableStrToFloatParser('fantasy_points'),
    'fantasy_points_ppr': NullableStrToFloatParser('fantasy_points_ppr'),
    'draftkings_points': NullableStrToFloatParser('draftkings_points'),
    'fanduel_points': NullableStrToFloatParser('fanduel_points'),
    'vbd': NullableStrToIntParser('vbd'),
    'fantasy_rank_pos': NullableStrToIntParser('fantasy_rank_pos'),
    'fantasy_rank_overall': NullableStrToIntParser('fantasy_rank_overall'),
    # Fantasy metadata
    # Literally just contains a link to a fantasy game log page
    'games': IdentityParser('games'),

    # Team stats
    # Offense
    'points': StrToIntParser('points'),
    'total_yards': StrToIntParser('total_yards'),
    'plays_offense': StrToIntParser('plays_offense'),
    'yds_per_play_offense': NullableStrToFloatParser('yds_per_play_offense'),
    'turnovers': StrToIntParser('turnovers'),
    'first_down': StrToIntParser('first_down'),
    'pass_fd': StrToIntParser('pass_fd'),
    'rush_fd': StrToIntParser('rush_fd'),
    'penalties': StrToIntParser('penalties'),
    'penalties_yds': StrToIntParser('penalties_yds'),
    'pen_fd': StrToIntParser('pen_fd'),
    'drives': StrToIntParser('drives'),
    'score_pct': NullableStrPercentageToFloatParser('score_pct'),
    'turnover_pct': NullableStrPercentageToFloatParser('turnover_pct'),
    'start_avg': IdentityParser('start_avg'),
    'time_avg': IdentityParser('time_avg'),
    'plays_per_drive': NullableStrToFloatParser('plays_per_drive'),
    'yds_per_drive': NullableStrToFloatParser('yds_per_drive'),
    'points_avg': NullableStrToFloatParser('points_avg'),

    # Game info
    'game_date': IdentityParser('game_date'),  # TODO datetime
    'game_num': StrToIntParser('game_num'),
    'week_num': StrToIntParser('week_num'),
    'age': IdentityParser('age'),
    'team': IdentityParser('team'),
    'game_location': IdentityParser('game_location'),
    'game_result': IdentityParser('game_result'),
    'week': StrToIntParser('week'),
    'day': IdentityParser('day'),
    'date': IdentityParser('date'),  # TODO datetime
    'game_time': IdentityParser('game_time'),  # TODO datetime,
    'boxscore_word': IdentityParser('boxscore_word'),
    'game_outcome': IdentityParser('game_outcome'),
    'overtime': IdentityParser('overtime'),
    'team_record': IdentityParser('team_record'),
    'opp': IdentityParser('opp'),

    # Team game stats
    'pts_off': StrToIntParser('pts_off'),
    'pts_def': StrToIntParser('pts_def'),
    'first_down_off': StrToIntParser('first_down_off'),
    'yards_off': StrToIntParser('yards_off'),
    'pass_yds_off_off': StrToIntParser('pass_yds_off_off'),
    'rush_yds_off_off': StrToIntParser('rush_yds_off_off'),
    'to_off': StrToIntParser('to_off'),
    'first_down_def': StrToIntParser('first_down_def'),
    'yards_def': StrToIntParser('yards_def'),
    'pass_yds_def_def': StrToIntParser('pass_yds_def_def'),
    'rush_yds_def_def': StrToIntParser('rush_yds_def_def'),
    'to_def': StrToIntParser('to_def'),
    'exp_pts_off': NullableStrToFloatParser('exp_pts_off'),
    'exp_pts_def': NullableStrToFloatParser('exp_pts_def'),
    'exp_pts_st': NullableStrToFloatParser('exp_pts_st'),

}  # type: Dict[str, RowParser]


def parse_stats_table(
    table: BeautifulSoup,
    stat_row_attributes: Optional[Dict[str, Any]] = None,
    parsers: Optional[Dict[str, RowParser]] = None,
) -> Tuple[List[str], List[List[Any]]]:
    if stat_row_attributes is None:
        stat_row_attributes = {}

    if parsers is None:
        parsers = {}  # type: Dict[str, RowParser]

    parsers = {**PARSERS, **parsers}

    column_infos = []
    html_columns = table.find('thead').find_all('tr')[-1]
    for column in html_columns.find_all('th'):
        stat = column['data-stat']
        name = column.text
        column_infos.append((stat, name))
    column_infos = column_infos[1:]  # Skip the ranker column

    output_columns = []
    for column_stat, column_name in column_infos:
        parser = parsers[column_stat]
        output_columns.extend(parser.output_fields)

    rows = []
    html_body = table.find('tbody')
    html_rows = html_body.find_all(
        'tr', recursive=False, **stat_row_attributes)
    for html_row in html_rows:
        row = [None] * len(output_columns)
        field_count = 0
        for i, ((column_stat, column_name), html_row_col) in enumerate(
            zip(column_infos, html_row.find_all('td', recursive=False))
        ):
            parser = parsers[column_stat]
            parsed = parser.parse(html_row_col)
            num_fields = len(parsed)
            # Assumption: .values() will return the fields in the order returned
            # by .output_fields
            row[field_count:field_count+num_fields] = parsed.values()
            field_count += num_fields
        rows.append(row)

    return output_columns, rows
