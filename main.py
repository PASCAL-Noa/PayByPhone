import json
import sys
from pathlib import Path
from paybyphone import PayByPhoneBot
from Debug import Debug
import time


log = Debug(debug=False, prefix="main")


def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        log.error(f"Erreur de lecture config.json: {e}")
        sys.exit(1)
    except FileNotFoundError:
        raise
    return cfg


def main():
    config_path = Path("config.json")
    if not config_path.exists():
        log.error("Erreur: config.json introuvable")
        log.info("Créez un fichier config.json avec vos identifiants")
        sys.exit(1)

    cfg = load_config(config_path)
    if not cfg.get("accounts"):
        log.warning("Aucun compte trouvé dans config.json")
        sys.exit(1)

    log.info(f"Démarrage - {len(cfg['accounts'])} compte(s) à vérifier\n")

    for i, acc in enumerate(cfg["accounts"], 1):

        log.info(f"Compte {i}/{len(cfg['accounts'])} - {acc['plate']}")

        bot = None
        try:
            bot = PayByPhoneBot()
            log.info(f"Connexion avec {acc['phone']}...")

            success = bot.login(acc["phone"], acc["password"])
            if not success:
                log.error("Échec de connexion")
                continue

            log.info(f"Vérification du stationnement pour {acc['plate']}...")


            if acc.get("use_handicap", False):
                log.info(f"Tentative d'activation mode handicapé...")
                bot.activate_handicap_sequence(acc["location"])
            else:
                log.info("Mode handicapé désactivé dans la config")

        except KeyboardInterrupt:
            log.info("\nInterrompu par l'utilisateur")
            break
        except Exception as e:
            log.critical(f"Erreur non gérée pour {acc.get('plate', 'N/A')}: {e}")
        finally:
            if bot:
                try:
                    if success:
                        time.sleep(2)
                    bot.close()
                    log.info("Navigateur fermé")
                except:
                    pass

    log.success("Vérification terminée")


if __name__ == "__main__":
    main()