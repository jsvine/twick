import json
import settings

def get_last_id(db):
    if not "tweets" in db.tables: return None
    q = list(db.query("SELECT MAX(id) AS last_id FROM tweets;"))
    return q[0]["last_id"]
    
def get_first_id(db):
    if not "tweets" in db.tables: return None
    q = list(db.query("SELECT MIN(id) AS first_id FROM tweets;"))
    return q[0]["first_id"]
    
def rowmaker_maker(response_id, store_raw):
    def rowmaker(t):
        items = t.to_row()
        items["response_id"] = response_id
        items["timestamp"] = t.timestamp.strftime(settings.date_format)
        if store_raw: items["raw"] = json.dumps(t.raw)
        return items
    return rowmaker

def store_response(db, response, store_raw=False):
    # Store metadata
    response_table = db["responses"]
    response_id = response_table.insert(response.to_row())
    # Store Tweets
    tweet_table = db["tweets"]
    rowmaker = rowmaker_maker(response_id, store_raw)
    tweet_table.insert_many(map(rowmaker, response.tweets))
