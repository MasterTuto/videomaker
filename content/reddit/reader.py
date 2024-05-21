import os
import math
from typing import Literal

import praw

import utilities.config.reddit as reddit_config
from utilities.types.reddit_types import RedditStoryConfig
from utilities.types.languages import SupportedLanguages
from utilities.persistence.manager import PersistenceManager
from translate import Translator


class RedditReader:
    def __init__(self, persistence: PersistenceManager):
        self.reddit = praw.Reddit(
            client_id=reddit_config.CLIENT_ID,
            client_secret=reddit_config.CLIENT_SECRET,
            user_agent="videomaker/mastertuto",
        )

        self.persistence = persistence

    def deploy_used_items(self):
        self.persistence.commit()

    def sample(self, config: RedditStoryConfig):
        reddit_config = config['reddit']
        subreddit = reddit_config['name']
        number_of_posts = reddit_config['number_of_posts']
        number_of_comments = reddit_config['number_of_comments']
        max_body_length = reddit_config['max_body_length']
        select = reddit_config['select']
        

        max_body_length = max_body_length if max_body_length > 0 else math.inf
        sub = self.reddit.subreddit(subreddit)

        top_posts: list[praw.reddit.Submission] = sub.top(limit=None, time_filter="all")
        top_posts = list(top_posts)

        selected_posts: list[praw.reddit.Submission] = []

        iteration = 0
        timefilters = ["all", "year", "week", "month", "day", "hour"]
        while True:
            for post in top_posts:
                if len(selected_posts) >= number_of_posts: break
                if post.locked: continue
                if len(post.selftext.strip()) >= min(max_body_length, 4500): continue

                if post.id not in self.persistence:
                    selected_posts.append(post)
                    self.persistence.append(post.id)
                
            if len(selected_posts) >= number_of_posts:
                break

            top_posts: list[praw.reddit.Submission] = sub.top(limit=None, time_filter=timefilters[iteration+1])
            top_posts = list(top_posts)

            iteration += 1

        
        content: list[str] = []
        translator = Translator("pt-br", config['lang'])
        for post_index, post in enumerate(selected_posts):
            if len(selected_posts) > 1:
                content.append(translator.translate(f"Publicação número {post_index+1}"))
        
            if 'title' in select:
                title: str = post.title.strip() or ''
                if title: content.append(title)

            if 'body' in select:
                body: str = post.selftext.strip() or ''
                if body: content.append(body)

            if 'comments' in select:
                post.comments.replace_more(limit=None)
                comment_index = 0
                for top_level_comment in post.comments:
                    content.append(translator.translate(f"Comentário número {comment_index+1}"))
                    if number_of_comments <= 0:
                        break

                    if top_level_comment.body: content.append(top_level_comment.body)
                    number_of_comments -= 1
                    comment_index += 1

        return content

