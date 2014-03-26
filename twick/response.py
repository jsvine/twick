from tweet import Tweet
from datetime import datetime
import settings

class Response(object):
    def __init__(self, raw):
        self.raw = raw
        self.tweets = map(Tweet, raw["statuses"])
        self.metadata = dict(raw["search_metadata"])
        self.timestamp = datetime.now()

    def to_row(self):
        return self.metadata
