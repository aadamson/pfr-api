import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from pfr_api.config import BASE_URL
from pfr_api.parse.parse import parse_stats_table


class Player(object):
    entity_type = 'players'

    def __init__(
        self,
        name: str,
        player_id: str,
    ):
        self._name = name
        self._player_id = player_id

    def _url_base(self):
        return (
            '{base}/{entity}/{first}/{id}'
            .format(
                base=BASE_URL,
                entity=self.entity_type,
                first=self._player_id[0],
                id=self._player_id
            )
        )

    def _gamelog_page(self, season: str = '') -> BeautifulSoup:
        url = (
            '{base}/gamelog/{season}'
            .format(base=self._url_base(), season=season)
        )
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup

    def regular_season_gamelog(self, season: str = '') -> pd.DataFrame:
        soup = self._gamelog_page(season)
        results_table = soup.find('table', {'id': 'stats'})
        columns, rows = parse_stats_table(
            results_table,
            stat_row_attributes={'id': re.compile('^stats\..*$')})
        return pd.DataFrame(columns=columns, data=rows)

    def playoffs_gamelog(self, season: str = '') -> pd.DataFrame:
        soup = self._gamelog_page(season)
        results_table = soup.find('table', {'id': 'stats_playoffs'})
        columns, rows = parse_stats_table(
            results_table,
            stat_row_attributes={'id': re.compile('^stats\..*$')})
        return pd.DataFrame(columns=columns, data=rows)
