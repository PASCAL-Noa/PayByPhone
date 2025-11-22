import json
import sys
import threading
from pathlib import Path
import time
import datetime

from paybyphone import PayByPhoneBot
from Debug import Debug

log = Debug(debug=True, prefix="main")


def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        return cfg.get("accounts", [])
    except json.JSONDecodeError as e:
        log.error(f"Erreur de lecture {config_path}: {e}")
        return []
    except FileNotFoundError:
        log.error(f"Erreur: Fichier {config_path} introuvable.")
        return []


def process_account(account_data, index, total_accounts):
    acc = account_data

    log.info(f"\n{'=' * 60}")
    log.info(f"THREAD {index}/{total_accounts} - Compte {acc['plate']}")
    log.info(f"{'=' * 60}")

    LAST_TIME = acc.get("last_start_time", 0)

    if LAST_TIME:
        last_start_datetime = datetime.datetime.fromtimestamp(LAST_TIME)
        today = datetime.date.today()
        start_of_day = datetime.datetime.combine(today, datetime.time(5, 0))

        if last_start_datetime > start_of_day:
            log.success(
                f"THREAD {index}: Parking déjà activé aujourd'hui ({last_start_datetime.strftime('%H:%M')}). IGNORÉ.")
            return
        else:
            log.warning(f"THREAD {index}: Ancien token détecté. Activation nécessaire.")
    else:
        log.warning(f"THREAD {index}: Aucun token trouvé. Activation nécessaire.")

    bot = None
    success = False

    try:
        bot = PayByPhoneBot()
        log.info(f"THREAD {index}: Connexion...")

        success = bot.login(acc["phone"], acc["password"])
        if not success:
            log.error(f"THREAD {index}: Échec de connexion")
            return

        if acc.get("use_handicap", False):
            log.info(f"THREAD {index}: Tentative d'activation mode handicapé...")

            if bot.activate_handicap_sequence(acc["location"], acc.get("use_handicap", False)):
                current_timestamp = int(time.time())
                bot.update_parking_time(acc["phone"], acc['config_file'], current_timestamp)
        else:
            log.info(f"THREAD {index}: Mode handicapé désactivé dans la config.")

    except Exception as e:
        log.critical(f"THREAD {index}: Erreur non gérée pour {acc.get('plate', 'N/A')}: {e}")

    finally:
        if bot:
            try:
                if success:
                    time.sleep(2)
                bot.close()
                log.info(f"THREAD {index}: Navigateur fermé")
            except:
                pass


def main():
    config_files = ["config.json", "config1.json", "config2.json"]
    all_accounts = []

    initial_load_success = True

    for file_name in config_files:
        config_path = Path(file_name)

        if config_path.exists():
            accounts = load_config(config_path)
            if accounts:
                for acc in accounts:
                    acc['config_file'] = file_name
                all_accounts.extend(accounts)
                log.info(f"Chargement réussi : {len(accounts)} compte(s) trouvés dans {file_name}.")
            else:
                log.warning(f"Le fichier {file_name} existe mais ne contient aucun compte valide.")
        else:
            log.error(f"Fichier manquant : {file_name}. Veuillez le créer.")
            initial_load_success = False

    if not initial_load_success and not all_accounts:
        sys.exit(1)

    if not all_accounts:
        log.warning("Aucun compte valide trouvé pour le démarrage.")
        sys.exit(1)

    accounts = all_accounts
    log.info(f"Démarrage de {len(accounts)} compte(s) en parallèle.")

    threads = []

    try:
        for i, acc in enumerate(accounts, 1):
            thread = threading.Thread(target=process_account, args=(acc, i, len(accounts)))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        log.warning("Interruption manuelle. Arrêt des processus...")

    log.success("Vérification multi-comptes terminée.")

if __name__ == "__main__":
    main()