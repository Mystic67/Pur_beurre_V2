from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # on utilise l'adaptateur postgresql
        'NAME': 'pur_beurre',  # le nom de notre base de donnees creee precedemment
        'USER': '',  # Remplacez par le nom d'utilisateur utilisé lors de l'installation du serveur
        'PASSWORD': '', # Entrer le mot de passe de configuration de votre serveur
        'HOST': '', # Entrer l'addresse de votre serveur s'il n'est pas en local
        'PORT': '5432',
    }
}
