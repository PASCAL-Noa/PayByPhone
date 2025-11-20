import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class FlutterUtils:
    """
    Contient les méthodes utilitaires pour interagir
    avec les applications Web rendues par Flutter (via Canvas/CDP).
    """

    def __init__(self):
        self.driver = None
        self.log = None

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


    def perform_flutter_action(self, x, y, wait_time=1):
        self.log.info(f"Tentative de clic sur ({x}, {y}) via CDP...")

        if not self.click_cdp(x, y):
            return False
        time.sleep(wait_time)
        self.inject_coords()
        return True


    def input_flutter_field(self, x, y, value, wait_time=1):
        self.log.info(f"Tentative de saisie dans le champ ({x}, {y})")

        if not self.click_cdp(x, y):
            return False

        try:
            self.driver.switch_to.active_element.send_keys(value)
            self.log.success("Valeur saisie")
            time.sleep(wait_time)
            return True
        except Exception as e:
            self.log.error(f"Échec de la saisie : {e}")
            return False

    def wait_for_flutter_canvas(self):
        self.log.debug("Attente du chargement du conteneur Flutter ('flt-glass-pane')...")
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "flt-glass-pane")))
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
            # MOUSE_DOWN
            self.driver.execute_cdp_cmd('Input.dispatchMouseEvent', {
                'type': 'mousePressed',
                'x': x_abs,
                'y': y_abs,
                'button': 'left',
                'clickCount': 1
            })
            time.sleep(0.05)

            # MOUSE_UP
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