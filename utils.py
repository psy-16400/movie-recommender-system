import requests

TMDB_API_KEY = "4bbf84cd839ed501c3127fd8f874926a"

def fetch_movie_data_tmdb(title):
    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {'api_key': TMDB_API_KEY, 'query': title}
    response = requests.get(search_url, params=params).json()
    if response['results']:
        movie = response['results'][0]
        poster_path = movie.get('poster_path')
        imdb_id = fetch_imdb_id(movie['id'])
        return {
            'title': movie['title'],
            'poster': f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
            'imdb_url': f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None
        }
    return None

def fetch_imdb_id(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/external_ids"
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(url, params=params).json()
    return response.get('imdb_id')
