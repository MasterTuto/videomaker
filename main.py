import os
import json
from random import choices, shuffle
from typing import Union

from content.builders.reddit_stories import RedditStoriesBuilder, RedditStoryConfig
from content.builders.simple_splits import SimpleSplitsBuilder, SimpleSplitsConfig
from tiktok.post import TiktokPoster
from utilities.shared import load, unload
from utilities.config.accounts import ACCOUNTS
from utilities.config.folder import CONFIGS_FOLDER, PERSISTENT_FOLDER
from utilities.persistence.manager import PersistenceManager

details_joiner = "/<!!>/"

def get_persistence_file(config_file_path):
    _, persitence_file_name = os.path.split(config_file_path)
    persitence_file_name, _ = os.path.splitext(persitence_file_name)
    persitence_file_name = persitence_file_name + '.txt'
    file_path =f"{PERSISTENT_FOLDER}/{persitence_file_name}"

    return PersistenceManager(file_path)

def post_videos(details: list[str]):
    print("Postando video antigo!!")
    previous_account_number: str = ''
    for detail_index, detail in enumerate(details):
        account_number, video_path = detail.split(details_joiner)
        
        ttk_post: TiktokPoster|None = None
        if previous_account_number == '' or previous_account_number != account_number:
            previous_account_number = account_number
            account = ACCOUNTS[int(account_number)]
            
            login_file = account['login_file'] if account else ''

            if ttk_post:
                ttk_post.close()

            ttk_post = TiktokPoster(login_file)

        if ttk_post:
            ttk_post.post(video_path)
            yield detail_index


def main():
    try:
        load()

        produced_files = PersistenceManager("videos_produced.txt")

        if produced_files:
            content = produced_files.content.copy()
            for posted_video in post_videos(content):
                produced_files.remove(posted_video)
                produced_files.commit()
            produced_files.content = []
            produced_files.commit()

        shuffle(ACCOUNTS)
        for account_number, account in enumerate(ACCOUNTS):
            ttk_poster = TiktokPoster(account['login_file'])

            videos_configs = account['videos_config']
            selected_configs = choices(videos_configs, k=2)
            for video_config in selected_configs:
                video_config_path = os.path.join(CONFIGS_FOLDER, video_config)

                with open(video_config_path, 'r') as f:
                    config = json.load(f)

                builder: Union[RedditStoriesBuilder, SimpleSplitsBuilder, None] = None

                if account['type'] == 'reddit_stories':
                    builder = RedditStoriesBuilder(config)
                elif account['type'] == 'simple_splits':
                    builder = SimpleSplitsBuilder(config)
                else:
                    raise ValueError("No builder found for "+account['type'])

                percistence = get_persistence_file(video_config_path)
                try:
                    videopath = builder.build(percistence, translate_to=account['lang'])
                except Exception as e:
                    print("Erro ao gerar video usando o builder: " + account['type'])
                    raise e

                video_metadata = details_joiner.join([str(account_number), videopath])
                video_index = produced_files.append(video_metadata)
                produced_files.commit()
                builder.deploy()
        
                try:
                    ttk_poster.post(videopath)
                    produced_files.remove(video_index)
                    produced_files.commit()
                except:
                    pass
            ttk_poster.close()
    finally:
        unload()

if __name__ == "__main__":
    main()