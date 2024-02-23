
import carball
import json
import os
import carball
import gzip
from carball.json_parser.game import Game
from carball.analysis.analysis_manager import AnalysisManager
import pandas as pd

OCTANE = 4284
FENNEC = 23

def invert_perspective(df):
    # Get the player names
    players = df.columns.levels[0]

    # Invert positions
    df.loc[:, (players[0], 'pos_x')] *= -1
    df.loc[:, (players[1], 'pos_x')] *= -1
    df.loc[:, ('ball', 'pos_x')] *= -1

    df.loc[:, (players[0], 'pos_y')] *= -1
    df.loc[:, (players[1], 'pos_y')] *= -1
    df.loc[:, ('ball', 'pos_y')] *= -1

    df.loc[:, (players[0], 'pos_z')] *= -1
    df.loc[:, (players[1], 'pos_z')] *= -1
    df.loc[:, ('ball', 'pos_z')] *= -1

    # Invert orientations (rotation)
    df.loc[:, (players[0], 'rot_x')] *= -1
    df.loc[:, (players[1], 'rot_x')] *= -1
    df.loc[:, ('ball', 'rot_x')] *= -1

    df.loc[:, (players[0], 'rot_y')] *= -1
    df.loc[:, (players[1], 'rot_y')] *= -1
    df.loc[:, ('ball', 'rot_y')] *= -1

    df.loc[:, (players[0], 'rot_z')] *= -1
    df.loc[:, (players[1], 'rot_z')] *= -1
    df.loc[:, ('ball', 'rot_z')] *= -1

    # Invert velocities
    df.loc[:, (players[0], 'vel_x')] *= -1
    df.loc[:, (players[1], 'vel_x')] *= -1
    df.loc[:, ('ball', 'vel_x')] *= -1

    df.loc[:, (players[0], 'vel_y')] *= -1
    df.loc[:, (players[1], 'vel_y')] *= -1
    df.loc[:, ('ball', 'vel_y')] *= -1

    df.loc[:, (players[0], 'vel_z')] *= -1
    df.loc[:, (players[1], 'vel_z')] *= -1
    df.loc[:, ('ball', 'vel_z')] *= -1

    # Create a list of columns for each player
    player_columns = []
    for player in players:
        player_columns.extend([(player, col) for col in df[player].columns])

    # Reorder the player columns in reverse order
    new_columns = pd.MultiIndex.from_tuples(player_columns[::-1])

    # Update the DataFrame with the new column order
    df = df[new_columns]

    return df

def print_player_info_at_frame(df, frame_index):
    # Get the player names
    players = df.columns.levels[0][:2]  # Assuming the first two are player names

    # Get the data at the specified frame index
    frame_data = df.iloc[frame_index]

    # Print information for each player
    for player in players:
        print(f"Player: {player}")
        player_data = frame_data[player]
        print(player_data)


# Obtention du chemin du dossier où se trouve le script Python
script_directory = os.path.dirname(os.path.realpath(__file__))
replays_directory = os.path.join(script_directory, 'Replays')

# Création des dossiers JSON et Data s'ils n'existent pas
json_directory = os.path.join(script_directory, 'JSON')
if not os.path.exists(json_directory):
    os.makedirs(json_directory)

data_directory = os.path.join(script_directory, 'Data')
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Parcours de tous les fichiers de replay dans le dossier "Replays"
for replay_file in os.listdir(replays_directory):
    if replay_file.endswith('.replay'):
        replay_name = os.path.splitext(replay_file)[0]
        replay_path = os.path.join(replays_directory, replay_file)

        try:
            # Lecture du replay
            data = carball.decompile_replay(replay_path)
            game = Game()
            game.initialize(loaded_json=data)
            analysis_manager = AnalysisManager(game)
            analysis_manager.create_analysis()
            
            # Écriture du JSON
            json_file_path = os.path.join(json_directory, f'Json-{replay_name}.json')
            with open(json_file_path, 'w') as json_file:
                analysis_manager.write_json_out_to_file(json_file)
                
            json_data = analysis_manager.get_json_data()

            # Récupération des données DataFrame
            data_frame = analysis_manager.get_data_frame()

            # Filtre des colonnes
            filtered_columns = [(player, prop) for player, prop in data_frame.columns.to_list()
                                if prop != 'ping' and prop != 'ball_cam']
            data_frame = data_frame[[col for col in filtered_columns]]
            
            if True or json_data["players"][0]["loadout"]["car"] == OCTANE or json_data["players"][0]["loadout"]["car"] == FENNEC:
                # Écriture du DataFrame dans un fichier CSV (non inversé)
                data_file_path = os.path.join(data_directory, f'Data-{replay_name}.csv')
                data_frame.to_csv(data_file_path, index=False)

            """
            # Inversion de la perspective
            data_frame_invert = invert_perspective(data_frame)

            # Écriture du DataFrame inversé dans un fichier CSV
            if json_data["players"][1]["loadout"]["car"] == OCTANE or json_data["players"][1]["loadout"]["car"] == FENNEC:
                data_file_path_invert = os.path.join(data_directory, f'Data-Invert-{replay_name}.csv')
                data_frame_invert.to_csv(data_file_path_invert, index=False)
            """

            print(f"Traitement terminé pour {replay_file}")
        except:
            pass

print("Tous les replays ont été traités.")
