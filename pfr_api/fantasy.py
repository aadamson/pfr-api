import pandas as pd
import requests
from bs4 import BeautifulSoup

from pfr_api.config import BASE_URL
from pfr_api.parse.parse import parse_stats_table
from pfr_api.parse.parser import PlayerRowParser


class Fantasy(object):
    def __init__(self, season):
        self._season = season

    def _fantasy_rankings_page(self) -> BeautifulSoup:
        url = (
            '{base}/years/{season}/fantasy.htm'
            .format(base=BASE_URL, season=self._season)
        )
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup

    def rankings(self) -> pd.DataFrame:
        soup = self._fantasy_rankings_page()
        results_table = soup.find('table', {'id': 'fantasy'})
        columns, rows = parse_stats_table(
            results_table,
            stat_row_attributes={'class': lambda x: x != 'thead'},
            parsers={'player': PlayerRowParser()})
        return pd.DataFrame(columns=columns, data=rows)
