import re, csv
import requests
from collections import Counter, defaultdict
from datetime import datetime
from bs4 import BeautifulSoup
import sys

def average(data):
    return sum(data) / len(data) if data else 0

def variance(data):
    if len(data) < 2:
        return 0

    mean_value = average(data)
    return sum((x - mean_value) ** 2 for x in data) / (len(data) - 1)

class Movies:
    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.lines = self.file_reader(1000)

    def dist_by_release(self):
        gen = (line for line in self.lines)
        dates = []
        pattern = r' \(\d{4}\)'
        for line in gen:
            title = line[1]
            if re.search(pattern, title):
                dates.append(title[-5:-1])
            else:
                dates.append('-')
        release_years = dict(Counter(dates).most_common())
        return release_years
    
    def dist_by_genres(self):
        gen = (line for line in self.lines)
        genres_list = []
        for line in gen:
            genres_list += line[2].split('|')
        genres = dict(Counter(genres_list).most_common())
        return genres
        
    def most_genres(self, n):
        gen = (line for line in self.lines)
        movies_dict = {}
        for line in gen:
            title = line[1][:-6]
            genres_count = len(line[2].split('|'))
            movies_dict[title.strip()] = genres_count
        movies = dict(Counter(movies_dict).most_common(n))
        return movies
    
    #дополнительный метод: возвращает список фильмов, соответствующих определённому жанру
    def movies_by_genre(self, genre: str):
        gen = (line for line in self.lines)
        movies = []
        for line in gen:
            if genre.lower() in line[2].lower():
                movies.append(line[1])
        return movies

    def file_reader(self, n):
        try:
            data = self.gen_read()
            next(data)
            lines = []
            for i, line in enumerate(data):
                if ',"' in line and '",' in line:
                    tmp = list(map(lambda x: x.rstrip(), line.rstrip('\n').split(',"')))
                    lines.append([tmp[0]] + tmp[1].split('",'))
                else:
                    lines.append(list(map(lambda x: x.rstrip(), line.rstrip('\n').split(','))))
                if len(lines[i]) != 3 or not(lines[i][0].isdigit()):
                    raise Exception
                if i == n:
                    data.close()
                    break
            return lines
        except (AttributeError, ValueError, TypeError, KeyError) as e:
            print(e)
        except Exception:
            print('Error: Incorrect file structure')

    def gen_read(self):
        try:
            with open(self.path, 'r') as file:
                for line in file:
                    yield line
        except FileNotFoundError as e:
            print(e)

