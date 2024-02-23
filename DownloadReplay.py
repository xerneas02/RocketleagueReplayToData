import requests
import os
import time

def download_replays():
    # Define your API token
    token = "API_TOKEN"

    # Define the ranks you want to download replays for
    ranks = ["platinum-1", "diamond-1"]

    # Create folder if it doesn't exist
    folder_path = "./Replays"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Base URL for replay download
    base_url = "https://ballchasing.com/api/replays"

    # Parameters for filtering replays by rank and other criteria
    params = {
        "playlist": "ranked-duels",
        "min-rank": ranks[0],
        "max-rank": ranks[1],
        "count": 200, 
        "sort-by": "created",  
        "sort-dir": "desc",
        "season": "f7"
    }

    # Make request to get replays
    response = requests.get(base_url, params=params, headers={"Authorization": token})
    if response.status_code == 200:
        replays = response.json().get("list", [])

        # Download and save replays
        for replay in replays:
            replay_id = replay.get("id")
            replay_title = replay.get("title", replay_id)
            download_url = f"{base_url}/{replay_id}/file"
            rank = replay.get("rank")
            file_path = f"{folder_path}/{replay_title}.replay"

            # Download the replay file
            r = requests.get(download_url, headers={"Authorization": token})
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                print(f"Downloaded {replay_title} to 'Replays' folder.")
            elif r.status_code == 429:
                # If rate limited, wait and retry
                print(f"Rate limited. Waiting and retrying...")
                time.sleep(5)  # Wait for 5 seconds
                r = requests.get(download_url, headers={"Authorization": token})
                if r.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                    print(f"Downloaded {replay_title} to 'Replays' folder.")
                else:
                    print(f"Failed to download {replay_title}. Status code: {r.status_code}")
            else:
                print(f"Failed to download {replay_title}. Status code: {r.status_code}")
    else:
        print("Failed to fetch replays.")

if __name__ == "__main__":
    download_replays()