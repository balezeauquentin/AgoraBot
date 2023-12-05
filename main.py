# -------------------------importation des modules-------------------------#
import time

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
driver.maximize_window()
db = Database('QR.db')
connected_user = ""

# ---- List of users and passwords----#

Bot1 = ("unlapinrameur", "leslapins")
Bot2 = ("QuantumScribe", ";AgoraBot0")
Bot3 = ("LeZinzin", "dingdong")
Bot4 = ("DrKawachima", "domojesuisjaponais")
Leo = ("Leo-A", "L!dXz9F!JSif67b")
Estouan = ("unflanpatissier", "utbm")
Quentin = ("QBalezeau", "TuJxKB8DzuZ99AB")

# -------Choose 2 users to play-------#

player1 = Quentin
player2 = Estouan

 # ------Set variables for users------#

idt = player1[0]
motdp = player1[1]
idt2 = player2[0]
motdp2 = player2[1]


# ------Alternative users----------#
altenative_idt = ("", "hallaine", "Leo-A", "Wikiro", "Nycolas", "SuperTimCraft")


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
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//i[contains(.,"Rédigée par :")]')))
    driver.execute_script('document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2).click();')

    try:
        element_question = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.question-content b')))
        soup = BeautifulSoup(element_question.get_attribute('outerHTML'), 'html.parser')
        texte_question = soup.get_text()
        print("Question :", texte_question)
        reponse = db.check_entry(texte_question)

        if reponse:
            print("Question déjà dans la db")
            bonne_reponse = db.get_answer(texte_question)
            print("Avant modif: "+bonne_reponse)
            #bonne_reponse = bonne_reponse.replace("\\", "\\\\")
            #bonne_reponse = bonne_reponse.replace('"', '\"')
            #bonne_reponse = bonne_reponse.replace("'", "\'")
            print("Après modif: "+bonne_reponse)

            expression_xpath = f'//button[contains(., "{bonne_reponse}")]'
            bouton_reponse = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, expression_xpath)))
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, expression_xpath)))

            if bouton_reponse:
                bouton_reponse.click()
            else:
                print("Je n'ai pas trouvé le bouton")
                boutons = driver.find_element(By.XPATH,
                    '//button[contains(@class, "mat-raised-button") and contains(@class, "comic-serif-font")]')
                # Si au moins un bouton est trouvé
                if boutons:
                    # Attendre que tous les boutons soient cliquables
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                        (By.XPATH,
                        '//button[contains(@class, "mat-raised-button") and contains(@class, "comic-serif-font")]')))

                    # Cliquez sur le bouton choisi
                    boutons.click()

        else:
            boutons = driver.find_element(By.XPATH,
                '//button[contains(@class, "responses-uncheck")]')
            # Si au moins un bouton est trouvé
            if boutons:

                # Attendre que tous les boutons soient cliquables
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class, "responses-uncheck")]')))

                # Cliquez sur le bouton choisi
                boutons.click()
            else:
                print("Aucun bouton trouvé")
        if reponse == False:
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.response-true')))
            reponse_a_rajouter = button.text
            print("Apprentissage:")
            print(texte_question)
            print(reponse_a_rajouter)
            db.insert(texte_question, reponse_a_rajouter)
    except:
        print("Mode QCM de merde")
        bouton_valide = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Valider 0 choix")]')))
        if bouton_valide:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Valider 0 choix")]')))
            bouton_valide.click()


