# PayByPhone Auto-Parking Checker (Cron Job)

Ce script Python utilise **Selenium** et le **Chrome DevTools Protocol (CDP)** pour automatiser la vérification quotidienne du stationnement via l'application web mobile PayByPhone.

L'objectif principal est de prévenir l'oubli de stationnement en lançant automatiquement la séquence d'activation du mode handicapé chaque jour à une heure fixe (par exemple, 20h00), si le stationnement n'a pas été enregistré.

--- 

## Prérequis

Avant de lancer le script, assurez-vous que les éléments suivants sont installés et configurés :

1. **Python 3.13** : Recommandé d'utiliser un environnement virtuel (`venv`).
    
2. **Google Chrome** : Le bot utilise le navigateur Chrome pour l'automatisation.
    
3. **Dépendances Python** : Installez les packages requis listés dans `requirements.txt`

---

## Structure du Projet

```
PayByPhone/
├── main.py                     #  Point d'entrée et logique de threading
├── paybyphone.py               #  Séquence des actions
├── flutter_utils.py            #  Utilitaire de bas niveau (CDP, WebDriver, etc)
├── Debug.py                    #  Classe de logging personnalisée
├── config.json                 #  Fichier de configuration des comptes
└── coords.js                   #  Script JS pour trouver les coordonnées (x, y)
```

---

## Configuration des Comptes (`config*.json`)

Le script utilise un ou plusieurs fichiers `config*.json` pour gérer les identifiants et les préférences.
Chaque compte doit contenir les champs suivants :

|**Champ**|**Type**|**Description**|
|---|---|---|
|`phone`|`string`|Numéro de téléphone de connexion PayByPhone.|
|`password`|`string`|Mot de passe du compte.|
|`location`|`string`|Code tarif/zone de stationnement (ex: `75008`).|
|`plate`|`string`|Plaque d'immatriculation associée.|
|`use_handicap`|`boolean`|Définit si le mode handicapé doit être activé (`true` ou `false`).|
|`last_start_time`|`number`|**[Token d'État]** Horodatage Unix de la dernière activation réussie. Utilisé par le script pour la vérification de l'oubli. Doit être initialisé à `0`.|

```
{
  "accounts": [
    {
      "phone": "06XXXXXXXX",
      "password": "VOTRE_MOT_DE_PASSE",
      "location": "75008",
      "plate": "FR-XXX",
      "use_handicap": true,
      "last_start_time": 0
    }
  ]
}
```

---

## Logique de Vérification (Système par Token)

Le script utilise une approche basée sur un **token d'état** pour éviter la vérification fragile du Front-end :

1. **Vérification de l'Oubli :** Avant d'ouvrir le navigateur pour un compte, le script vérifie la valeur de `last_start_time` dans le JSON.
    
2. **Seuil Quotidien :** Si `last_start_time` est antérieur à 5h00 du matin aujourd'hui, le stationnement est considéré comme **oublié**.
    
3. **Activation :** Seuls les comptes dont l'état est "oublié" ouvrent le navigateur et lancent la séquence d'activation.
    
4. **Mise à Jour :** Après le succès de l'activation, le `last_start_time` est mis à jour dans le fichier JSON source, empêchant le script de relancer l'activation avant demain matin.

---

## Déploiement (Cron Job)

Le script est conçu pour être lancé par un système de tâches planifiées (Cron ou Planificateur de Tâches Windows).

### Configuration de la Tâche Quotidienne (Windows)

1. **Planificateur de Tâches Windows :** Ouvrez le Planificateur de Tâches.
    
2. **Déclencheur :** Créez un nouveau déclencheur Quotidien à **20:00:00**.
    
3. **Action :** Définissez l'action comme suit :
    
    - **Programme/script :** Chemin complet vers votre interpréteur Python (ex: `C:\chemin\vers\PayByPhone\.venv\Scripts\python.exe`)
        
    - **Ajouter des arguments :** Chemin complet vers `main.py` (ex: `C:\chemin\vers\PayByPhone\main.py`)
        
    - **Démarrer dans :** Chemin du dossier racine du projet (ex: `C:\chemin\vers\PayByPhone`)
        

Ceci garantit que le script sera exécuté tous les jours à 20h00.
