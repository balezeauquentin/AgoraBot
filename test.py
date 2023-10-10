import time
import pyautogui
import random
import requests
import sqlite3
import unittest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import threading

idt = "unlapinrameur"
motdp = "leslapins"


def bonjour():
    print("hello world")


thread1 = threading.Thread(target=bonjour())
thread2 = threading.Thread(target=bonjour())
thread3 = threading.Thread(target=bonjour())
thread4 = threading.Thread(target=bonjour())


# driver = webdriver.Firefox()
# driver.get('https://agora-quiz.education/Games/List')
# element = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='username']")
# element.send_keys("lapin")
# driver.quit()