def partie():
    try:
        print("on est la")
        bouton_versus = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//b[contains(text(), "VS")]')))

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//b[contains(text(), "VS")]')))

        bouton_versus.click()

        driver.execute_script('document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2).click();')
        print("ca passe")
    finally:

        boutons_similaires = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-raised-button.theme-button')))

        boutons_similaires.click()
        for i in range(3):
            phase()
        try:
            bouton_fermer = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Fermer")]')))

            if bouton_fermer:
                bouton_fermer.click()

        finally:

            try:
                bouton_suivant = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Suivant")]')))
                bouton_suivant.click()
            finally:

                try:
                    print("j'essaye le bouton retour aux parties en cours")
                    bouton_retour = WebDriverWait(driver, 3).until(
                        EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Retour aux Parties en cours")]')))
                    print("le bouton est visible tkt")
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Retour aux Parties en cours")]')))
                    print("je peux cliquer chef'")
                    if bouton_retour:
                        bouton_retour.click()
                    print("partie fini a l'autre")

                except:
                    try:
                        print("Bon bah j'essaye la manche suivante")
                        bouton_manche = WebDriverWait(driver, 3).until(
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
    global connected_user
    # Recherche de l'élément identifiant et envoi de la valeur de idt
    identifiant = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='username']")
    identifiant.send_keys(idt)

    # Recherche de l'élément mdp et envoi de la valeur de motdp
    mdp = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='password']")
    mdp.send_keys(motdp)

    # Recherche du bouton_connexion et clic dessus
    print("j'essaye de me connecter à " + idt)
    time.sleep(1)
    bouton_connexion = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "primary-button")))
    bouton_connexion.click()
    # Récupère l'URL actuelle de la page
    print("Connected")
    WebDriverWait(driver, 10).until(EC.title_is("AgoraQuiz - Accueil du groupe"))
    url_actuelle = driver.current_url
    print(url_actuelle)
    # Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site
    if url_actuelle == "https://agora-quiz.education/HomeGroupe":
        connected_user = idt
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
def start_partie(idt2, alternative_idt):
    # Recherche de l'élément input_adversaire et envoi de la valeur de idt2
    input_adversaire = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-placeholder="Nom de l\'adversaire"]')))
    input_adversaire.send_keys(idt2)

    # Recherche du bouton_inviter et clic dessus
    bouton_inviter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Inviter")]')))
    bouton_inviter.click()

    url_actuelle = driver.current_url
    print(url_actuelle)

    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,'//mat-error[contains(.,"Vous afrrontez déjà ce joueur")]')))
        caplante = 0
    except:
        caplante = 1

    if caplante:
        partie()
    else:
        uwu = '//button[contains(.,"' + idt2 + '")]'
        bouton_partiedejala = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, uwu)))
        if bouton_partiedejala:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, uwu)))
            bouton_partiedejala.click()
            partie()
        else:
            # reprendre une partie aleatoire
            bouton_reprise = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".succes-div")))
            if bouton_reprise.click():
                bouton_reprise.click()
            else:
                n = 0
                input_adversaire = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "mat-input-3")))
                while driver.current_url == "https://agora-quiz.education/Games/List":
                    input_adversaire.clear()
                    input_adversaire.send_keys(alternative_idt[n])
                    bouton_inviter = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Inviter")]')))
                    bouton_inviter.click()
                    if n == len(alternative_idt):
                        print("tout les utilisateurs sont déjà pris")
                        break
                    n = n + 1
                    time.sleep(1)
                print("erreur lancement de partie")

    # Récupération de la taille de l'écran et clic au centre de l'écran

    # Appel de la fonction partie()

    # Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site


def bot(id, mdp, id2):
    # Récupère l'URL actuelle de la page
    url_actuelle = driver.current_url

    # Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site
    if url_actuelle == "https://agora-quiz.education/Login":
        bool = connection(id, mdp)
    else:
        bool = False
    # Affiche "lapin" dans la console
    print("lapin")

    # Appelle la fonction start_partie avec l'argument idt2 pour commencer une partie
    if bool:
        start_partie(id2, altenative_idt)
    print("fin")


def choose_user():
    global connected_user
    if connected_user == idt:
        bot(idt2, motdp2, idt)
    else:
        bot(idt, motdp, idt2)


# PROGRAMME PRINCIPAL

while (1):
    try:
        driver.get('https://agora-quiz.education/Games/List')
        choose_user()
        bouton_fermer = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.mat-tooltip-trigger.avatar-toggle.main-logo-link')))
        if bouton_fermer:
            bouton_fermer.click()
            bouton_deconnexion = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//a[contains(.,"Déconnexion")]')))
            if bouton_deconnexion:
                bouton_deconnexion.click()
                print("déconnexion")
                choose_user()
            else:
                print("erreur déconnexion")
        else:
            print("erreur déconnexion")
    except:
        print("changement user")

# Ferme le navigateur web contrôlé par Selenium WebDriver
driver.quit()

"""
ANCIENNE SOLUTION POUR BOT 2 (fermeture du navigateur et réouverture)

driver = webdriver.Firefox()

# Ouvre le site https://agora-quiz.education/Games/List en utilisant le navigateur web contrôlé par Selenium WebDriver
driver.get('https://agora-quiz.education/Games/List')

# Récupère l'URL actuelle de la page
url_actuelle = driver.current_url

# Si l'URL actuelle est "https://agora-quiz.education/Login", appelle la fonction connection avec les arguments idt et motdp pour se connecter au site
if url_actuelle == "https://agora-quiz.education/Login":
    bool2 = connection(idt2, motdp2)
else:
    bool2 = False

# Affiche "lapin" dans la console
print("lapin")

# Appelle la fonction start_partie avec l'argument idt2 pour commencer une partie
if bool2:
    start_partie(idt, altenative_idt)
print("fin")

# Ferme le navigateur web contrôlé par Selenium WebDriver
driver.quit()
"""

# Ferme la db
db.close()
