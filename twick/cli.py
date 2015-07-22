#!/usr/bin/env python
import sys, os
import re
import argparse
import dataset
import logging
from datetime import datetime
from time import sleep
from getpass import getpass
from twick.search import Search
from twick.persistence import get_last_id, get_first_id, store_response
import twick.settings as settings

logging.basicConfig()
logger = logging.getLogger("twick")

DEFAULT_DB = "sqlite:///twick.sqlite"

CREDENTIAL_NAMES = [
    "TWICK_API_KEY",
    "TWICK_API_SECRET",
    "TWICK_ACCESS_TOKEN",
    "TWICK_ACCESS_TOKEN_SECRET"
]

def try_credential(name):
    try: return os.environ[name]
    except: raise Exception("Missing environment variable ${}".format(name))

def get_credentials(credential_array=None):
    if credential_array: return credential_array
    return map(try_credential, CREDENTIAL_NAMES)

linebreak_pattern = re.compile(r"[\n\r]+")
def format_tweet(t):
    timestamp = t.timestamp.strftime(settings.date_format)
    screen_name = t.raw["user"]["screen_name"]
    text = t.raw["text"].strip()
    formatted = u"Tweet @ {}: <{}>: {}".format(timestamp, screen_name, text)
    newlines_removed = re.sub(linebreak_pattern, " ", formatted)
    return newlines_removed

def log_response(response):
    logger.info(u"Response @ {}: Found {} tweet(s).".format(
        response.timestamp.strftime(settings.date_format),
        len(response.tweets)))
    map(logger.info, map(format_tweet, response.tweets))
    pass

def cmd_fetch(args):
    search = Search(args.credentials)
    while True:
        last_id = get_last_id(args.db)
        response = search.query(args.query, since_id=last_id)
        log_response(response)
        store_response(args.db, response, args.store_raw)
        sleep(args.throttle)

def cmd_backfill(args):
    search = Search(args.credentials)
    while True:
        # Note: Unlike since_id, max_id is inclusive
        # Cf.: https://dev.twitter.com/docs/working-with-timelines
        first_id = get_first_id(args.db)
        max_id = (first_id or sys.maxsize) - 1
        response = search.query(args.query, max_id=max_id)
        log_response(response)
        store_response(args.db, response, args.store_raw)
        if not len(response.tweets): break 
        else: sleep(args.throttle)

def dispatch_command(args):
    commands = {
        "fetch": cmd_fetch,
        "backfill": cmd_backfill,
    } 
    commands[args.command](args)

def add_shared_args(parser):
    parser.add_argument("query")
    parser.add_argument("--db",
        type=dataset.connect,
        help="SQLAlchemy connection string. Default: " + DEFAULT_DB,
        default=DEFAULT_DB)
    parser.add_argument("--throttle",
        type=int,
        default=15,
        help="""Wait X seconds between requests.
        Default: 15 (to stay under rate limits)""")
    parser.add_argument("--credentials",
        nargs=4,
        help="""
            Four space-separated strings for {}.
            Defaults to environment variables by those names.
        """.format(", ".join(CREDENTIAL_NAMES))
    )
    parser.add_argument("--store-raw",
        help="Store raw tweet JSON, in addition to excerpted fields.",
        action="store_true")
    parser.add_argument("--quiet",
        help="Silence logging.",
        action="store_true")
    
def parse_args():
    parser = argparse.ArgumentParser(prog="twick")
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    parser_fetch = subparsers.add_parser("fetch")
    add_shared_args(parser_fetch)

    parser_backfill = subparsers.add_parser("backfill")
    add_shared_args(parser_backfill)

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    args.credentials = get_credentials(args.credentials)
    logger.setLevel(logging.WARNING if args.quiet else logging.INFO)
    dispatch_command(args)

if __name__ == "__main__":
    main()
