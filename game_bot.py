from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tmdb_scrape import get_connected_movies, get_movie_id
from datetime import datetime
import random

import time

def play_game():

    service = Service(executable_path="/Users/johnsader/PycharmProjects/Cine2Nerdle/chromedriver")
    driver = webdriver.Chrome(service=service)

    link = input("Paste Gamelink: ")

    driver.get(link)

    time.sleep(2)

    link = driver.find_element(By.CLASS_NAME, "battle-home-button")
    link.click()

    time.sleep(3)

    add_bans(driver)

    time.sleep(20)

    main_game(driver)

    driver.quit()

def add_bans(driver):

    time.sleep(3)


    input_element = driver.find_elements(By.CLASS_NAME, "battle-input")
    input_element[0].send_keys("Robert De Niro" + Keys.ENTER)
    input_element[1].send_keys("Martin Scorsese" + Keys.ENTER)
    input_element[2].send_keys("Leonardo DiCaprio" + Keys.ENTER)

    driver.execute_script("window.scrollBy(0, 250);")
    time.sleep(3)

    link = driver.find_element(By.CLASS_NAME, "battle-choose-bans-button")

    link.click()


def main_game(driver):

    game_end = False



    while not game_end:

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "battle-input"))
        )


        input_element = driver.find_element(By.CLASS_NAME, "battle-input")

        time.sleep(2)

        last_played_movie = driver.find_element(By.CLASS_NAME, "battle-board-movie")


        print(last_played_movie.text)
        movie_title = last_played_movie.text.split()
        print(movie_title)
        movie_year = str(movie_title[-1][1:-1])
        movie_title = " ".join(movie_title[2:-1])

        move_id = get_movie_id(movie_title, movie_year)
        movie_list = get_connected_movies(move_id)

        input_element.send_keys(movie_list[random.randint(0, 3)][random.randint(0,4)])
        link = driver.find_element(By.CLASS_NAME, "fa-sharp")

        link.click()

        time.sleep(1)



play_game()

