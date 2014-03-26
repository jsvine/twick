from datetime import datetime, time
import settings

def parse_created_at(created_at):
    return datetime.strptime(created_at, settings.date_format)

class Tweet(object):
    def __init__(self, raw):
        self.raw = raw
        self.timestamp = parse_created_at(raw["created_at"])
    def to_row(self):
        return {
            "id": self.raw["id"],
            "text": self.raw["text"],
            "created_at": self.raw["created_at"],
            "user_name": self.raw["user"]["name"],
            "screen_name": self.raw["user"]["screen_name"],
            "user_location": self.raw["user"]["location"]
        }
