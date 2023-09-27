#-------------------------importation des modules-------------------------#
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

import sqlite3



#-------------------------définition des variables-------------------------#

driver = webdriver.Firefox()
#idt = "unlapinrameur"
#motdp = ";leslapins"

#idt2="QuantumScribe"
#motdp2=";AgoraBot0"



idt = "QuantumScribe"
motdp = ";AgoraBot0"

idt2="hallaine"
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


class Database:
    def __init__(self, db) -> None:
        self.db = sqlite3.connect(db)
        self.cursor = self.db.cursor()

    def insert(self, question, answer) -> None:
        self.cursor.execute("INSERT INTO questions(question, answer) VALUES (?, ?)", (question, answer))
        self.db.commit()

    def check_entry(self, question) -> int:
        self.cursor.execute("SELECT * FROM questions WHERE question=?", (question,))
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            return True
        return False

    def get_answer(self, question) -> str:
        self.cursor.execute("SELECT answer FROM questions WHERE question=?", (question,))
        rows = self.cursor.fetchall()
        return rows[0][0]

    def close(self) -> None:
        self.db.close()


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
def phase():
    element_question = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.question-content b')))
    soup = BeautifulSoup(element_question.get_attribute('outerHTML'), 'html.parser')
    texte_question = soup.get_text()
    #reponse = obtenir_reponse(texte_question)
    reponse = None
    if reponse:
        print("Réponse :", reponse)
        expression_xpath = f'//button[contains(text(), "{reponse}")]'
        bouton_reponse = driver.find_element(By.XPATH, expression_xpath)
        bouton_reponse.click()
    else:
        largeur_ecran, hauteur_ecran = pyautogui.size()
        x_centre = largeur_ecran // 2
        y_centre = hauteur_ecran // 2
        pyautogui.click(x_centre, y_centre)
        boutons_aleatoires = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.mat-raised-button')))
        time.sleep(2)


        # Choisis un bouton au hasard parmi ceux trouvés
        if boutons_aleatoires:
            bouton_choisi = random.choice(boutons_aleatoires)

            # Clique sur le bouton choisi
            bouton_choisi.click()
            time.sleep(2)
            largeur_ecran, hauteur_ecran = pyautogui.size()
            x_centre = largeur_ecran // 2
            y_centre = hauteur_ecran // 2
            pyautogui.click(x_centre, y_centre)
        else:
            print("Aucun bouton trouvé")


def partie():
    for i in range(3):

        phase()
        time.sleep(4)
    #apprantisage()
    bouton_suivant = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Suivant")]')))
    bouton_suivant.click()
    time.sleep(2)
    bouton_suivant = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Retour aux Parties en cours")]')))
    if bouton_suivant:
        bouton_suivant.click()
    else:
        bouton_suivant = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Manche Suivante")]')))
        if bouton_suivant:
            bouton_suivant.click()
            partie()
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
    # Récupère l'URL actuelle de la page
    url_actuelle = driver.current_url

    # Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site
    if url_actuelle != "https://agora-quiz.education/Login":

    # Recherche du bouton_jouer et clic dessus après qu'il soit visible
        bouton_jouer = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Jouer des Parties")]')))
        bouton_jouer.click()
        return True
    else:
        print("erreur connection")
        return False

    
# Définition de la fonction start_partie avec un argument idt2
def start_partie(idt2):

    # Recherche de l'élément input_adversaire et envoi de la valeur de idt2
    input_adversaire = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "mat-input-3")))
    input_adversaire.send_keys(idt2)
    
    # Recherche du bouton_inviter et clic dessus
    bouton_inviter = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Inviter")]')))
    bouton_inviter.click()
    url_actuelle = driver.current_url
    if url_actuelle != "https://agora-quiz.education/Games/List":
        time.sleep(5)
        largeur_ecran, hauteur_ecran = pyautogui.size()
        x_centre = largeur_ecran // 2
        y_centre = hauteur_ecran // 2
        pyautogui.click(x_centre, y_centre)

        # Recherche du bouton boutons_similaires et clic dessus
        boutons_similaires = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-raised-button.theme-button')))
        boutons_similaires.click()
        partie()
    else:
        bouton_duel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(.,"'+idt2+'")]')))
        bouton_duel.click()

        url_actuelle = driver.current_url
        if url_actuelle != "https://agora-quiz.education/Games/List":
            #passage debut duel ou on voit les tete

            time.sleep(5)
            largeur_ecran, hauteur_ecran = pyautogui.size()
            x_centre = largeur_ecran // 2
            y_centre = hauteur_ecran // 2
            pyautogui.click(x_centre, y_centre)


            boutons_similaires = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-raised-button.theme-button')))
            boutons_similaires.click()
            partie()
        else:
            print("erreur lancement de partie")
    
    # Récupération de la taille de l'écran et clic au centre de l'écran

    
    # Appel de la fonction partie()


    # Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site


# Ouvre le site https://agora-quiz.education/Games/List en utilisant le navigateur web contrôlé par Selenium WebDriver
driver.get('https://agora-quiz.education/Games/List')

# Récupère l'URL actuelle de la page
url_actuelle = driver.current_url

# Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site
if url_actuelle == "https://agora-quiz.education/Login":
    bool=connection(idt,motdp)
    
# Affiche "lapin" dans la console
print("lapin")

# Appelle la fonction start_partie avec l'argument idt2 pour commencer une partie
if bool==True:
    start_partie(idt2)
print("fin")
time.sleep(3)
# Ferme la connexion à la base de données
conn.close()

# Ferme le navigateur web contrôlé par Selenium WebDriver
driver.quit()