from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup

from pfr_api.parse.parser import FieldParser, _identity_parser, \
    _str_to_int_parser, _nullable_str_to_int_parser, \
    _nullable_str_to_float_parser, _str_percentage_to_float_parser, \
    _nullable_str_percentage_to_float_parser


PARSERS = {
    'year_id': _str_to_int_parser('year_id'),
    'game_date': _identity_parser('game_date'),
    'game_num': _str_to_int_parser('game_num'),
    'week_num': _str_to_int_parser('week_num'),
    'age': _identity_parser('age'),
    'team': _identity_parser('team'),
    'game_location': _identity_parser('game_location'),
    'opp': _identity_parser('opp'),
    'game_result': _identity_parser('game_result'),
    'gs': _identity_parser('gs'),   # TODO
    'pass_cmp': _nullable_str_to_int_parser('pass_cmp'),
    'pass_att': _nullable_str_to_int_parser('pass_att'),
    'pass_cmp_perc': _nullable_str_percentage_to_float_parser('pass_cmp_perc'),
    'pass_yds': _nullable_str_to_int_parser('pass_yds'),
    'pass_td': _nullable_str_to_int_parser('pass_td'),
    'pass_int': _nullable_str_to_int_parser('pass_int'),
    'pass_rating': _nullable_str_to_float_parser('pass_rating'),
    'pass_sacked': _nullable_str_to_int_parser('pass_sacked'),
    'pass_sacked_yds': _nullable_str_to_int_parser('pass_sacked_yds'),
    'pass_yds_per_att': _nullable_str_to_float_parser('pass_yds_per_att'),
    'pass_adj_yds_per_att': _nullable_str_to_float_parser('pass_adj_yds_per_att'),
    'rush_att': _nullable_str_to_int_parser('rush_att'),
    'rush_yds': _nullable_str_to_int_parser('rush_yds'),
    'rush_yds_per_att': _nullable_str_to_float_parser('rush_yds_per_att'),
    'rush_td': _nullable_str_to_int_parser('rush_td'),
    'targets': _nullable_str_to_int_parser('targets'),
    'rec': _nullable_str_to_int_parser('rec'),
    'rec_yds': _nullable_str_to_int_parser('rec_yds'),
    'rec_yds_per_rec': _nullable_str_to_float_parser('rec_yds_per_rec'),
    'rec_td': _nullable_str_to_int_parser('rec_td'),
    'catch_pct': _str_percentage_to_float_parser('catch_pct'),
    'rec_yds_per_tgt': _nullable_str_to_float_parser('rec_yds_per_tgt'),
    'two_pt_md': _nullable_str_to_int_parser('two_pt_md'),
    'all_td': _nullable_str_to_int_parser('all_td'),
    'scoring': _nullable_str_to_int_parser('scoring'),
    'fumbles': _nullable_str_to_int_parser('fumbles'),
    'fumbles_lost': _nullable_str_to_int_parser('fumbles_lost'),
    'offense': _nullable_str_to_int_parser('offense'),
    'off_pct': _nullable_str_percentage_to_float_parser('off_pct'),

    # Special teams
    'kick_ret': _nullable_str_to_int_parser('kick_ret'),
    'kick_ret_yds': _nullable_str_to_int_parser('kick_ret_yds'),
    'kick_ret_yds_per_ret': _nullable_str_to_float_parser('kick_ret_yds_per_ret'),
    'kick_ret_td': _nullable_str_to_int_parser('kick_ret_td'),
    'punt_ret': _nullable_str_to_int_parser('punt_ret'),
    'punt_ret_yds': _nullable_str_to_int_parser('punt_ret_yds'),
    'punt_ret_yds_per_ret': _nullable_str_to_float_parser('punt_ret_yds_per_ret'),
    'punt_ret_td': _nullable_str_to_int_parser('punt_ret_td'),
    'special_teams': _nullable_str_to_int_parser('special_teams'),
    'st_pct': _nullable_str_percentage_to_float_parser('st_pct'),

    # defensive
    'sacks': _nullable_str_to_float_parser('sacks'),
    'tackles_solo': _nullable_str_to_int_parser('tackles_solo'),
    'tackles_assists': _nullable_str_to_int_parser('tackles_assists'),
    'tackles_combined': _nullable_str_to_int_parser('tackles_combined'),
    'tackles_loss': _nullable_str_to_int_parser('tackles_loss'),
    'qb_hits': _nullable_str_to_int_parser('qb_hits'),
    'fumbles_forced': _nullable_str_to_int_parser('fumbles_forced'),
    'fumbles_rec': _nullable_str_to_int_parser('fumbles_rec'),
    'fumbles_rec_yds': _nullable_str_to_int_parser('fumbles_rec_yds'),
    'fumbles_rec_td': _nullable_str_to_int_parser('fumbles_rec_td'),
    'def_int': _nullable_str_to_int_parser('def_int'),
    'def_int_yds': _nullable_str_to_int_parser('def_int_yds'),
    'def_int_td': _nullable_str_to_int_parser('def_int_td'),
    'pass_defended': _nullable_str_to_int_parser('pass_defended'),
    'defense': _nullable_str_to_int_parser('defense'),
    'def_pct': _nullable_str_percentage_to_float_parser('def_pct'),

    # Fantasy-specific
    'player': _identity_parser('player'),
    'fantasy_pos': _identity_parser('fantasy_pos'),
    'g': _nullable_str_to_int_parser('g'),
    # 'gs': _str_to_int_parser('gs'),  TODO how to handle ambiguity
    'two_pt_pass': _nullable_str_to_float_parser('two_pt_pass'),
    'fantasy_points': _nullable_str_to_float_parser('fantasy_points'),
    'fantasy_points_ppr': _nullable_str_to_float_parser('fantasy_points_ppr'),
    'draftkings_points': _nullable_str_to_float_parser('draftkings_points'),
    'fanduel_points': _nullable_str_to_float_parser('fanduel_points'),
    'vbd': _nullable_str_to_int_parser('vbd'),
    'fantasy_rank_pos': _nullable_str_to_int_parser('fantasy_rank_pos'),
    'fantasy_rank_overall': _nullable_str_to_int_parser('fantasy_rank_overall'),
}  # type: Dict[str, FieldParser]


def parse_stats_table(
    table: BeautifulSoup,
    stat_row_attributes: Optional[Dict[str, Any]] = None,
    parsers: Optional[Dict[str, FieldParser]] = None,
) -> Tuple[List[str], List[List[Any]]]:
    if stat_row_attributes is None:
        stat_row_attributes = {}

    if parsers is None:
        parsers = {}  # type: Dict[str, FieldParser]

    parsers = {**PARSERS, **parsers}

    column_infos = []
    html_columns = table.find('thead').find_all('tr')[1]
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
