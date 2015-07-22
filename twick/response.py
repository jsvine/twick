from datetime import datetime
from twick.tweet import Tweet
import twick.settings as settings

class Response(object):
    def __init__(self, raw):
        self.raw = raw
        self.tweets = list(map(Tweet, raw["statuses"]))
        self.metadata = dict(raw["search_metadata"])
        self.timestamp = datetime.now()

    def to_row(self):
        return self.metadata
