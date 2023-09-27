import time
import pyautogui
import unittest
import random
import sqlite3
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Firefox()

idt = "unlapinrameur"
motdp = "leslapins"

idt2="QuantumScribe"
motdp2=";AgoraBot0"
conn = sqlite3.connect('QR.db')


def rajouter_sql(question,reponse):
    # Connexion à la base de données SQLite (ou création si elle n'existe pas)
    conn = sqlite3.connect('QR.db')

    # Création d'un curseur
    cursor = conn.cursor()

    # Variables contenant la question et la réponse
    nouvelle_question = "Quelle est la capitale de la France ?"
    nouvelle_reponse = "La capitale de la France est Paris."

    # Requête SQL pour insérer la nouvelle entrée
    requete = "INSERT INTO ma_table (Question, Reponse) VALUES (?, ?)"
    cursor.execute(requete, (nouvelle_question, nouvelle_reponse))

    # Valide la transaction
    conn.commit()

    # Ferme la connexion à la base de données
    conn.close()
def get_html():
    url = driver.current_url
    response = requests.get(url)

    # Vérifie si la requête a réussi
    if response.status_code == 200:
        # Obtient le contenu de la page web
        html_content = response.text

        # Utilise BeautifulSoup pour analyser le code HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Obtient le code HTML complet sous forme de chaîne de caractères avec l'indentation (prettify)
        html_string = soup.prettify()

        # Maintenant, html_string contient tout le code HTML de la page web
        print(html_string)
        return html_string

    else:
        print('La requête a échoué avec le code de statut :', response.status_code)
        return None

def obtenir_reponse(question):
    cursor = conn.cursor()
    cursor.execute('SELECT ReponseText FROM Reponses INNER JOIN Questions ON Reponses.QuestionID = Questions.QuestionID WHERE Questions.QuestionText = ?', (question,))
    result = cursor.fetchone()
    return result[0] if result else None
def partie():
    for i in range(3):
        time.sleep(5)
        element_question = driver.find_element(By.CSS_SELECTOR,'.question-content b')
        soup = BeautifulSoup(element_question.get_attribute('outerHTML'), 'html.parser')
        texte_question = soup.get_text()
        reponse = obtenir_reponse(texte_question)
        if reponse:
            print("Réponse :", reponse)
            expression_xpath = f'//button[contains(text(), "{reponse}")]'
            bouton_reponse = driver.find_element(By.XPATH,expression_xpath)
            bouton_reponse.click()
        else:
            boutons_aleatoires = driver.find_elements(By.CSS_SELECTOR,'button.mat-raised-button')

            # Choisis un bouton au hasard parmi ceux trouvés
            if boutons_aleatoires:
                bouton_choisi = random.choice(boutons_aleatoires)

                # Clique sur le bouton choisi
                bouton_choisi.click()
                time.sleep(3)
            else:
                print("Aucun bouton trouvé")

    html_content = get_html()

    # Utilise BeautifulSoup pour analyser le code HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Sélectionne toutes les sections de réponses
    sections = soup.find_all('app-user-answer')

    # Boucle à travers les sections de réponses
    for section in sections:
        # Extrait la question
        question = section.find('div', class_='question-div').text.strip()

        # Extrait la réponse
        response_div = section.find('div', class_='good-answer-div')
        if response_div:
            response = response_div.find('b', class_='success-text').text.strip()
        else:
            response = "Aucune réponse trouvée"

def connection(idt,motdp):
    identifiant = driver.find_element(By.ID, "mat-input-0")
    identifiant.send_keys(idt)
    mdp = driver.find_element(By.ID, "mat-input-1")
    mdp.send_keys(motdp)
    bouton = driver.find_element(By.CLASS_NAME,"primary-button")
    bouton.click()
    
    bouton_jouer = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located(By.XPATH, '//button[contains(.,"Jouer des Parties")]'))
    )
    bouton_jouer.click()

    
def start_partie(idt2):
    input_adversaire=driver.find_element(By.ID,"mat-input-3")
    input_adversaire.send_keys(idt2)

    
    
    bouton_inviter = driver.find_element(By.XPATH, '//button[contains(.,"Inviter")]')
    bouton_inviter.click()
    time.sleep(3)
    largeur_ecran, hauteur_ecran = pyautogui.size()
    x_centre = largeur_ecran // 2
    y_centre = hauteur_ecran // 2
    pyautogui.click(x_centre, y_centre)
    time.sleep(3)
    boutons_similaires = driver.find_element(By.CSS_SELECTOR,'.mat-raised-button.theme-button')
    boutons_similaires.click()
    time.sleep(3)
    partie()
    time.sleep(3)
    


driver.get('https://agora-quiz.education/Games/List')
url_actuelle = driver.current_url
if url_actuelle == "https://agora-quiz.education/Login":
    connection(idt,motdp)
    time.sleep(3)
    print("lapin")
    start_partie(idt2)

time.sleep(100)
conn.close()
driver.quit()
