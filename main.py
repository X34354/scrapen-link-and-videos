from download_link import link
from download_videos import clean_and_process_videos
import json 

if __name__ == "__main__":
    # Open the JSON file
    with open('configuration.json', 'r') as file:
        data = json.load(file)

    link(data)
    clean_and_process_videos(data)