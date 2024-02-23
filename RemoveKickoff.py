import os
import json
import pandas as pd

def remove_frames_between_goals_and_kickoffs(data_frame, goals, kickoffs):
    # Remove frames between goals and kickoffs
    for goal in goals:
        goal_frame = goal['frameNumber']
        next_kickoff_frame = next((kickoff['startFrameNumber'] for kickoff in kickoffs if kickoff['startFrameNumber'] > goal_frame), None)
        if next_kickoff_frame:
            data_frame = data_frame.drop(range(goal_frame + 1, next_kickoff_frame))

    # Remove frames between start and end of each kickoff
    for kickoff in kickoffs:
        kickoff_start_frame = kickoff['startFrameNumber']
        kickoff_end_frame = kickoff['endFrameNumber']
        data_frame = data_frame.drop(range(kickoff_start_frame, kickoff_end_frame + 1))

    return data_frame

# Directory paths
json_directory = 'JSON'
data_directory = 'Data'

# Iterate over each JSON file in the JSON folder
for json_file in os.listdir(json_directory):
    if json_file.endswith('.json'):
        # Load JSON data
        with open(os.path.join(json_directory, json_file)) as f:
            json_data = json.load(f)

        # Extract relevant information
        goals = json_data['gameMetadata']['goals']
        kickoffs = json_data['gameStats']['kickoffs']

        # Load corresponding DataFrames
        data_file_name = os.path.splitext(json_file)[0]
        data_file_name = "-".join(data_file_name.split("-")[1:])     
        
        try:
            data_file_path = os.path.join(data_directory, f'Data-{data_file_name}.csv')
            data_frame = pd.read_csv(data_file_path)
            #data_frame_invert = pd.read_csv(os.path.join(data_directory, f'Data-Invert-{data_file_name}.csv'))

            # Remove frames between goals and kickoffs
            data_frame_modified = remove_frames_between_goals_and_kickoffs(data_frame.copy(), goals, kickoffs)
            #data_frame_invert_modified = remove_frames_between_goals_and_kickoffs(data_frame_invert.copy(), goals, kickoffs)

            # Save modified DataFrames to new CSV files
            modified_data_file_path = os.path.join(data_directory, f'Data-Modified-{data_file_name}.csv')
            #modified_data_file_path_invert = os.path.join(data_directory, f'Data-Modified-Invert-{data_file_name}.csv')
            data_frame_modified.to_csv(modified_data_file_path, index=False)
            #data_frame_invert_modified.to_csv(modified_data_file_path_invert, index=False)

            print(f"Processed {json_file}")
        except:
            pass

print("All JSON files processed.")
