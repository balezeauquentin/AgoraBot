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


def phase(driver, db):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//i[contains(.,"Rédigée par :")]')))
    driver.execute_script('document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2).click();')
    element_question = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.question-content b')))
    soup = BeautifulSoup(element_question.get_attribute('outerHTML'), 'html.parser')
    texte_question = soup.get_text()
    print("Question :", texte_question)
    reponse = db.check_entry(texte_question)

    if reponse:
        print("je l'ai")
        print("Réponse :", reponse)
        bonne_reponse = db.get_answer(texte_question)
        bonne_reponse = bonne_reponse.replace('"', '\"')
        expression_xpath = f'//button[contains(., "{bonne_reponse}")]'

        bouton_reponse = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, expression_xpath)))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH,
             expression_xpath)))

        if bouton_reponse:
            bouton_reponse.click()
        else:
            boutons = driver.find_element(By.XPATH,
                                          '//button[contains(@class, "mat-raised-button") and contains(@class, "comic-serif-font")]')
            # Si au moins un bouton est trouvé
            if boutons:
                # Attendre que tous les boutons soient cliquables
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH,
                     '//button[contains(@class, "mat-raised-button") and contains(@class, "comic-serif-font")]')))

                # Cliquez sur le bouton choisi
                boutons.click()

    else:
        boutons = driver.find_element(By.XPATH,
                                      '//button[contains(@class, "mat-raised-button") and contains(@class, "comic-serif-font")]')
        # Si au moins un bouton est trouvé
        if boutons:

            # Attendre que tous les boutons soient cliquables
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class, "mat-raised-button") and contains(@class, "comic-serif-font")]')))

            # Cliquez sur le bouton choisi
            boutons.click()
        else:
            print("Aucun bouton trouvé")
    if reponse == False:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.response-true')))
        reponse_a_rajouter = button.text
        print("Apprentissage:")
        print(texte_question)
        print(reponse_a_rajouter)
        db.insert(texte_question, reponse_a_rajouter)


def partie(driver, db):
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

        boutons_similaires = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-raised-button.theme-button')))

        boutons_similaires.click()
        for i in range(3):
            phase(driver, db)
        try:
            bouton_fermer = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//button[contains(.,"Fermer")]')))

            if bouton_fermer:
                bouton_fermer.click()

        finally:
            bouton_suivant = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Suivant")]')))
            bouton_suivant.click()

            try:
                bouton_retour = WebDriverWait(driver, 5).until(
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
                        partie(driver, db)

                except:
                    print("erreur")

            finally:
                print("fin partie")
                return


def start_partie(idt2, alternative_idt, driver, db):
    # Recherche de l'élément input_adversaire et envoi de la valeur de idt2
    input_adversaire = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-placeholder="Nom de l\'adversaire"]')))
    input_adversaire.send_keys(idt2)

    # Recherche du bouton_inviter et clic dessus
    bouton_inviter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Inviter")]')))
    bouton_inviter.click()

    url_actuelle = driver.current_url
    if url_actuelle != "https://agora-quiz.education/Games/List" and url_actuelle != "https://agora-quiz.education/HomeGroupe":
        partie(driver, db)
    else:
        uwu = '//button[contains(.,"' + idt2 + '")]'
        bouton_partiedejala = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, uwu)))
        if bouton_partiedejala:
            uwu = '//button[contains(.,"' + idt2 + '")]'
            bouton_inviter = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, uwu)))
            bouton_partiedejala.click()
            partie(driver, db)
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


def connection(idt, motdp, driver):
    global connected_user
    # Recherche de l'élément identifiant et envoi de la valeur de idt
    identifiant = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='username']")
    identifiant.send_keys(idt)

    # Recherche de l'élément mdp et envoi de la valeur de motdp
    mdp = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='password']")
    mdp.send_keys(motdp)

    # Recherche du bouton_connexion et clic dessus
    print("j'essaye de me connecter")
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


def deconnection(driver):
    bouton_fermer = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.mat-tooltip-trigger.avatar-toggle.main-logo-link')))
    if bouton_fermer:
        bouton_fermer.click()
        bouton_deconnexion = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//a[contains(.,"Déconnexion")]')))
        if bouton_deconnexion:
            bouton_deconnexion.click()
            print("déconnexion")

        else:
            print("erreur déconnexion")
    else:
        print("erreur déconnexion")


def principal(idt1, idt2, mdp1, mdp2, alternative):
    db = Database('QR.db')
    print("hello world 1")
    driver = webdriver.Firefox()
    driver.get('https://agora-quiz.education/Games/List')
    connection(idt1, mdp1, driver)
    start_partie(idt2, alternative, driver, db)
    deconnection(driver)
    print("hello world 2")
    connection(idt2, mdp2, driver)
    start_partie(idt1, alternative, driver, db)
    deconnection(driver)
    db.close()


# --------------BOT 1--------------#
idt1 = "unlapinrameur"
motdp1 = "leslapins"

# --------------BOT 2--------------#
idt2 = "QuantumScribe"
motdp2 = ";AgoraBot0"

# --------------BOT 3--------------#
idt3 = "unchat"
motdp3 = "deuxchat"

# --------------BOT 4--------------#
idt4 = "unchien"
motdp4 = "deuxchien"

# ------Alternative users----------#
altenative_idt = ("QBalezeau", "hallaine", "Leo-A", "Wikiro", "Nycolas", "SuperTimCraft")

bot1 = threading.Thread(target=principal, args=(idt1, idt2, motdp1, motdp2, altenative_idt))
bot2 = threading.Thread(target=principal, args=(idt3, idt4, motdp3, motdp4, altenative_idt))
bot1.start()
bot2.start()
bot1.join()
bot2.join()
print("fin thread")

# driver = webdriver.Firefox()
# driver.get('https://agora-quiz.education/Games/List')
# element = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='username']")
# element.send_keys("lapin")
# driver.quit()
