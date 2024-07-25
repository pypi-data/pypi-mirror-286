import praw

from autovid import api_keys
from autovid import exceptions

__all__ = ['_fetch_post', '_fetch_comment']

def __getcredentials():
    return praw.Reddit(
        client_id=api_keys.client_id,
        client_secret=api_keys.client_secret,
        user_agent="autovid 0.0.1"
    )

def _fetch_post(url:str):
    reddit = __getcredentials()
    submission = reddit.submission(url=url)
    return submission

def _fetch_comment(url:str):
    reddit = __getcredentials()
    submission = reddit.comment(url=url)
    return submission