import requests

TMDB_API_KEY = "4bbf84cd839ed501c3127fd8f874926a"

def fetch_movie_data_tmdb(title):
    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {'api_key': TMDB_API_KEY, 'query': title}
    response = requests.get(search_url, params=params).json()

    if response['results']:
        movie = response['results'][0]
        poster_path = movie.get('poster_path')
        tmdb_id = movie['id']
        imdb_id, imdb_rating = fetch_imdb_info(tmdb_id)
        return {
            'title': movie['title'],
            'poster': f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
            'imdb_url': f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None,
            'rating': imdb_rating
        }
    return None

def fetch_imdb_info(tmdb_id):
    ext_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
    movie_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {'api_key': TMDB_API_KEY}

    imdb_id = requests.get(ext_url, params=params).json().get('imdb_id')
    imdb_rating = requests.get(movie_url, params=params).json().get('vote_average')

    return imdb_id, imdb_rating
