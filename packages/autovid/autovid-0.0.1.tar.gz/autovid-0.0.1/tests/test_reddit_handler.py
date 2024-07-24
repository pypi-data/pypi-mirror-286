import pytest

import autovid as av

def test_invalid_url():
    with pytest.raises(Exception):
        reddit = av.RedditEngine()
        reddit.fetch("https://www.invalid_url.com")

def test_valid_url():
    try:
        reddit = av.RedditEngine()
        reddit.fetch("https://www.reddit.com/r/reddit.com/comments/87/the_downing_street_memo/")
    except Exception:
        pytest.fail("Unexcepted exception thrown")