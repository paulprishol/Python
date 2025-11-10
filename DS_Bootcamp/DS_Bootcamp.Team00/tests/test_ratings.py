import pytest
from unittest.mock import mock_open, patch
from collections import Counter, defaultdict
from datetime import datetime
from movielens_analysis import Ratings, average, variance

MOCK_RATINGS_DATA = (
    "userId,movieId,rating,timestamp\n"
    "1,1,4.0,964982703\n"
    "1,2,3.0,964981247\n"
    "1,3,5.0,964983815\n"
    "2,1,3.5,964982931\n"
    "2,3,4.5,964982242\n"
)

MOCK_MOVIES_DATA = (
    "movieId,title,genres\n"
    "1,Toy Story,Animation|Adventure\n"
    "2,Jumanji,Adventure|Children\n"
    "3,Grumpier Old Men,Comedy|Romance\n"
)

@pytest.fixture
def mock_ratings_data():
    return MOCK_RATINGS_DATA

@pytest.fixture
def mock_movies_data():
    return MOCK_MOVIES_DATA

@pytest.fixture
def ratings(mock_ratings_data, mock_movies_data):
    with patch("builtins.open", mock_open(read_data=mock_ratings_data)) as mock_ratings, \
         patch("movielens_analysis.Ratings.load_movie_titles", return_value={1: "Toy Story", 2: "Jumanji", 3: "Grumpier Old Men"}):
        yield Ratings("ratings.csv")

class TestMoviesr:
    def test_dist_by_year(self, ratings):
        m = ratings.Movies(ratings.data, ratings.movie_titles)
        res = m.dist_by_year()
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == int, "Keys (years) must be integers"
            assert type(v) == int, "Values (counts) must be integers"
        k = list(res.keys())
        assert all(k[i] <= k[i+1] for i in range(len(k) - 1)), "Keys must be sorted in ascending order"
        assert res == {2000: 5}, "Expected year distribution"
        # краевой случай - пустые данные
        m_empty = ratings.Movies([], ratings.movie_titles)
        assert m_empty.dist_by_year() == {}, "Expected empty dict for empty data"

    def test_dist_by_rating(self, ratings):
        m = ratings.Movies(ratings.data, ratings.movie_titles)
        res = m.dist_by_rating()
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == float, "Keys (ratings) must be floats"
            assert type(v) == int, "Values (counts) must be integers"
        k = list(res.keys())
        assert all(k[i] <= k[i+1] for i in range(len(k) - 1)), "Keys must be sorted in ascending order"
        assert res == {3.0: 1, 3.5: 1, 4.0: 1, 4.5: 1, 5.0: 1}, "Expected rating distribution"
        # краевой случай - пустые данные
        m_empty = ratings.Movies([], ratings.movie_titles)
        assert m_empty.dist_by_rating() == {}, "Expected empty dict for empty data"

    def test_top_by_num_of_ratings(self, ratings):
        m = ratings.Movies(ratings.data, ratings.movie_titles)
        res = m.top_by_num_of_ratings(2)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == str, "Keys (movie titles) must be strings"
            assert type(v) == int, "Values (counts) must be integers"
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Values must be sorted in descending order"
        assert res == {"Toy Story": 2, "Grumpier Old Men": 2}, "Expected top movies by ratings count"
        # краевой случай - пустые данные
        m_empty = ratings.Movies([], ratings.movie_titles)
        assert m_empty.top_by_num_of_ratings(2) == {}, "Expected empty dict for empty data"

    def test_top_by_ratings(self, ratings):
        m = ratings.Movies(ratings.data, ratings.movie_titles)
        res = m.top_by_ratings(2, metric=average)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == str, "Keys (movie titles) must be strings"
            assert type(v) == float, "Values (metric) must be floats"
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Values must be sorted in descending order"
        assert res == {"Grumpier Old Men": 4.75, "Toy Story": 3.75}, "Expected top movies by average rating"
        # краевой случай - пустые данные
        m_empty = ratings.Movies([], ratings.movie_titles)
        assert m_empty.top_by_ratings(2, metric=average) == {}, "Expected empty dict for empty data"

    def test_top_controversial(self, ratings):
        m = ratings.Movies(ratings.data, ratings.movie_titles)
        res = m.top_controversial(2)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == str, "Keys (movie titles) must be strings"
            assert type(v) == float, "Values (variance) must be floats"
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Values must be sorted in descending order"
        assert res == {"Toy Story": 0.12, "Grumpier Old Men": 0.12}, "Expected top controversial movies"
        # краевой случай - пустые данные
        m_empty = ratings.Movies([], ratings.movie_titles)
        assert m_empty.top_controversial(2) == {}, "Expected empty dict for empty data"

    def test_top_rated_by_user(self, ratings):
        m = ratings.Movies(ratings.data, ratings.movie_titles)
        res = m.top_rated_by_user(1, 2)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == str, "Keys (movie titles) must be strings"
            assert type(v) == float, "Values (ratings) must be floats"
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Values must be sorted in descending order"
        assert res == {"Grumpier Old Men": 5.0, "Toy Story": 4.0}, "Expected top rated movies by user 1"
        # краевой случай - несуществующий userId
        res_empty = m.top_rated_by_user(999, 2)
        assert res_empty == {}, "Expected empty dict for non-existent user"

class TestUsersr:
    def test_user_by_num_of_rat(self, ratings):
        u = ratings.Users(ratings.data, ratings.movie_titles)
        res = u.user_by_num_of_rat()
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == int, "Keys (userId) must be integers"
            assert type(v) == int, "Values (counts) must be integers"
        k = list(res.keys())
        assert all(k[i] <= k[i+1] for i in range(len(k) - 1)), "Keys must be sorted in ascending order"
        assert res == {1: 3, 2: 2}, "Expected user ratings count"
        # краевой случай - пустые данные
        u_empty = ratings.Users([], ratings.movie_titles)
        assert u_empty.user_by_num_of_rat() == {}, "Expected empty dict for empty data"

    def test_user_by_med_rat(self, ratings):
        u = ratings.Users(ratings.data, ratings.movie_titles)
        res = u.user_by_med_rat(metric=average)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == int, "Keys (userId) must be integers"
            assert type(v) == float, "Values (metric) must be floats"
        k = list(res.keys())
        assert all(k[i] <= k[i+1] for i in range(len(k) - 1)), "Keys must be sorted in ascending order"
        assert res == {1: 4.0, 2: 4.0}, "Expected user average ratings"
        # краевой случай - пустые данные
        u_empty = ratings.Users([], ratings.movie_titles)
        assert u_empty.user_by_med_rat(metric=average) == {}, "Expected empty dict for empty data"

    def test_top_user_rat(self, ratings):
        u = ratings.Users(ratings.data, ratings.movie_titles)
        res = u.top_user_rat(2)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == int, "Keys (userId) must be integers"
            assert type(v) == float, "Values (variance) must be floats"
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Values must be sorted in descending order"
        assert res == {1: 1.0, 2: 0.5}, "Expected top users by rating variance"
        # краевой случай - пустые данные
        u_empty = ratings.Users([], ratings.movie_titles)
        assert u_empty.top_user_rat(2) == {}, "Expected empty dict for empty data"