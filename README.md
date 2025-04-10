## Sommaire
- [Contenu](#contenu) Expliquer ce qu'est le projet ainsi que ses fonctionnalités
- [Objectif](#objectif) Expliquer le but de ce projet
- [Groupe](#groupe) Les membres du groupe 
- [Fichiers](#fichiers) Quels sont les fichiers et leurs fonctions
- [Compiler](#compiler) Comment compiler le projet
- [Prérequis](#prérequis) Les bibliothèques à installer 


## Contenu

Ce projet consiste à créer une plateforme numérique intelligente qui regroupe divers services et fonctionnalités pour les utilisateurs d'une maison. Cette plateforme contient plusieurs modules qui sont accessibles selon le type d'utilisateur (visiteur, simple, complexe et administateur).   
Le module "Information" conresponds à la page d'accueil quand les utilisateurs ne sont pas connectés (les visiteurs) pour voir les certains objets et quelques informations locales.  
Le module "Visualisation" accessible seulement aux personnes inscrites sur la plateforme et apparetenant à la famille (cette condition est vérifiée par l'administracteur via une validation d'inscription). Ainsi l'utilisateur de type simple a accès au module "Information" mais peut également modifier son profil, recherhcer et consulter des objets et les services.   
Le module "Gestion" est dédier aux utilisateurs de type complexe (qui ont aussi accès aux modules "Information" et "Visualisation"). Ce module est une sorte de tableau de bord avancé dédié à la gestion des objets connectés et des services.  
Le module "Administrateur" est dédié aux utilisateurs du type administrateur, qui ont accès à tous les modules de la plateforme. IL permet de gèrer la plateforme dans son ensemble, y compris les utilisateurs, les objets connectés et les services.


## Objectif

L'objectif est de rendre la maison plus connectée, inclusive et efficace en centralisant des fonctionnalités adaptées aux besoins des différents types d'utilisateurs. Cette plateforme permet de faciliter la vie quotidienne de ses utilisateurs en proposant des outils variés comme la gestion d’accès des objets de la maison, d’informations locales, la consommation énergique et d’eau ainsi que la gestion des pièces.

## Groupe

Notre groupe est composé d'Orianne COURTADE, Alban SOUPPAYA, Medhi BOULAICH EL KHADRI et Saïd BELKACEM.

## Fichiers

    - migrations : contient les migrations pour les changements de base de données
    - static : 
        - scripts : contient les fichiers JavaScript
        - styles : contient les fichiers CSS
    - templates : contient les fichiers HTML
    - __init__.py : constructeur de l'application Flask
    - admin.py : gère les routes du module administrateur
    - auth.py : gère les routes de l'authentification
    - db.sqlite : base de données
    - ItsDangerous.py : fonctions nécessaires à la confirmation de mail et création du token de sécurité
    - main.py : gère les routes de la page principale
    - manage_object.py : gère les routes de la page objet
    - models.py : tables de la base de données

## Compiler
Avant de lancer et compiler le projet vous devez aller dans le dossier "DevWebProjet" est lancer l'environnement virtuel à l'aide des commandes suivantes:
```
.\venv\Scripts\activate
cd ..
flask run
```

## Prérequis

Vous devez en premier lieu télécharger le dossier DevWebProjet à partir du dépot git, ensuite entrez dans le dossier et créez un environnement virtuel à l'aide des commandes suivantes :
```
python -m venv venv
```
 >[!IMPORTANT] 
 >Il faut activer les scripts pour windows  
 
Ensuite vous devez activer l'environnement virtuel:
```
.\venv\Scripts\activate 
```
Afin d'installer toutes les bilbliothèques nécessaires il faut exéctuer sous windows: 
```
pip install -r biblioRequise.txt
```
Une fois toutes les bibliothèques installer, vous devez modifier les variables d'environnement de votre environnement virtuel:
```
[System.Environment]::SetEnvironmentVariable("FLASK_APP", "DevWebProjet", "User")
[System.Environment]::SetEnvironmentVariable("FLASK_DEBUG", "1", "User")

```
Une fois ces commandes exécutées vous devez redémarrer le terminal.


# CY_Tech
![CYTECH](CY_Tech_logo.jpg)
