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

- Show Help

```bash
python scraper --help
```

- Basic usage

```bash
python scraper
```

- Setting maximum number of tweets. defaults to `50`.

```bash
python scraper --tweets=500   # Scrape 500 Tweets
```

- Options and Arguments

```bash
usage: python scraper [option] ... [arg] ...

options:                description
-t, --tweets            : Number of tweets to scrape (default: 50).
                          e.g.
                            -t 500
                            --tweets=500

-u, --username          : Twitter username.
                          Scrape tweets from a user's profile.
                          e.g.
                            -u elonmusk
                            --username=@elonmusk

-ht, --hashtag          : Twitter hashtag.
                          Scrape tweets from a hashtag.
                          e.g.
                            -ht javascript
                            --hashtag=javascript

-q, --query             : Twitter query or search.
                          Scrape tweets from a query or search.
                          e.g.
                            -q "Philippine Marites"
                            --query="Jak Roberto anti selos"

--latest                : Twitter latest tweets (default: True).
                          Note: Only for hashtag-based
                          and query-based scraping.
                          usage:
                            python scraper -t 500 -ht=python --latest

--top                   : Twitter top tweets (default: False).
                          Note: Only for hashtag-based
                          and query-based scraping.
                          usage:
                            python scraper -t 500 -ht=python --top
```

### Sample Scraping Commands

- **Custom Limit Scraping**

```bash
python scraper -t 500
```

- **User Profile Scraping**

```bash
python scraper -t 100 -u elonmusk
```

- **Hashtag Scraping**

  - Latest

    ```bash
    python scraper -t 100 -ht python --latest
    ```

  - Top

    ```bash
    python scraper -t 100 -ht python --top
    ```

- **Query or Search Scraping**
  _(Also works with twitter advanced search.)_

  - Latest

    ```bash
    python scraper -t 100 -q "Jak Roberto Anti Selos" --latest
    ```

  - Top

    ```bash
    python scraper -t 100 -q "International News" --top
    ```
