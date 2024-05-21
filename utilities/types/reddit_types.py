from typing import TypedDict, Literal

from utilities.types.languages import SupportedLanguages

class RedditSource(TypedDict):
    name: str
    readable_name: str
    subname_position: int
    select: list[Literal['comment', 'title', 'body']]

    max_body_length: int
    number_of_posts: int
    number_of_comments: int
    

class RedditStoryConfig(TypedDict):
    lang: SupportedLanguages
    hashtags: str
    reddit: RedditSource