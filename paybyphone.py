import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from Debug import Debug


class PayByPhoneBot:

    def __init__(self):
        self.log = Debug(debug=True, prefix="paybyphone")

        chrome_options = Options()
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        chrome_options.add_argument("--window-size=412,800")


        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        self.wait = WebDriverWait(self.driver, 20)
        self.log.success("WebDriver initialisé.")

    def inject_coords(self):
        try:
            with open("coords.js", "r", encoding="utf8") as f:
                script = f.read()

            self.driver.execute_script(script)
            self.log.debug("coords.js injecté.")
            return True

        except Exception as e:
            self.log.error(f"Erreur injection coords.js : {e}")
            return False


    def perform_flutter_action(self, x, y, wait_time=0.2):
        self.log.info(f"Tentative de clic sur ({x}, {y}) via CDP...")

        if not self.click_cdp(x, y):
            return False
        time.sleep(wait_time)
        self.inject_coords()
        return True

    def input_flutter_field(self, x, y, value, wait_time=0.2):
        self.log.info(f"Tentative de saisie dans le champ ({x}, {y})")

        if not self.click_cdp(x, y):
            return False

        try:
            self.driver.switch_to.active_element.send_keys(value)
            self.log.success(f"Valeur saisie")
            time.sleep(wait_time)
            return True
        except Exception as e:
            self.log.error(f"Échec de la saisie : {e}")
            return False

    def accept_cookies(self):
        try:
            btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Autoriser tous les cookies')]"))
            )
            btn.click()
            self.log.info("Cookies acceptés.")
            time.sleep(1)
        except:
            self.log.debug("Aucune fenêtre cookies détectée.")

    def click_stationner(self):
        try:
            btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Stationner')]"))
            )
            btn.click()
            self.log.info("Bouton 'Stationner' cliqué.")
        except:
            self.log.error("Impossible de cliquer sur 'Stationner'.")
            return False
        return True


    def wait_for_flutter_canvas(self):
        self.log.debug("Attente du chargement du conteneur Flutter ('flt-glass-pane')...")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "flt-glass-pane"))
            )
            self.log.success("Conteneur Flutter détecté.")
            time.sleep(1)
            return True
        except Exception as e:
            self.log.error(f"Erreur: 'flt-glass-pane' non détecté après le délai.")
            return False

    def click_cdp(self, x_abs, y_abs):
        if not self.wait_for_flutter_canvas():
            self.log.error("Échec de la détection du conteneur Flutter. Annulation du clic CDP.")
            return False

        self.log.debug(f"Demande de clic CDP à ({x_abs},{y_abs}).")

        try:
            self.driver.execute_cdp_cmd('Input.dispatchMouseEvent', {
                'type': 'mousePressed',
                'x': x_abs,
                'y': y_abs,
                'button': 'left',
                'clickCount': 1
            })
            time.sleep(0.05)

            self.driver.execute_cdp_cmd('Input.dispatchMouseEvent', {
                'type': 'mouseReleased',
                'x': x_abs,
                'y': y_abs,
                'button': 'left',
                'clickCount': 1
            })

            self.log.success(f"Clic CDP effectué sur ({x_abs},{y_abs}).")
            time.sleep(0.2)
            return True

        except Exception as e:
            self.log.error(f"Erreur clic CDP : {e}")
            return False

    def login(self, phone, password):
        self.log.info("Ouverture de PayByPhone...")

        self.driver.get("https://www.paybyphone.fr/")
        time.sleep(0.5)

        self.inject_coords()
        self.accept_cookies()
        if not self.click_stationner():
            return False

        self.accept_cookies()
        self.inject_coords()

        IGNOR_BUTTON_X      =   134
        IGNOR_BUTTON_Y      =   606
        COUNTRY_BUTTON_X    =    78
        COUNTRY_BUTTON_Y    =   271
        CONNECT_X           =   247
        CONNECT_Y           =   395
        PHONE_FIELD_X       =   161
        PHONE_FIELD_Y       =   129
        MDP_FIELD_X         =   166
        MDP_FIELD_Y         =   215
        VALID_FORM_X        =   247
        VALID_FORM_Y        =   606


        # 1. Clic ignorer
        if not self.perform_flutter_action( IGNOR_BUTTON_X,  IGNOR_BUTTON_Y):
            return False

        # 2. Clic sur le bouton Pays
        if not self.perform_flutter_action(COUNTRY_BUTTON_X, COUNTRY_BUTTON_Y,):
            return False

        # 3. Clic sur le bouton de Connexion
        if not self.perform_flutter_action(
                CONNECT_X, CONNECT_Y):
            return False

        # 4. Saisie du numéro de téléphone
        if not self.input_flutter_field(
                PHONE_FIELD_X, PHONE_FIELD_Y,phone):
            return False

        # 5. Saisie du mot de passe
        if not self.input_flutter_field(MDP_FIELD_X, MDP_FIELD_Y, password):
            return False

        # 6. Se connecter
        if not self.perform_flutter_action(VALID_FORM_X, VALID_FORM_Y):
            return False
        self.log.success("EEEEEENFIN !!")
        return True


    def check_parking(self, plate):
       pass

    def close(self):
        self.log.info("Fermeture du WebDriver.")
        self.driver.quit()