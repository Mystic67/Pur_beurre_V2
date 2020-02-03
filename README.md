# Project 11 (Pur beurre V2)
L' application Pur beurre V2 est une amélioration du projet "pur beurre" (projet 8), pour un déploiement sur un serveur dédié ou nutualisé.
Le version 2 de "Pur beurre", ajoute la possibilité, pour l'utilisateur, de réinitialiser sont mot de passe en cas d'oubli et de modifier son mot de passe une fois connecté à son compte.

## **I. Présentation**
Pur beurre est un application web qui permet d'effectuer une recherche des aliments et de trouver un produit de substitutions 
plus sain, que l'utilisateur peut ensuite enregister dans ses aliments de substitutions favoris après avoir créé un compte 
et s'être authentifié.
Cette application est en Python/Django et utilise les bases de données d'Openfoodfacts.

<div align="center">
     <img src="/store/static/store/img/Screenshot.png">
</div>

**Fonctionnalités générales:**
- Sur la page d'accueil, l'utilisateur accède à un moteur de recherche qui va lui permettre d'effectuer une recherche sur un aliment de son choix.
  
  Il a également la posibilité de créer immédiatement un compte, lui permettant d'accéder à l'ensemble des fonctionnalité 
  de l'application (Sauvegader des substituts dans ses favoris, visualiser ses enregistements et modifier les données de son compte). 
- Après avoir lancé la recherche, une page affiche les aliments trouvés en fonction de la requête. L'utilisateur a la possiblité de voir 
  le détail d'un aliment en cliquant sur '+' ou de rechercher un aliment de substitution en cliquant sur la loupe.
  
- Après avoir effectué une recherche de substituts, la page des resultats s'affiche. Si l'utilisateur est authentifié, il peux alors 
  enregister un aliment dans ses favoris qui peux consulter en cliquant sur la carotte en haut à droite.
  
  Il peut également voir le détail d'un produit de substitution en cliquant sur '+'.
  
**Le système d'authentification:**

- L'utilisateur peut créer un compte par un clique sur l'icone situé en haut à droite.
- La page l'invite à s'authenfier par son adresse mail et son mot de passe si un compte à déjà été créé. Après validation du formulaire,
  l'utilisateur est rediriger vers la page d'accueil pour y saisir sa recherche. Les menus 'Favoris' et 'se déconnecté' son désormais affiché en haut à droite.
   
  Dans le cas ou l'utilisateur n'a pas encore créer de compte, il peut accéder à la page de création de compte en cliquant sur le lien
   "Je me connecte à un compte existant" au bas du formulaire.
- Sur la page d'authentification, l'utilisateur est invité à entrer ses données personnel par le biais du formulaire.
  Seules les données "adresse e-mail" et "mot de passe' sont necessaires, les autres données sont faculatifs.
  
  Après validation du formulaire, l'utilisateur est automatiquement authentifié et rediriger vers la page d'accueil pour y effectuer sa recherche.
  
  
**NB:** L'utilisateur peut effectuer une recherche à partir de n'importe quelle page par le biais du champs de recherche situé en haut de chaque page.
        Il suffit d'entrer la requête et appuyer sur la touche "Entrer" de son clavier.
 
  
## **II. Installation**

**Prérequis:**
1) Télécharger et installé le serveur de base de donnée PostgreSQL:  
   Voir la page:  <https://www.postgresql.org/download/>
2) Télécharger et installer Python3:  
    Voir le page: <https://www.python.org/downloads/>
3) installer pip dans votre terminal. (mode console):   
   Voir la page: <https://pip.pypa.io/en/stable/installing/>

**Installation du repository et de l'environement:**
1) Ouvrir votre therminal préféré et créer un répertoire pour le projet.  
   ex: `>>> mkdir mon_repertoire`
2) Installer un environement vituel (pipenv dans notre exemple)  
   ex: `>>> pip install pipenv`     
2) Cloner ou télécharger le repository Git du projet dans le répertoire que vous venez de créer. 
3) Aller dans le repertoire racine du projet.  
    ex: `ex: cd /Pur_beurre_V2`
4) Créer et démarrer votre environement virtuel pipenv:  
    ex: `>>> pipenv shell`
    NB: En tapant la commande 'ls' le fichier requirement.txt doit être visible.
5) Installer les requirements  
    `>>> pip install -r requirement.txt`  
6) Votre environement est créé, il vous reste à installer les bases de données (voir la suite)