class Links:
    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.lines = self.file_reader(100)
    
    def get_imdb(self, list_of_movies, list_of_fields):
        imdb_info = []
        movies = (str(movie) for movie in sorted([int(movie) for movie in list_of_movies], reverse=True))
        for movie in movies:
            movieId = self.check_id(movie, 1)
            if movieId:
                imdb_info.append([movie])
                url = f"https://www.imdb.com/title/tt{movieId}/"
                response = self.request(url)
                if response is not None and response.status_code != 200:
                    imdb_info[len(imdb_info) - 1].append(f'Error: Failed connection (code: {response.status_code})')
                    continue
                if response.url != url:
                    imdb_info[len(imdb_info) - 1].append(f'Error: Movie {movieId} not found on IMDB')
                    continue
                fields = (str(field) for field in list_of_fields)
                for field in fields:
                    result = self.parse(response, field)
                    if result:
                        imdb_info[len(imdb_info) - 1].append(', '.join(result))
                    else:
                        imdb_info[len(imdb_info) - 1].append(None)
            else:
                imdb_info.append([None])
        return imdb_info
        
    def top_directors(self, n):
        directors = {}
        movies = [line[0] for line in self.lines]
        movies_and_directors = self.get_imdb(movies, ['Director'])
        for data in movies_and_directors:
            if self.skip(data):
                continue
            directors_list = data[1:]
            for director in directors_list:
                if director not in directors:
                    directors[director] = 1
                else:
                    directors[director] += 1
        directors = dict(sorted(directors.items(), key=lambda x: x[1] if x[1] is not None else "", reverse=True)[:n])
        return directors
        
    def most_expensive(self, n):
        budgets = {} 
        movies = [line[0] for line in self.lines]
        titles_and_budgets = self.get_imdb(movies, ['title', 'budget'])
        for data in titles_and_budgets:
            if self.skip(data):
                continue
            title = data[1]
            budget = data[2]
            if budget is not None:
                budget_int = int(''.join(filter(lambda x: x.isdigit(), budget)))
            else:
                budget_int = None
            budgets[title] = [budget, budget_int] 
        budgets = dict(sorted(budgets.items(), key=lambda x: x[1][1] if x[1][1] is not None else 0, reverse=True)[:n])
        for k, v in budgets.items():
            if v[0] is not None:
                budgets[k] = v[0].replace(' (estimated)', '')
            else:
                budgets[k] = v[0]
        return budgets
        
    def most_profitable(self, n):
        profits = {} 
        movies = [line[0] for line in self.lines]
        titles_grosses_budgets = self.get_imdb(movies, ['title', 'cumulative worldwide gross', 'budget'])
        for data in titles_grosses_budgets:
            if self.skip(data):
                continue
            title = data[1]
            gross = data[2]
            budget = data[3]
            if budget is not None:
                budget_int = int(''.join(filter(lambda x: x.isdigit(), budget)))
                currency = budget[:1]
            else:
                budget_int, currency = None, None
            if gross is not None:
                gross_int = int(''.join(filter(lambda x: x.isdigit(), gross)))
            else:
                gross_int = None
            if gross is not None and budget is not None:
                profits[title] = [currency, gross_int - budget_int]
            else:
                profits[title] = [currency, None]
        profits = dict(sorted(profits.items(), key=lambda x: x[1][1] if x[1][1] is not None else -sys.maxsize - 1, reverse=True)[:n])
        for k, v in profits.items():
            if v[1] is not None:
                profits[k] = v[0] + str(v[1])
            else:
                profits[k] = v[1]
        return profits
        
    def longest(self, n):
        runtimes = {}
        movies = [line[0] for line in self.lines]
        movies_and_runtimes = self.get_imdb(movies, ['title', 'runtime'])
        for data in movies_and_runtimes:
            if self.skip(data):
                continue
            title = data[1]
            runtime = data[2]
            if runtime is not None:
                minutes = int(''.join(filter(lambda x: x.isdigit(), runtime.split('(')[1])))
                runtimes[title] = [runtime, minutes]
            else:
                runtimes[title] = [runtime, None] 
        runtimes = dict(sorted(runtimes.items(), key=lambda x: x[1][1] if x[1][1] is not None else 0, reverse=True)[:n])
        for k, v in runtimes.items():
            runtimes[k] = v[0]
        return runtimes
        
    def top_cost_per_minute(self, n):
        costs = {}
        movies = [line[0] for line in self.lines]
        movies_budgets_runtimes = self.get_imdb(movies, ['title', 'budget', 'runtime'])
        for data in movies_budgets_runtimes:
            if self.skip(data):
                continue
            title = data[1]
            budget = data[2]
            runtime = data[3]
            if runtime is not None:
                minutes = int(''.join(filter(lambda x: x.isdigit(), runtime.split('(')[1])))
            else:
                minutes = None
            if budget is not None:
                budget_int = int(''.join(filter(lambda x: x.isdigit(), budget)))
                currency = budget[:1]
            else:
                budget_int, currency = None, None
            if budget is not None and runtime is not None:
                costs[title] = [currency, budget_int / minutes]
            else:
                costs[title] = [currency, None]
        costs = dict(sorted(costs.items(), key=lambda x: x[1][1] if x[1][1] is not None else -sys.maxsize - 1, reverse=True)[:n])
        for k, v in costs.items():
            if v[1] is not None:
                costs[k] = v[0] + str(round(v[1], 2))
            else:
                costs[k] = v[1]
        return costs
    
    #дополнительный метод: подсчитывает количество стран, в которых создавался фильм, на основе данных из базы
    def dist_by_country(self):
        countries = {}
        movies = [line[0] for line in self.lines]
        movies_and_countries = self.get_imdb(movies, ['title', 'Country of origin'])
        for data in movies_and_countries:
            if self.skip(data):
                continue
            country = data[2:]
            for c in country:
                if c not in countries:
                    countries[c] = 1
                else:
                    countries[c] += 1
        countries = dict(sorted(countries.items(), key=lambda x: x[1] if x[1] is not None else 0, reverse=True))
        return countries

    def file_reader(self, n):
        try:
            data = self.gen_read()
            next(data)
            lines = []
            for i, line in enumerate(data):
                lines.append(line.rstrip('\n').rstrip().split(','))
                if len(lines[i]) != 3 or not(lines[i][0].isdigit()):
                    raise Exception
                if i == n:
                    data.close()
                    break
            return lines
        except (AttributeError, ValueError, TypeError, KeyError) as e:
            print(e)
        except Exception:
            print('Error: Incorrect file structure')

    def gen_read(self):
        try: 
            with open(self.path, 'r') as file:
                for line in file:
                    yield line
        except FileNotFoundError as e:
            print(e)

    def check_id(self, id: str, col: int):
        gen = (line for line in self.lines)
        for _, line in enumerate(gen):
            if id == line[0] and line[col] != '':
                return line[col]
        return None

    def request(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            }
            response = requests.get(url, headers=headers)
            return response
        except (requests.exceptions.RequestException, ConnectionError) as e:
            print(f'Connection error: {e}')
    
    def parse(self, response, field):
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all("li", class_="ipc-metadata-list__item")
        if 'title' == field.lower():
            return [soup.find("h1").text]
        pattern = re.compile(rf'.*{field.replace(' ', '')}.*', re.IGNORECASE)
        for li in items:
            labels = li.find_all(lambda tag: tag.name in ["span", "a"])
            label_texts = [l.get_text(strip=True) for l in labels]
            attr_match = any(pattern.search(str(v).replace(' ', '')) for v in li.attrs.values())
            if any(pattern.search(text.replace(' ', '')) for text in label_texts) or attr_match:
                value_container = li.find("div", class_="ipc-metadata-list-item__content-container")
                if value_container:
                    links = value_container.find_all("a")
                    if links:
                        return [a.get_text(strip=True) for a in links]
                    nested_items = value_container.find_all("li")
                    if nested_items:
                        return [ni.get_text(strip=True) for ni in nested_items]
                    return value_container.get_text(strip=True)
        return None
    
    def skip(self, data):
        False if data[0] is None or 'not found on IMDB' in data[1] or 'Error: Failed connection (code: ' in data[1] else True

