#-------------------------importation des modules-------------------------#

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

#-------------------------définition des variables-------------------------#

driver = webdriver.Firefox()

idt = "unlapinrameur"
motdp = "leslapins"

idt2="QuantumScribe"
motdp2=";AgoraBot0"
conn = sqlite3.connect('QR.db')

#-------------------------définition des fonctions-------------------------#

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


# Définition de la fonction obtenir_reponse avec un argument question
def obtenir_reponse(question):
    # Création d'un curseur pour exécuter une requête SQL
    cursor = conn.cursor()
    
    # Exécution de la requête SQL pour récupérer la réponse à la question donnée
    cursor.execute('SELECT ReponseText FROM Reponses INNER JOIN Questions ON Reponses.QuestionID = Questions.QuestionID WHERE Questions.QuestionText = ?', (question,))
    
    # Récupération du résultat de la requête
    result = cursor.fetchone()
    
    # Retourne la réponse si elle existe, sinon retourne None
    return result[0] if result else None


# Définition de la fonction connection avec deux arguments idt et motdp
def connection(idt,motdp):
    
    # Recherche de l'élément identifiant et envoi de la valeur de idt
    identifiant = driver.find_element(By.ID, "mat-input-0")
    identifiant.send_keys(idt)
    
    # Recherche de l'élément mdp et envoi de la valeur de motdp
    mdp = driver.find_element(By.ID, "mat-input-1")
    mdp.send_keys(motdp)
    
    # Recherche du bouton_connexion et clic dessus
    bouton_connexion = driver.find_element(By.CLASS_NAME,"primary-button")
    bouton_connexion.click()
    
    # Recherche du bouton_jouer et clic dessus après qu'il soit visible
    bouton_jouer = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Jouer des Parties")]')))
    bouton_jouer.click()

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


# Définition de la fonction connection avec deux arguments idt et motdp
def connection(idt,motdp):
    
    # Recherche de l'élément identifiant et envoi de la valeur de idt
    identifiant = driver.find_element(By.ID, "mat-input-0")
    identifiant.send_keys(idt)
    
    # Recherche de l'élément mdp et envoi de la valeur de motdp
    mdp = driver.find_element(By.ID, "mat-input-1")
    mdp.send_keys(motdp)
    
    # Recherche du bouton_connexion et clic dessus
    bouton_connexion = driver.find_element(By.CLASS_NAME,"primary-button")
    bouton_connexion.click()
    
    # Recherche du bouton_jouer et clic dessus après qu'il soit visible
    bouton_jouer = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Jouer des Parties")]')))
    bouton_jouer.click()

    
# Définition de la fonction start_partie avec un argument idt2
def start_partie(idt2):

    # Recherche de l'élément input_adversaire et envoi de la valeur de idt2
    input_adversaire = WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.ID,"mat-input-3")))
    input_adversaire.send_keys(idt2)
    
    # Recherche du bouton_inviter et clic dessus
    bouton_inviter = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Inviter")]')))
    bouton_inviter.click()
    
    # Récupération de la taille de l'écran et clic au centre de l'écran
    largeur_ecran, hauteur_ecran = pyautogui.size()
    x_centre = largeur_ecran // 2
    y_centre = hauteur_ecran // 2
    pyautogui.click(x_centre, y_centre)

    # Recherche du bouton boutons_similaires et clic dessus
    boutons_similaires = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.mat-raised-button.theme-button')))
    boutons_similaires.click()
    
    # Appel de la fonction partie()
    partie()


# Ouvre le site https://agora-quiz.education/Games/List en utilisant le navigateur web contrôlé par Selenium WebDriver
driver.get('https://agora-quiz.education/Games/List')

# Récupère l'URL actuelle de la page
url_actuelle = driver.current_url

# Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site
if url_actuelle == "https://agora-quiz.education/Login":
    connection(idt,motdp)
    
# Affiche "lapin" dans la console
print("lapin")

# Appelle la fonction start_partie avec l'argument idt2 pour commencer une partie
start_partie(idt2)

# Ferme la connexion à la base de données
conn.close()

# Ferme le navigateur web contrôlé par Selenium WebDriver
driver.quit()