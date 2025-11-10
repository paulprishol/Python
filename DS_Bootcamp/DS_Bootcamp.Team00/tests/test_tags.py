import pytest
from unittest.mock import mock_open, patch
from movielens_analysis import Tags

MOCK_TAGS_DATA = (
    "userId,movieId,tag,timestamp\n"
    "1,1,animation,964982703\n"
    "1,1,funny,964982704\n"
    "2,1,family,964982931\n"
    "2,3,comedy,964982242\n"
    "3,1,animation,964982905\n"
)

@pytest.fixture
def mock_tags_data():
    return MOCK_TAGS_DATA

@pytest.fixture
def tags(mock_tags_data):
    with patch("builtins.open", mock_open(read_data=mock_tags_data)):
        yield Tags("tags.csv")

class TestTags:
    def test_most_words(self, tags):
        res = tags.most_words(2)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == str, "Keys (tags) must be strings"
            assert type(v) == int, "Values (word counts) must be integers"
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Values must be sorted in descending order"
        assert res == {"animation": 1, "funny": 1}, "Expected tags by word count"
        # краевой случай - пустые данные
        tags_empty = Tags("tags.csv")
        tags_empty.data = []
        assert tags_empty.most_words(2) == {}, "Expected empty dict for empty data"

    def test_longest(self, tags):
        res = tags.longest(2)
        assert type(res) == list, "Result must be a list"
        for item in res:
            assert type(item) == str, "Items (tags) must be strings"
        v = [len(item) for item in res]
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Items must be sorted by length in descending order"
        assert res == ["animation", "family"], "Expected longest tags"
        # краевой случай - пустые данные
        tags_empty = Tags("tags.csv")
        tags_empty.data = []
        assert tags_empty.longest(2) == [], "Expected empty list for empty data"

    def test_most_words_and_longest(self, tags):
        res = tags.most_words_and_longest(2)
        assert type(res) == list, "Result must be a list"
        for item in res:
            assert type(item) == str, "Items (tags) must be strings"
        assert res == sorted(res), "List must be sorted alphabetically"
        most_words = set(tags.most_words(2).keys())
        most_chars = set(tags.longest(2))
        assert all(item in most_words and item in most_chars for item in res), "Items must be in intersection"
        assert res == ["animation"], "Expected intersection of most words and longest tags"
        # краевой случай - пустые данные
        tags_empty = Tags("tags.csv")
        tags_empty.data = []
        assert tags_empty.most_words_and_longest(2) == [], "Expected empty list for empty data"

    def test_most_popular(self, tags):
        res = tags.most_popular(2)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == str, "Keys (tags) must be strings"
            assert type(v) == int, "Values (counts) must be integers"
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Values must be sorted in descending order"
        assert res == {"animation": 2, "funny": 1}, "Expected most popular tags"
        # краевой случай - пустые данные
        tags_empty = Tags("tags.csv")
        tags_empty.data = []
        assert tags_empty.most_popular(2) == {}, "Expected empty dict for empty data"

    def test_tags_with(self, tags):
        res = tags.tags_with("action")
        assert type(res) == list, "Result must be a list"
        for item in res:
            assert type(item) == str, "Items (tags) must be strings"
        assert res == sorted(res), "List must be sorted alphabetically"
        assert res == [], "Expected no tags containing 'action'"
        res_animation = tags.tags_with("animation")
        assert res_animation == ["animation"], "Expected tags containing 'animation'"
        # краевой случай - пустые данные
        tags_empty = Tags("tags.csv")
        tags_empty.data = []
        assert tags_empty.tags_with("action") == [], "Expected empty list for empty data"

    def test_popular_tags_by_movie(self, tags):
        res = tags.popular_tags_by_movie(1, 2)
        assert type(res) == dict, "Result must be a dictionary"
        for k, v in res.items():
            assert type(k) == str, "Keys (tags) must be strings"
            assert type(v) == int, "Values (counts) must be integers"
        v = list(res.values())
        assert all(v[i] >= v[i+1] for i in range(len(v) - 1)), "Values must be sorted in descending order"
        assert res == {"animation": 2, "funny": 1}, "Expected popular tags for movieId=1"
        # краевой случай - несуществующий movieId
        res_empty = tags.popular_tags_by_movie(999, 2)
        assert res_empty == {}, "Expected empty dict for non-existent movie"
        # краевой случай - пустые данные
        tags_empty = Tags("tags.csv")
        tags_empty.data = []
        assert tags_empty.popular_tags_by_movie(1, 2) == {}, "Expected empty dict for empty data"