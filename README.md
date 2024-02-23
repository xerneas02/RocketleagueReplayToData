# Rocket League Replay Data Collection and Processing

## Introduction
This repository contains scripts to download Rocket League replays from [Ballchasing.com](https://ballchasing.com) and process them for use in training a bot.

## DownloadReplay.py
This script is used to search for and download replays from Ballchasing.com. By default, it downloads 1v1 replays between Platinum 1 and Diamond 1 players from Season 7 of the free-to-play version of Rocket League. It will download a maximum of 200 replays. You'll need an API token, which can be obtained from Ballchasing.com/upload.

## rocketReplay.py
This script is responsible for decompiling the downloaded replays. It decompiles them into a DataFrame and JSON format using the Carball library. There's also a function to obtain data with mirrored player and ball positions, along with constants corresponding to the Octane and Fennec body IDs.

## RemoveKickoff.py
This script takes the data retrieved by rocketReplay and removes frames between a goal and the start of the next kickoff to eliminate unnecessary data for bot training, which could introduce noise.

## How to Use
1. **Obtain API Token:** Go to Ballchasing.com/upload and obtain your API token.
2. **Download Replays:** Run `DownloadReplay.py` with your API token to download replays.
3. **Decompile Replays:** Run `rocketReplay.py` to decompile the downloaded replays.
4. **Remove Kickoff Data:** Run `RemoveKickoff.py` to clean up the replay data for training.

## Environment
There's a `.env` folder included, which contains a Python environment with the necessary libraries pre-installed.

# Rocket League Replay Data Collection et Traitement

## Introduction
Ce dépôt contient des scripts pour télécharger des replays de Rocket League depuis [Ballchasing.com](https://ballchasing.com) et les traiter pour les utiliser dans l'entraînement d'un bot.

## DownloadReplay.py
Ce script est utilisé pour rechercher et télécharger des replays depuis Ballchasing.com. Par défaut, il télécharge des replays 1v1 entre les joueurs Platinum 1 et Diamond 1 de la Saison 7 de la version gratuite de Rocket League. Il téléchargera au maximum 200 replays. Vous aurez besoin d'un jeton d'API, qui peut être obtenu sur Ballchasing.com/upload.

## rocketReplay.py
Ce script est responsable de la décompilation des replays téléchargés. Il les décompile en format DataFrame et JSON en utilisant la bibliothèque Carball. Il y a aussi une fonction pour obtenir des données avec des positions de joueur et de balle inversées, ainsi que des constantes correspondant aux identifiants des carrosseries Octane et Fennec.

## RemoveKickoff.py
Ce script prend les données récupérées par rocketReplay et supprime les trames entre un but et le début du prochain coup d'envoi pour éliminer les données inutiles à l'entraînement du bot, ce qui pourrait introduire du bruit.

## Comment utiliser
1. **Obtenir un jeton d'API :** Allez sur Ballchasing.com/upload et obtenez votre jeton d'API.
2. **Télécharger les replays :** Exécutez `DownloadReplay.py` avec votre jeton d'API pour télécharger les replays.
3. **Décompiler les replays :** Exécutez `rocketReplay.py` pour décompiler les replays téléchargés.
4. **Supprimer les données de coup d'envoi :** Exécutez `RemoveKickoff.py` pour nettoyer les données du replay pour l'entraînement.

## Environnement
Il y a un dossier `.env` inclus, qui contient un environnement Python avec les bibliothèques nécessaires pré-installées.
