import csv

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


tracking_data = [['Movie Recieved', 'Movie Played', 'Time to respond']]

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

    main_game(driver)

    driver.quit()

def add_bans(driver):

    time.sleep(3)


    input_element = driver.find_elements(By.CLASS_NAME, "battle-input")
    input_element[0].send_keys("Robert De Niro" + Keys.ENTER)
    input_element[1].send_keys("Martin Scorsese" + Keys.ENTER)
    input_element[2].send_keys("Leonardo DiCaprio" + Keys.ENTER)

    driver.execute_script("window.scrollBy(0, 250);")
    time.sleep(1)

    link = driver.find_element(By.CLASS_NAME, "battle-choose-bans-button")

    link.click()


def main_game(driver):

    game_end = False
    input_element = None

#Waits to find the battle board before starting the game
    WebDriverWait(driver, 90).until(
        EC.presence_of_element_located((By.CLASS_NAME, "battle-board-movie"))

    )

    while not game_end:

        start_time = time.time()

        WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CLASS_NAME, "battle-input"))

        )


        input_element = driver.find_element(By.CLASS_NAME, "battle-input")

        time.sleep(0.5)

        input_movie = driver.find_element(By.CLASS_NAME, "battle-board-movie")
        print(input_movie.text)
        if len(input_movie.text) !=0:

            print(input_movie.text)
            movie_title = input_movie.text.split()
            print(movie_title)
            movie_year = str(movie_title[-1][1:-1])
            movie_title = " ".join(movie_title[2:-1])

            move_id = get_movie_id(movie_title, movie_year)

            movie_list = get_connected_movies(move_id)


            movie_to_play = movie_list[random.randint(0, 2)][random.randint(0,2)]
            time.sleep(1)
            last_movie = driver.find_element(By.CLASS_NAME, "battle-board-movie")
            input_element.send_keys(movie_to_play)
            link = driver.find_element(By.CLASS_NAME, "fa-sharp")

            link.click()
            end_time = time.time()
            total_time = end_time - start_time

            export_data = [movie_title, movie_to_play, total_time]
            tracking_data.append(export_data)

            with open('game_data.csv', mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                csv_writer.writerows(tracking_data)



            time.sleep(1)



play_game()

