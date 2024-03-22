# selenium-twitter-scraper

## Setup

1. Install dependencies

```bash
pip install -r requirements.txt
```

## Authentication Options

### Using Environment Variable

1. Rename `.env.example` to `.env`.

2. Open `.env` and update environment variables

```bash
TWITTER_USERNAME=# Your Twitter Handle (e.g. @username)
TWITTER_USERNAME=# Your Twitter Username
TWITTER_PASSWORD=# Your Twitter Password
```

### Authentication in Terminal

- Add a `username` and `password` to the command line.

```bash
python scraper --user=@elonmusk --password=password123
```

### No Authentication Provided

- If you didn't specify a username and password, the program will
  ask you to enter a username and password.

```bash
Twitter Username: @username
Password: password123
```

---

**_Authentication Sequence Priority_**

```bash
1. Authentication provided in terminal.
2. Authentication provided in environment variables.
```

---

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

authentication options  description
--user                  : Your twitter account Handle.
                          e.g.
                          --user=@username

--password              : Your twitter account password.
                          e.g.
                          --password=password123

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

-a, --add               : Additional data to scrape and
                          save in the .csv file.

                          values:
                          pd - poster's followers and following

                          e.g.
                            -a "pd"
                            --add="pd"

                          NOTE: Values must be separated by commas.

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

-ntl, --no_tweets_limit : Set no limit to the number of tweets to scrape
                          (will scrap until no more tweets are available).
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
  _(Also works with twitter's advanced search.)_

  - Latest

    ```bash
    python scraper -t 100 -q "Jak Roberto Anti Selos" --latest
    ```

  - Top

    ```bash
    python scraper -t 100 -q "International News" --top
    ```

- **Advanced Search Scraping**

  - For tweets mentioning `@elonmusk`:

    ```bash
    python scraper --query="(@elonmusk)"
    ```

  - For tweets that mentions `@elonmusk` with at least `1000` replies from `January 01, 2020 - August 31, 2023`:

    ```bash
    python scraper --query="(@elonmusk) min_replies:1000 until:2023-08-31 since:2020-01-01"
    ```

  - Perform more `Advanced Search` using Twitter's Advanced Search, just setup the advanced query and copy the resulting string query to the program:
  - **[Twitter Advanced Search](https://twitter.com/search-advanced)**
    [![Image](./img/advanced-search-01.png)](./img/advanced-search-01.png)

- **Scrape Additional Data**

```bash
python scraper --add="pd"
```

| Values | Description                                        |
| :----: | :------------------------------------------------- |
|   pd   | Tweet poster's id, followers, and following count. |

---
