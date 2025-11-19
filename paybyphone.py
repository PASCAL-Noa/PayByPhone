import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from Debug import Debug
from flutter_utils import FlutterUtils

class PayByPhoneBot(FlutterUtils):

    def __init__(self):
        self.log = Debug(debug=True, prefix="paybyphone")

        chrome_options = Options()
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        chrome_options.add_argument("--window-size=412,900")
        chrome_options.add_argument("--disable-application-cache")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        self.wait = WebDriverWait(self.driver, 20)
        self.log.success("WebDriver initialisé.")


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
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Stationner')]")))
            btn.click()
            self.log.info("Bouton 'Stationner' cliqué.")
        except:
            self.log.error("Impossible de cliquer sur 'Stationner'.")
            return False
        return True

    def login(self, phone, password):
        self.log.info("Ouverture de PayByPhone...")

        self.driver.get("https://www.paybyphone.fr/")
        time.sleep(0.5)

        self.inject_coords()
        self.accept_cookies()
        if not self.click_stationner():
            return False

        self.inject_coords()
        self.accept_cookies()

        IGNOR_BUTTON_X      =   134
        IGNOR_BUTTON_Y      =   706
        COUNTRY_BUTTON_X    =    78
        COUNTRY_BUTTON_Y    =   271
        CONNECT_X           =   252
        CONNECT_Y           =   573
        PHONE_FIELD_X       =   161
        PHONE_FIELD_Y       =   138
        MDP_FIELD_X         =   166
        MDP_FIELD_Y         =   223
        VALID_FORM_X        =   258
        VALID_FORM_Y        =   705

        if not self.perform_flutter_action( IGNOR_BUTTON_X,  IGNOR_BUTTON_Y):
            return False
        if not self.perform_flutter_action(COUNTRY_BUTTON_X, COUNTRY_BUTTON_Y,):
            return False
        if not self.perform_flutter_action(CONNECT_X, CONNECT_Y):
            return False
        if not self.input_flutter_field(PHONE_FIELD_X, PHONE_FIELD_Y,phone):
            return False
        if not self.input_flutter_field(MDP_FIELD_X, MDP_FIELD_Y, password):
            return False
        if not self.perform_flutter_action(VALID_FORM_X, VALID_FORM_Y):
            return False
        self.log.success("EEEEEENFIN !!")
        time.sleep(2)
        return True


    def activate_handicap_sequence(self, location):
        self.search_tarif(location)
        self.set_handicap_and_time()

    def search_tarif(self, location):
        SEARCH_FIELD_X  = 193
        SEARCH_FIELD_Y  = 101
        SEARCH_X        = 244
        SEARCH_Y        = 705
        SELECT_X        = 198
        SELECT_Y        = 150
        CAR_X           = 222
        CAR_Y           = 550

        if not self.perform_flutter_action(SEARCH_FIELD_X, SEARCH_FIELD_Y):
            return False
        if not self.input_flutter_field(SEARCH_FIELD_X, SEARCH_FIELD_Y, location):
            return False
        if not self.perform_flutter_action(SEARCH_X, SEARCH_Y):
            return False
        if not self.perform_flutter_action(SELECT_X, SELECT_Y):
            return False
        if not self.perform_flutter_action(CAR_X, CAR_Y):
            return False

        time.sleep(2)
        return True

    def set_handicap_and_time(self):
        STEP1_X = 184
        STEP1_Y = 503
        STEP2_X = 190
        STEP2_Y = 689
        STEP3_X = 230
        STEP3_Y = 625
        STEP4_X = 413
        STEP4_Y = 614
        STEP5_X = 246
        STEP5_Y = 683
        STEP6_X = 258
        STEP6_Y = 692
        STEP7_X = 254
        STEP7_Y = 730
        STEP8_X = 249
        STEP8_Y = 703

        if not self.perform_flutter_action(STEP1_X, STEP1_Y):
            return False
        if not self.perform_flutter_action(STEP2_X, STEP2_Y):
            return False
        if not self.input_flutter_field(STEP3_X, STEP3_Y, 1):
            return False
        if not self.perform_flutter_action(STEP4_X, STEP4_Y):
            return False
        if not self.perform_flutter_action(STEP5_X, STEP5_Y):
            return False
        if not self.perform_flutter_action(STEP6_X, STEP6_Y):
            return False
        if not self.perform_flutter_action(STEP7_X, STEP7_Y):
            return False
        if not self.perform_flutter_action(STEP8_X, STEP8_Y):
            return False

        time.sleep(2)
        return True


    def close(self):
        self.log.info("Fermeture du WebDriver.")
        self.driver.quit()