#### **Configuration des données de développement:**
1) Configurer les settings:  
    a) Ouvrir le fichier '\_\_init\_\_.py', avec votre éditeur préféré qui se trouve à le racine de l'application du projet:  
        **/pur_beurre_V2_app/settings/\_\_init\_\_.py**  
        (donc dans le répertoire: **/votre_repertoire/Pur_beurre_V2/pur_beurre_V2_app/settings/\_\_init\_\_.py**)  
    b) Modifier la configuration pour l'accès à votre base de données:  
        Dans la section DATABASES:  
    >        DATABASES = {  
    >          'default': {  
    >                'ENGINE': 'django.db.backends.postgresql',   <-- Ne pas modifier
    >                'NAME': 'pur_beurre',   <-- Ne pas modifier sauf si vous souhaiter un autre nom pour votre base de donnée.
    >                'USER': 'votre_nom_d'utilisateur',   <-- Remplacez par le nom d'utilisateur que vous avez utilisé lors de l'installation du serveur PostgreSQL
    >                'PASSWORD': '',   <-- Entrer le mot de passe de configuration de votre serveur
    >                'HOST': '',   <-- Entrer l'addresse de votre serveur s'il n'est pas en local
    >                'PORT': '5432',   <-- Ne pas modifier, sauf si vous avez changer le port par défaut de votre serveur PostgreSQL
    >            }
    >         }

2) Créer la base de donnée, les tables et peupler (remplir) les tables:  
    Retourner dans votre environement virtuel activé (à la racine de l'application '/mon_repertoire/pur_beurre' et entrer les commandes suivantes;   
    a) Créer la base de donnée:  
       `>>> createdb -O votre_nom_utilisateur pur_beurre`   <-- Non d'utilisateur et nom de la base de donnée défini dans settings.py   
    b) Créer les tables:  
       `>>> python manage.py migrate` ou le racourci `>>> ./manage.py migrate`
    c) Peupler les tables avec les données d'openfoodfacts:
       `>>> python manage.py update_db` ou le racourci `>>> ./manage.py update_db`
       
#### **Démarrer le serveur de développement:**  
  -   Toujours dans la console:  
        `>>> python manage.py runserver`
    
   **NB:** Ne pas démarrer le serveur de développement sur le serveur de production.
   
Vous pouvez vous rendre à l'adresse local indiquée dans le terminal avec votre navigateur web préféré.  
Ex: http://127.0.0.1:800 ou http://localhost:8000

### **Configuration des données de production:**
Pour des raisons de sécurité le fichier "production.py" doit être créé directement sur le serveur et ne doit pas être versionné sur Github.
1) Créer un fichier "production.py" dans le répertoire  "/Pur_beurre_V2/pur_beurre_V2_app/settings/" directement sur le serveur:
2) Editer le fichier "production.py" (/Pur_beurre_V2/pur_beurre_V2_app/settings/production.py), copier/coller les informations ci-dessous et adapter les informations avec les données de votre serveur:

#### **production.py**

    > from . import *
    > SECRET_KEY = 'Votre clé d'application' # <- A remplaver par votre clé d'application  
    > DEBUG = False  
    > ALLOWED_HOSTS = ['www.exemple.com', 'localhost'] # <- A remplacer par votre nom de domaine et/ou adresse ip d'accès

    > DATABASES = {
    >     'default': {
    >         'ENGINE': 'django.db.backends.postgresql',  # on utilise l'adaptateur postgresql
    >         'NAME': 'pur_beurre',  # le nom de votre base de données.
    >         'USER': 'votre_nom_d'utilisateur',  # attention : remplacez par votre nom d'utilisateur !!
    >         'PASSWORD': 'votre_mot_de_passe', # remplacez par votre mot de passe d'accès à la base de données !!
    >         'HOST': '',
    >         'PORT': '5432',
    >     }
    > }

    > EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    > EMAIL_HOST = 'mail.exemple.com'  # A rempacer par le nom d'hôte qui envoi les mail
    > EMAIL_PORT = 25  # A remplacer par le port du serveur mail (25, 465 ou 587) 
    > EMAIL_USE_TLS = False  # mettre à "True" pour l'activation du Protocol TLS
    > EMAIL_HOST_USER = 'exemple@mon_domaine.com'  # Nom d’utilisateur à utiliser pour le serveur SMTP
    > EMAIL_HOST_PASSWORD = 'mot_de_passe'  # Remplacer par le mot de passe du serveur SMTP
    > DEFAULT_FROM_EMAIL = 'exemple@mon_domaine.com'  # Remplacer par l'adresse mail d'envoi par défaut
    > SERVER_EMAIL = 'exemple@mon_domaine.com'  # Remplacer par le serveur mail d'envoi

   


   
   
    
    
       
       
     
    


