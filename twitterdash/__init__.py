from .scraper import get_last_month_tweets

import os

# register the portals
from twitterdash import routes
from twitterdash.routes import app
from twitterdash.preprocessing import process_text
