import requests

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
    page = 1

    while page < 501:

        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&primary_release_year={year}&sort_by=popularity.desc'

        response = requests.get(url, headers=headers)
        results = response.json()

        for j in range(20):
            if results['results'][j]['title'] == movie:
                return results['results'][j]['id']

        page += 1

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
    print(results)
    print(len(results['cast']))

    i=0
    while i < min(5, len(results['cast'])):
        movie = results['cast'][i]

        if movie['media_type'] == 'movie':
            print(movie['id'])
            return_list.append(get_movie(movie['id']))

        i+=1

    return return_list
def get_connected_movies(id):

    return_list = []

    url = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"

    response = requests.get(url, headers=headers)

    results = response.json()

    for i in range(4):
        return_list.append(get_cast_movies(results['cast'][i]['id']))


    return return_list

def get_movie(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    response = requests.get(url, headers=headers)
    results = response.json()

    return results['title'] + " (" + results['release_date'][:4] + ")"

print(get_cast_movies(1945702))