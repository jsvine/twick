from time import sleep
import logging
import twython
from response import Response

defaults = {
    "result_type": "recent",
    "count": 100
}

logger = logging.getLogger("twick")

class Search(object):
    def __init__(self, credentials):
        self.twitter = twython.Twython(*credentials)

    def query(self, q, **kw):
        opts = dict(defaults)
        opts.update(**kw)
        wait = 1
        while True:
            try:
                response = Response(self.twitter.search(q=q, **opts))
                break
            except twython.exceptions.TwythonError as err:
                logger.info("Twython error: {0}".format(err))
                logger.info("Waiting {0} seconds...".format(wait))
                sleep(wait)
                wait *= 2
        return response
