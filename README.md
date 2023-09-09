# selenium-twitter-scraper

## Setup

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Rename `.env.example` to `.env`.
3. Open .env and update environment variables

```bash
TWITTER_USERNAME=# Your Twitter Handle (e.g. @username)
TWITTER_PASSWORD=# Your Twitter Password
```

## Usage

- Basic usage

```bash
python scraper
```

- Setting maximum number of tweets. defaults to `50`.

```bash
python scraper --tweets=500       # Scrape 500 Tweets
```

### Options and Arguments

```bash
usage: python scraper [arg]

Arguments           Description
--tweets            : No. of tweets. default: 50.
                      e.g. --tweets=500
```
