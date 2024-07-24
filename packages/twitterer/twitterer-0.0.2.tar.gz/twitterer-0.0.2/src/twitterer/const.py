﻿import os

from dotenv import find_dotenv, load_dotenv

env_path = find_dotenv(usecwd=True)
if not (env_path):
    raise Exception("Could not find env file to use authenticate")
load_dotenv(env_path, override=True)

TWITTER_LOGIN_URL = "https://x.com/i/flow/login"
# TWITTER_REDIRECT_URL = "https://x.com/i/flow/login?redirect_after_login=%2Fhome"
TWITTER_HOME_URL = "https://x.com/home"

TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

COOKIES_PATH = "twitter_cookie.pkl"


class Selector:
    USERNAME = "input[autocomplete='username']"
    PASSWORD = "input[autocomplete='current-password']"

    LOGIN_SUCCESSED = "[data-testid='SideNav_AccountSwitcher_Button']"
    LOGIN_FAILED = "[data-testid='mask']"

    LOADING = "circle[style^='stroke']"
    BASE = "[data-testid='tweet']"

    URL = "a[href*='/status/']:not([href$='analytics'])"
    USER_ELEMENTS = "[data-testid='User-Name'] a"
    VERIFIED = "[data-testid='icon-verified']"
    DATE_TIME = "time[datetime]"

    CONTENT = "[data-testid='tweetText'] span,[data-testid='tweetText'] img"

    REPLYS = "[data-testid='reply']"

    UNRETWEETED = "[data-testid='retweet']"
    RETWEETED = "[data-testid='unretweet']"
    RETWEETS = f"{UNRETWEETED},{RETWEETED}"
    RETWEET_CONFIRM = "[data-testid='retweetConfirm']"
    UNRETWEET_CONFIRM = "[data-testid='unretweetConfirm']"

    UNLIKED = "[data-testid='like']"
    LIKED = "[data-testid='unlike']"
    LIKES = f"{UNLIKED},{LIKED}"

    ANALYTICS = "a[href*='/status/'][href$='/analytics']"
    BOOKMARKS = "[data-testid='bookmark']"

    IMGS = "[data-testid='tweetPhoto'][src^='https://pbs.twimg.com/media/'] img"
    VIDEOS = "[data-testid='videoPlayer'],[data-testid='previewInterstitial']"
    VIDEO_THUMBNAILS = (
        "[data-testid='videoPlayer'] video,[data-testid='previewInterstitial'] img"
    )


# $$("[data-testid='tweet']")
# $$("[data-testid='icon-verified']")
# $$("[data-testid='Tweet-User-Avatar']")
# $$("[data-testid='UserAvatar-Container-xxx']")
# $$("[data-testid='User-Name']")
# $$("[data-testid='caret']")
# $$("[data-testid='tweetText']")
# $$("[data-testid='reply']")
# $$("[data-testid='app-text-transition-container']")
# $$("[data-testid='retweet']")
# $$("[data-testid='like']")
# $$("[data-testid='bookmark']")
# $$("[data-testid='tweetPhoto']")
# $$("[data-testid='placementTracking']")
# $$("[data-testid='videoPlayer']")
# $$("[data-testid='videoComponent']")
