import requests
import time

file_path = 'Auth_Token'
with open(file_path, 'r') as file:
    token = file.read()

headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + token
}


def prompt_movie():
    done = False

    while not done:

        movie = input("\nMovie: ")
        year = input("Year: ")

        id = get_movie_id(movie, year)
        if id != -1:
            print_cast(id)
        else:
            print("Movie not found :(")

        user_input = input("\nDone (y/n): ")
        done = user_input == "y"


def get_movie_id(movie, year):
    # Checking at three different page numbers each iteration through. Top will look at the top of the list,
    # while mid and bottom look at chunks in the middle. 500 is the max pages per year. Movies played are heavily
    # skewed towards the top of the list which is why the increments for get larger from top-bottom.
    # The max iterations is 250 which seems to take about 20s as is. Pretty unlikely to run out of time.

    top = 1
    mid = 16
    bottom = 250

    while bottom < 501:

        if top < 15:
            url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={top}&primary_release_year={year}&sort_by=popularity.desc'

            response = requests.get(url, headers=headers)
            results = response.json()

            for i in range(20):
                if results['results'][i]['title'] == movie:
                    end_time = time.time()
                    return results['results'][i]['id']

        if mid < 251:
            url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={mid}&primary_release_year={year}&sort_by=popularity.desc'

            response = requests.get(url, headers=headers)
            results = response.json()

            for j in range(20):
                if results['results'][j]['title'] == movie:
                    end_time = time.time()
                    return results['results'][j]['id']

        if bottom < 501:
            url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={bottom}&primary_release_year={year}&sort_by=popularity.desc'

            response = requests.get(url, headers=headers)
            results = response.json()

            for k in range(len(results['results'])):
                if results['results'][k]['title'] == movie:
                    end_time = time.time()
                    return results['results'][k]['id']

        top += 1
        mid += 1
        bottom += 1

    return -1


def print_cast(id):
    url = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"

    response = requests.get(url, headers=headers)

    results = response.json()

    for i in range(4):
        print("\n" + results['cast'][i]['name'] + ":")
        print_cast_movies(results['cast'][i]['id'])


def print_cast_movies(pid):
    url = f"https://api.themoviedb.org/3/person/{pid}/combined_credits?language=en-US"

    response = requests.get(url, headers=headers)
    results = response.json()

    for i in range(3):
        print_movie(results['cast'][i]['id'])


def print_movie(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    response = requests.get(url, headers=headers)
    results = response.json()

    print(results['title'])


def get_cast_movies(pid):
    return_list = []
    url = f"https://api.themoviedb.org/3/person/{pid}/combined_credits?language=en-US"

    response = requests.get(url, headers=headers)
    results = response.json()

    i = 0
    while i < min(5, len(results['cast'])):
        movie = results['cast'][i]

        if movie['media_type'] == 'movie':
            return_list.append(get_movie(movie['id']))

        i += 1

    return return_list


def get_connected_movies(id):
    return_list = []

    url = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"

    response = requests.get(url, headers=headers)

    results = response.json()

    i = 0
    while i < 5 or i < len(get_cast_movies(results['cast'])):
        return_list.append(get_cast_movies(results['cast'][i]['id']))

    return return_list


def get_movie(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    response = requests.get(url, headers=headers)
    results = response.json()

    return results['title'] + " (" + results['release_date'][:4] + ")"
