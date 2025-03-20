## Sommaire
- [Contenu](#contenu) Expliquer ce qu'est le projet ainsi que ses fonctionnalités
- [Objectif](#objectif) Expliquer le but de ce projet
- [Groupe](#groupe) Les membres du groupe 
- [Fichiers](#fichiers) Quels sont les fichiers et leurs fonctions
- [Compiler](#compiler) Comment compiler le projet
- [Prérequis](#prérequis) Les bibliothèques à installer 
- [Utilisation_de_l'application](#utilisation_de_l'application) Comment utiliser l'application
- [Sources](#sources) Les ressources sur lesquelles nous nous sommes basées


## Contenu

## Objectif

## Groupe

Notre groupe est d'Orianne COURTADE, Alban SOUPPAYA, Medhi BOULAICH EL KHADRI et Saïd BELKACEM.

## Fichiers

## Compiler

Pour compiler notre projet vous devez vous placez dans le dossier parent de "DevWebProjet" et lancer la commande :
```
flask run
```

## Prérequis

Vous devez en premier lieu télécharger le dossier DevWebProjet à partir du dépot git, ensuite entrez dans le dossier et créez un environnement virtuel à l'aide des commandes suivantes :
```
python -m venv venv
```
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

## Utilisation_de_l'application

## Sources 

# CY_Tech
![CYTECH](CY_Tech_logo.jpg)
