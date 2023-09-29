# -------------------------importation des modules-------------------------#
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

# -------------------définition de la classe Database----------------------#

class Database:
    def __init__(self, db) -> None:
        # Initialise la connexion à la db
        self.db = sqlite3.connect(db)
        self.cursor = self.db.cursor()

    def insert(self, question, answer) -> None:
        # Insère une nouvelle question ainsi que sa réponse dans la db
        self.cursor.execute("INSERT INTO questions(question, answer) VALUES (?, ?)", (question, answer))
        self.db.commit()

    def check_entry(self, question) -> int:
        # Vérifie si la question est déjà dans la db
        self.cursor.execute("SELECT * FROM questions WHERE question=?", (question,))
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            return True
        return False

    def get_answer(self, question) -> str:
        # Récupère la réponse à la question dans la db
        self.cursor.execute("SELECT answer FROM questions WHERE question=?", (question,))
        rows = self.cursor.fetchall()
        return rows[0][0]

    def close(self) -> None:
        # Ferme la connexion à la db
        self.db.close()

# -------------------------définition des variables-------------------------#

driver = webdriver.Firefox()
# idt = "unlapinrameur"
# motdp = ";leslapins"

# idt2="QuantumScribe"
# motdp2=";AgoraBot0"


idt = "QuantumScribe"
motdp = ";AgoraBot0"

idt2 = "hallaine"
motdp2 = ";AgoraBot0"

db = Database('QR.db')

# -------------------------définition des fonctions-------------------------#

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

def phase():
    element_question = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.question-content b')))
    soup = BeautifulSoup(element_question.get_attribute('outerHTML'), 'html.parser')
    texte_question = soup.get_text()
    # reponse = obtenir_reponse(texte_question)
    reponse = None
    if reponse:
        print("Réponse :", reponse)
        expression_xpath = f'//button[contains(text(), "{reponse}")]'
        bouton_reponse = driver.find_element(By.XPATH, expression_xpath)
        bouton_reponse.click()
    else:

        boutons = driver.find_elements(By.XPATH,
                                       '//button[contains(@class, "mat-raised-button") and contains(@class, "comic-serif-font")]')

        # Si au moins un bouton est trouvé
        if boutons:
            # Choisir un bouton au hasard parmi les quatre
            bouton_choisi = random.choice(boutons)

            # Attendre que tous les boutons soient cliquables

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class, "mat-raised-button") and contains(@class, "comic-serif-font")]')))

            # Cliquez sur le bouton choisi
            bouton_choisi.click()

        else:
            print("Aucun bouton trouvé")


def partie():
    try:
        print("on est la")
        bouton_versus = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main-container')))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'main-container')))
        bouton_versus.click()
        driver.execute_script('document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2).click();')
        print("ca passe")
    finally:

        boutons_similaires = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-raised-button.theme-button')))
        boutons_similaires.click()
        for i in range(3):
            phase()
            time.sleep(4)
        # apprantisage()
        try:
            bouton_fermer = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Fermer")]')))
            if bouton_fermer:
                bouton_fermer.click()
        finally:
            bouton_suivant = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Suivant")]')))
            bouton_suivant.click()
            try:
                bouton_retour = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Retour aux Parties en cours")]')))
                if bouton_retour:
                    bouton_retour.click()
                print("partie fini a l'autre")
            except:
                try:
                    bouton_manche = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//button[contains(.," Manche Suivante ")]')))
                    if bouton_manche:
                        bouton_manche.click()
                        partie()
                except:

                    print("erreur")
                
            finally:
                print("fin partie")
                return


# Définition de la fonction connection avec deux arguments idt et motdp

def connection(idt, motdp):
    # Recherche de l'élément identifiant et envoi de la valeur de idt
    identifiant = driver.find_element(By.ID, "mat-input-0")
    identifiant.send_keys(idt)

    # Recherche de l'élément mdp et envoi de la valeur de motdp
    mdp = driver.find_element(By.ID, "mat-input-1")
    mdp.send_keys(motdp)

    # Recherche du bouton_connexion et clic dessus
    bouton_connexion = driver.find_element(By.CLASS_NAME, "primary-button")
    bouton_connexion.click()
    # Récupère l'URL actuelle de la page

    WebDriverWait(driver, 10).until(EC.title_is("AgoraQuiz - Accueil du groupe"))
    url_actuelle = driver.current_url
    print(url_actuelle)
    # Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site
    if url_actuelle == "https://agora-quiz.education/HomeGroupe":

        # Recherche du bouton_jouer et clic dessus après qu'il soit visible
        bouton_jouer = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Jouer des Parties")]')))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Jouer des Parties")]')))
        bouton_jouer.click()
        return True
    else:
        print("erreur connection")
        return False


# Définition de la fonction start_partie avec un argument idt2
def start_partie(idt2):
    # Recherche de l'élément input_adversaire et envoi de la valeur de idt2
    input_adversaire = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-3")))
    input_adversaire.send_keys(idt2)

    # Recherche du bouton_inviter et clic dessus
    bouton_inviter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Inviter")]')))
    bouton_inviter.click()
    url_actuelle = driver.current_url
    if url_actuelle != "https://agora-quiz.education/Games/List" and url_actuelle != "https://agora-quiz.education/HomeGroupe":
        partie()
    else:
        bouton_duel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(.,"' + idt2 + '")]')))
        bouton_duel.click()

        url_actuelle = driver.current_url
        if url_actuelle != "https://agora-quiz.education/Games/List":
            # passage debut duel ou on voit les tete

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
    bool = connection(idt, motdp)

# Affiche "lapin" dans la console
print("lapin")

# Appelle la fonction start_partie avec l'argument idt2 pour commencer une partie
if bool == True:
    start_partie(idt2)
print("fin")
time.sleep(3)
# Ferme la connexion à la base de données
db.close()

# Ferme le navigateur web contrôlé par Selenium WebDriver
driver.quit()
