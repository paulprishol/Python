from movielens_analysis import Movies
from unittest.mock import mock_open, patch
import pytest

MOCK_MOVIES_DATA = (
    "movieId,title,genres\n"
    "1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy\n"
    "2,Jumanji (1995),Adventure|Children|Fantasy\n"
    "3,Grumpier Old Men (1995),Comedy|Romance\n"
    "4,Three Colors: Red (Trois couleurs: Rouge) (1994),Drama\n"
    "5,Three Colors: Blue (Trois couleurs: Bleu) (1993),Drama\n"
    "6,Heat (1995),Action|Crime|Thriller\n"
    "7,Sabrina (1995),Comedy|Romance\n"
    "8,Tom and Huck (1995),Adventure|Children\n"
    "9,Sudden Death (1995),Action\n"
    "10,Strange Days (1995),Action|Crime|Drama|Mystery|Sci-Fi|Thriller\n"
)

@pytest.fixture
def mock_movie_data():
    return MOCK_MOVIES_DATA

@pytest.fixture
def movies(mock_movie_data):
    with patch("builtins.open", mock_open(read_data=mock_movie_data)):
        yield Movies('movies.csv')

class Test_Movies:
    def test_movies_dist_by_release(self, movies):
        res = movies.dist_by_release()
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str
            assert type(v) == int
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1))
        assert res['1995'] == 8
        assert res['1994'] == 1

    def test_movies_dist_by_genres(self, movies):
        res = movies.dist_by_genres()
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str
            assert type(v) == int
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1))
        assert res['Drama'] == 3
        assert res['Comedy'] == 3
        assert res['Sci-Fi'] == 1

    def test_movies_most_genres(self, movies):
        res = movies.most_genres(1000)
        assert type(res) == dict
        for k, v in res.items():
            assert type(k) == str
            assert type(v) == int
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1))
        assert res['Strange Days'] == 6
        assert res['Sudden Death'] == 1

    def test_movies_movies_by_genre(self, movies):
        res = movies.movies_by_genre('Comedy')
        assert type(res) == list
        for movie in res:
            assert type(movie) == str
        assert res[0] == 'Toy Story (1995)'
        assert res[1] == 'Grumpier Old Men (1995)'
