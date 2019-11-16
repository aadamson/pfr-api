from typing import Any, Dict, List, Optional, Tuple, Union

from bs4 import BeautifulSoup


def _str_to_int_parser(field_str: str) -> int:
    return int(field_str)


def _nullable_str_to_int_parser(field_str: str) -> Union[None, int]:
    if not field_str:
        return None
    return int(field_str)


def _str_to_float_parser(field_str: str) -> float:
    return float(field_str)


def _nullable_str_to_float_parser(field_str: str) -> Union[None, float]:
    if not field_str:
        return None
    return float(field_str)


def _str_percentage_to_float_parser(field_str: str) -> float:
    percentage = float(field_str[:-1])
    return percentage / 100.


def _nullable_str_percentage_to_float_parser(field_str: str) -> Union[None, float]:
    if not field_str:
        return None
    percentage = float(field_str[:-1])
    return percentage / 100.


PARSERS = {
    'year_id': _str_to_int_parser,
    'game_date': lambda x: x,
    'game_num': _str_to_int_parser,
    'week_num': _str_to_int_parser,
    'age': lambda x: x,
    'team': lambda x: x,
    'game_location': lambda x: x,
    'opp': lambda x: x,
    'game_result': lambda x: x,
    'gs': lambda x: x == '*',
    'pass_cmp': _str_to_int_parser,
    'pass_att': _str_to_int_parser,
    'pass_cmp_perc': _nullable_str_percentage_to_float_parser,
    'pass_yds': _str_to_int_parser,
    'pass_td': _str_to_int_parser,
    'pass_int': _str_to_int_parser,
    'pass_rating': _nullable_str_to_float_parser,
    'pass_sacked': _str_to_int_parser,
    'pass_sacked_yds': _str_to_int_parser,
    'pass_yds_per_att': _nullable_str_to_float_parser,
    'pass_adj_yds_per_att': _nullable_str_to_float_parser,
    'rush_att': _str_to_int_parser,
    'rush_yds': _str_to_int_parser,
    'rush_yds_per_att': _nullable_str_to_float_parser,
    'rush_td': _str_to_int_parser,
    'targets': _str_to_int_parser,
    'rec': _str_to_int_parser,
    'rec_yds': _str_to_int_parser,
    'rec_yds_per_rec': _nullable_str_to_float_parser,
    'rec_td': _str_to_int_parser,
    'catch_pct': _str_percentage_to_float_parser,
    'rec_yds_per_tgt': _nullable_str_to_float_parser,
    'two_pt_md': _nullable_str_to_int_parser,
    'all_td': _str_to_int_parser,
    'scoring': _str_to_int_parser,
    'fumbles': _str_to_int_parser,
    'fumbles_lost': _str_to_int_parser,
    'fumbles_forced': _str_to_int_parser,
    'fumbles_rec': _str_to_int_parser,
    'fumbles_rec_yds': _str_to_int_parser,
    'fumbles_rec_td': _str_to_int_parser,
    'offense': _str_to_int_parser,
    'off_pct': _str_percentage_to_float_parser,
    'defense': _str_to_int_parser,
    'def_pct': _str_percentage_to_float_parser,
    'special_teams': _str_to_int_parser,
    'st_pct': _str_percentage_to_float_parser,
    'kick_ret': _str_to_int_parser,
    'kick_ret_yds': _str_to_int_parser,
    'kick_ret_yds_per_ret': _nullable_str_to_float_parser,
    'kick_ret_td': _str_to_int_parser,
    'punt_ret': _str_to_int_parser,
    'punt_ret_yds': _str_to_int_parser,
    'punt_ret_yds_per_ret': _nullable_str_to_float_parser,
    'punt_ret_td': _str_to_int_parser,

    # Fantasy-specific
    'player': lambda x: x,
    'fantasy_pos': lambda x: x,
    'g': _nullable_str_to_int_parser,
    # 'gs': _str_to_int_parser,  TODO how to handle ambiguity
    'two_pt_pass': _nullable_str_to_float_parser,
    'fantasy_points': _nullable_str_to_float_parser,
    'fantasy_points_ppr': _nullable_str_to_float_parser,
    'draftkings_points': _nullable_str_to_float_parser,
    'fanduel_points': _nullable_str_to_float_parser,
    'vbd': _nullable_str_to_int_parser,
    'fantasy_rank_pos': _nullable_str_to_int_parser,
    'fantasy_rank_overall': _nullable_str_to_int_parser,
}


def _parse_stats_table(
    table: BeautifulSoup,
    stat_row_attributes: Optional[Dict[str, Any]] = None
) -> Tuple[List[Tuple[str, Any]], List[List[Any]]]:
    if stat_row_attributes is None:
        stat_row_attributes = {}

    column_infos = []
    html_columns = table.find('thead').find_all('tr')[1]
    for column in html_columns.find_all('th'):
        stat = column['data-stat']
        name = column.text
        column_infos.append((stat, name))
    column_infos = column_infos[1:]  # Skip the ranker column

    rows = []
    html_body = table.find('tbody')
    html_rows = html_body.find_all(
        'tr', recursive=False, **stat_row_attributes)
    for html_row in html_rows:
        row = [None] * len(column_infos)
        for i, ((column_stat, column_name), html_row_col) in enumerate(
            zip(column_infos, html_row.find_all('td', recursive=False))
        ):
            parser = PARSERS[column_stat]
            row[i] = parser(html_row_col.text)
        rows.append(row)

    return column_infos, rows
