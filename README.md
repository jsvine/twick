# twick (*Twitter, quick.*)

`twick` is a command-line tool for fetching and storing tweets on short notice.

`twick` fetches tweets that match a given search query, and stores them in any [SQLAlchemy-supported](http://docs.sqlalchemy.org/en/rel_0_9/dialects/index.html) database (SQLite, PostgreSQL, MySQL, and more).

Developed at BuzzFeed.

## Installation

`pip install twick`

## Setup

To authenticate its API requests, `twick` requires the standard set of Twitter credentials: API key, API secret, access token, and access token secret. (For instructions on how to obtain these credentials, [read this StackOverflow answer](http://stackoverflow.com/a/12335636) or [follow Dan Nguyen's guide](http://www.compjour.org/tutorials/getting-started-with-tweepy/).) You can either supply them via the `--credentials` command-line argument (as four, space-separated strings), or by setting the following environment variables in your shell:

```sh
export TWICK_API_KEY="[replace me]"
export TWICK_API_SECRET="[replace me]"
export TWICK_ACCESS_TOKEN="[replace me]"
export TWICK_ACCESS_TOKEN_SECRET="[replace me]"
```

## Usage

`twick` has two subcommands:

- `twick fetch` polls for new tweets at a regular interval.

- `twick backfill` pulls earlier tweets, and stops when it can find no more. 

Both store basic data on each tweet (`id`, `text`, `created_at`, `user_name`, `screen_name`, and `user_location`) and each API response (`query`, `count`, `completed_in`, `max_id`, `since_id`, `refresh_url`, `next_results`).

Your __search query__ will be the first argument after each subcommand. You can also supply any of these optional arguments:

- `--db [connection string]`: Any valid SQLAlchemy connection string, describing where to store your results. Default: `sqlite:///twick.sqlite`
- `--throttle [num]`: Wait [num] seconds between API requests. Defaults to 15 to stay under standard rate limits.
- `--store-raw`: Store raw tweet JSON, in addition to excerpted fields described above.
- `--quiet`: Silence logging.
- `--credentials [api_key, api_secret, access_token, access_token_secret]`: See ["Setup"](#setup) above.

## Examples

```sh
twick fetch "harlem building collapse" --db sqlite:///tweets.db
```

```sh
twick fetch "drone from:buzzfeedben" --db sqlite:///ben-drone-tweets.sqlite --throttle 60
```

```sh
twick backfill "to:davidplotz pandas" --store-raw --throttle 5
```