class Ratings:
    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.lines = self.file_reader(1000)
        self.data = []
        self.movie_titles = self.load_movie_titles('ml-latest-small/movies.csv')
        self.load_data_csv()

    def file_reader(self, n):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)
                lines = []
                for i, row in enumerate(reader):
                    if i >= n:
                        break
                    if len(row) != 4:
                        raise ValueError("Incorrect file structure")
                    lines.append(row)
                return lines
        except FileNotFoundError:
            print(f"File {self.path} not found")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    def load_movie_titles(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                return {int(row[0]): row[1] for row in reader}
        except FileNotFoundError:
            print(f"File {path} not found")
            return {}
        except Exception as e:
            print(f"Error loading movie titles: {e}")
            return {}

    def load_data_csv(self):
        try:
            for row in self.lines:
                self.data.append({
                    "userId": int(row[0]),
                    "movieId": int(row[1]),
                    "rating": float(row[2]),
                    "timestamp": int(row[3])
                })
        except Exception as e:
            print(f"Error upload data: {e}")

    class Movies:
        def __init__(self, ratings_data, movie_titles):
            self.ratings_data = ratings_data
            self.movie_titles = movie_titles

        def dist_by_year(self):
            ratings_by_year = Counter(datetime.fromtimestamp(entry["timestamp"]).year for entry in self.ratings_data)
            return dict(sorted(ratings_by_year.items()))

        def dist_by_rating(self):
            ratings_distribution = Counter(entry["rating"] for entry in self.ratings_data)
            return dict(sorted(ratings_distribution.items()))

        def top_by_num_of_ratings(self, n):
            counts = Counter(entry["movieId"] for entry in self.ratings_data)
            top_n = sorted(counts.items(), key=lambda x: (-x[1], self.movie_titles.get(x[0], str(x[0]))))[:n]
            return {self.movie_titles.get(movie_id, str(movie_id)): count for movie_id, count in top_n}

        def top_by_ratings(self, n, metric=average):
            movie_rat = defaultdict(list)
            for entry in self.ratings_data:
                movie_rat[entry["movieId"]].append(entry["rating"])
            top_movies_metric = {
                movie_id: round(metric(ratings), 2)
                for movie_id, ratings in movie_rat.items()
            }
            top_n = sorted(top_movies_metric.items(), key=lambda x: (-x[1], self.movie_titles.get(x[0], str(x[0]))))[:n]
            return {self.movie_titles.get(movie_id, str(movie_id)): value for movie_id, value in top_n}

        def top_controversial(self, n):
            movie_rat = defaultdict(list)
            for entry in self.ratings_data:
                movie_rat[entry["movieId"]].append(entry["rating"])
            top_movies_variance = {
                movie_id: round(variance(ratings), 2)
                for movie_id, ratings in movie_rat.items()
                if len(ratings) > 1
            }
            top_n = sorted(top_movies_variance.items(), key=lambda x: (-x[1], self.movie_titles.get(x[0], str(x[0]))))[:n]
            return {self.movie_titles.get(movie_id, str(movie_id)): value for movie_id, value in top_n}

        # дополнительный метод - возвращает топ-n фильмов, которые конкретный пользователь (userId) оценил выше всего; ключи — заголовки фильмов, значения — их рейтинги
        def top_rated_by_user(self, user_id, n):
            try:
                user_ratings = [(entry["movieId"], entry["rating"]) for entry in self.ratings_data if entry["userId"] == user_id]
                top_ratings = sorted(user_ratings, key=lambda x: (-x[1], self.movie_titles.get(x[0], str(x[0]))))[:n]
                return {
                    self.movie_titles.get(movie_id, str(movie_id)): round(rating, 2)
                    for movie_id, rating in top_ratings
                }
            except Exception as e:
                print(f"Error in top_rated_by_user: {e}")
                return {}

    class Users(Movies):
        def __init__(self, ratings_data, movie_titles):
            super().__init__(ratings_data, movie_titles)

        def user_by_num_of_rat(self):
            user_rat = Counter(entry["userId"] for entry in self.ratings_data)
            return dict(sorted(user_rat.items()))

        def user_by_med_rat(self, metric=average):
            user_rat = defaultdict(list)
            for entry in self.ratings_data:
                user_rat[entry["userId"]].append(entry["rating"])
            user_rat_med = {
                user: round(metric(ratings), 2)
                for user, ratings in user_rat.items()
            }
            return dict(sorted(user_rat_med.items()))

        def top_user_rat(self, n):
            user_rat = defaultdict(list)
            for entry in self.ratings_data:
                user_rat[entry["userId"]].append(entry["rating"])
            top_user = {
                user: round(variance(ratings), 2)
                for user, ratings in user_rat.items()
                if len(ratings) > 1
            }
            return dict(sorted(top_user.items(), key=lambda x: (-x[1], x[0]))[:n])

class Tags:
    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.lines = self.file_reader(1000)
        self.data = []
        self.load_data_csv()
    
    def file_reader(self, n):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)
                lines = []
                for i, row in enumerate(reader):
                    if i >= n:
                        break
                    if len(row) != 4:
                        raise ValueError("Incorrect file structure")
                    lines.append(row)
                return lines
        except FileNotFoundError:
            print(f"File {self.path} not found")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def load_data_csv(self):
        try:
            for row in self.lines:
                self.data.append({
                    "userId": int(row[0]),
                    "movieId": int(row[1]),
                    "tag": row[2],
                    "timestamp": int(row[3])
                })
        except Exception as e:
            print(f"Error upload data: {e}")
    
    def most_words(self, n):
        big_tags = {}
        try:
            for entry in self.data:
                big_tags[entry["tag"]] = len(entry["tag"].split())
        except Exception as e:
            print(f"Error: {e}")
        return dict(sorted(big_tags.items(), key=lambda x: x[1], reverse=True)[:n])
    
    def longest(self, n):
        big_tags = {}
        try:
            for entry in self.data:
                big_tags[entry["tag"]] = len(entry["tag"])
        except Exception as e:
            print(f"Error: {e}")
        return [x[0] for x in sorted(big_tags.items(), key=lambda x: x[1], reverse=True)[:n]]
    
    def most_words_and_longest(self, n):
        most_chars = set(self.longest(n))
        most_words = set(self.most_words(n).keys())
        return sorted(list(most_words.intersection(most_chars)))
    
    def most_popular(self, n):
        try:
            tag_counts = Counter(entry["tag"] for entry in self.data)
            return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:n])
        except Exception as e:
            print(f"Error: {e}")
    
    def tags_with(self, word):
        tags_with_word = set()
        try:
            for entry in self.data:
                if word in entry["tag"].split():
                    tags_with_word.add(entry["tag"])
        except Exception as e:
            print(f"Error: {e}")
        return sorted(tags_with_word)
    
    # дополнительный метод - возвращает топ-n самых популярных тегов для указанного фильма (movieId); ключи — теги, значения — количество их упоминаний
    def popular_tags_by_movie(self, movie_id, n):
        try:
            movie_tags = Counter(entry["tag"] for entry in self.data if entry["movieId"] == movie_id)
            return dict(sorted(movie_tags.items(), key=lambda x: x[1], reverse=True)[:n])
        except Exception as e:
            print(f"Error in popular_tags_by_movie: {e}")
            return {}