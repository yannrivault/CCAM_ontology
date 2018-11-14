# CCAM_ontology

## Description

Code python pour transformer un fichier excel de la Classification Commune des Actes Médicaux (CCAM) fourni par l'Assurance Maladie en une ontologie en RDF.

---

Python script to transform an excel file of the *Classification Commune des Actes Médicaux* (CCAM) provided by the French Health Insurance into an ontology in RDF.

## Utilisation/Usage :

python ccam2ontology.py fichier="un fichier excel de la CCAM fourni par l'Assurance Maladie"

ou bien

python ccam2ontology.py

(la version 54.10 est alors téléchargée depuis le site https://www.ameli.fr/accueil-de-la-ccam/telechargement/index.php)

---

python ccam2ontology.py fichier="An excel file of the CCAM from the French Health Insurance"

or else

python ccam2ontology.py

(the 54.10 release is then downloaded from https://www.ameli.fr/accueil-de-la-ccam/telechargement/index.php)

## Dépendances/Dependencies :
Ce script nécessite python 2.7, les paquets xlrd, re, urllib, ssl et argparse.

This script requires python 2.7, as well as xlrd, re, urllib and argparse packages.
