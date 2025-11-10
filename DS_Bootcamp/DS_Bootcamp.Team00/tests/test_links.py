from movielens_analysis import Links
from unittest.mock import mock_open, patch
import pytest

MOCK_LINKS_DATA = (
    "movieId,imdbId,tmdbId\n"
    "1,0114709,862\n"
    "2,0113497,8844\n"
    "3,0113228,15602\n"
    "4,0114885,31357\n"
    "5,0113041,11862\n"
)

@pytest.fixture
def mock_links_data():
    return MOCK_LINKS_DATA

@pytest.fixture
def links(mock_links_data):
    with patch("builtins.open", mock_open(read_data=mock_links_data)):
        yield Links('movies.csv')

class Test_Links:
    def test_links_get_imdb(self, links):
        movies = [_ for _ in range(1, 6)]
        fields = ['Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime']
        res = links.get_imdb(movies, fields)
        assert type(res) == list
        for data in res:
            assert type(data) == list
        assert all(int(res[i][0]) >= int(res[i+1][0]) for i in range(len(res) - 1))
        assert res[4] == ['1', 'John Lasseter', '$30,000,000 (estimated)', '$394,436,586', '1h 21m(81 min)'] 

    def test_links_top_directors(self, links):
        res = links.top_directors(5)
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str
            assert type(v) == int
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1))
        assert res['John Lasseter'] == 1
        assert res['Joe Johnston'] == 1

    def test_links_most_expensive(self, links):
        res = links.most_expensive(5)
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str
            assert type(v) == str or type(v) == type(None)
        v = list(res.values())
        v = [i for i in v if i is not None]
        for i in range(len(v) - 1):
            budget = int(''.join(filter(lambda x: x.isdigit(), v[i])))
            next_budget = int((''.join(filter(lambda x: x.isdigit(), v[i+1]))))
            assert budget >= next_budget
        assert res['Джуманджи'] == '$65,000,000'
        assert res['История игрушек'] == '$30,000,000'

    def test_links_most_profitable(self, links):
        res = links.most_profitable(5)
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str
            assert type(v) == str or type(v) == type(None)
        v = list(res.values())
        v = [i for i in v if i is not None]
        for i in range(len(v) - 1):
            profit = int(''.join(filter(lambda x: x.isdigit(), v[i]))) 
            if '-' in v[i]:
                profit *= -1
            next_profit = int((''.join(filter(lambda x: x.isdigit(), v[i+1]))))
            if '-' in v[i+1]:
                next_profit *= -1
            assert profit >= next_profit
        assert res['История игрушек'] == '$364436586'

    def test_links_longest(self, links):
        res = links.longest(5)
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str
            assert type(v) == str or type(v) == type(None)
        v = list(res.values())
        v = [i for i in v if i is not None]
        for i in range(len(v) - 1):
            runtime = v[i].split('(')[1]
            int_runtime = int(''.join(filter(lambda x: x.isdigit(), runtime)))
            next_runtime = v[i+1].split('(')[1]
            next_int_runtime = int(''.join(filter(lambda x: x.isdigit(), next_runtime)))
            assert int_runtime >= next_int_runtime
        assert res['В ожидании выдоха'] == '2h 4m(124 min)'
        assert res['История игрушек'] == '1h 21m(81 min)'

    def test_links_top_cost_per_minute(self, links):
        res = links.top_cost_per_minute(5)
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str
            assert type(v) == str or type(v) == type(None)
        v = list(res.values())
        v = [i for i in v if i is not None]
        assert all(float(v[i][1:]) >= float(v[i+1][1:]) for i in range(len(v) - 1))
        assert res['Джуманджи'] == '$625000.0'

    def test_links_dist_by_country(self, links):
        res = links.dist_by_country()
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str or type(k) == type(None)
            assert type(v) == int
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1))
        assert res['United States'] == 5