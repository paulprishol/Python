import pytest
from tests.test_ratings import TestMoviesr, TestUsersr, ratings, mock_movies_data, mock_ratings_data
from tests.test_tags import TestTags, mock_tags_data, tags
from tests.test_movies import Test_Movies, mock_movie_data, movies
from tests.test_links import Test_Links, mock_links_data, links

if __name__ == "__main__":
    pytest.main()