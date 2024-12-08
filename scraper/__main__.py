import json
import os
import sys
import argparse
import getpass

from scraper.result import Result
from scraper.twitter_scraper import Twitter_Scraper

try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)


def main():
    try:
        parser = argparse.ArgumentParser(
            add_help=True,
            usage="python scraper [option] ... [arg] ...",
            description="Twitter Scraper is a tool that allows you to scrape tweets from twitter without using Twitter's API.",
        )

        try:
            parser.add_argument(
                "--mail",
                type=str,
                default=os.getenv("TWITTER_MAIL"),
                help="Your Twitter mail.",
            )

            parser.add_argument(
                "--user",
                type=str,
                default=os.getenv("TWITTER_USERNAME"),
                help="Your Twitter username.",
            )

            parser.add_argument(
                "--filePath",
                type=str,
                default=None,
                help="Your Save File Path.",
            )

            parser.add_argument(
                "--password",
                type=str,
                default=os.getenv("TWITTER_PASSWORD"),
                help="Your Twitter password.",
            )
        except Exception as e:
            print(f"Error retrieving environment variables: {e}")
            sys.exit(1)

        parser.add_argument(
            "-t",
            "--tweets",
            type=int,
            default=50,
            help="Number of tweets to scrape (default: 50)",
        )

        parser.add_argument(
            "-u",
            "--username",
            type=str,
            default=None,
            help="Twitter username. Scrape tweets from a user's profile.",
        )

        parser.add_argument(
            "-ht",
            "--hashtag",
            type=str,
            default=None,
            help="Twitter hashtag. Scrape tweets from a hashtag.",
        )

        parser.add_argument(
            "-ntl",
            "--no_tweets_limit",
            nargs='?',
            default=False,
            help="Set no limit to the number of tweets to scrape (will scrap until no more tweets are available).",
        )

        parser.add_argument(
            "-q",
            "--query",
            type=str,
            default=None,
            help="Twitter query or search. Scrape tweets from a query or search.",
        )

        parser.add_argument(
            "-a",
            "--add",
            type=str,
            default="",
            help="Additional data to scrape and save in the .csv file.",
        )

        parser.add_argument(
            "--latest",
            action="store_true",
            help="Scrape latest tweets",
        )

        parser.add_argument(
            "--top",
            action="store_true",
            help="Scrape top tweets",
        )

        args = parser.parse_args()

        USER_MAIL = args.mail
        USER_UNAME = args.user
        USER_PASSWORD = args.password
        FILE_PATH = args.filePath

        if USER_UNAME is None:
            USER_UNAME = input("Twitter Username: ")

        if USER_PASSWORD is None:
            USER_PASSWORD = getpass.getpass("Enter Password: ")

        tweet_type_args = []

        if args.username is not None:
            tweet_type_args.append(args.username)
        if args.hashtag is not None:
            tweet_type_args.append(args.hashtag)
        if args.query is not None:
            tweet_type_args.append(args.query)

        additional_data: list = args.add.split(",")

        if len(tweet_type_args) > 1:
            print(json.dumps(Result.fail_with_msg("Please specify only one of --username, --hashtag, or --query.").to_dict()))
            sys.exit(1)

        if args.latest and args.top:
            print(json.dumps(Result.fail_with_msg("Please specify either --latest or --top. Not both.").to_dict()))
            sys.exit(1)

        if USER_UNAME is not None and USER_PASSWORD is not None:
            scraper = Twitter_Scraper(
                mail=USER_MAIL,
                username=USER_UNAME,
                password=USER_PASSWORD,
                file_path=FILE_PATH,
            )
            # scraper.login()
            scraper.scrape_tweets(
                max_tweets=args.tweets,
                no_tweets_limit=args.no_tweets_limit if args.no_tweets_limit is not None else True,
                scrape_username=args.username,
                scrape_hashtag=args.hashtag,
                scrape_query=args.query,
                scrape_latest=args.latest,
                scrape_top=args.top,
                scrape_poster_details="pd" in additional_data,
            )
            scraper.save_to_json()
            if not scraper.interrupted:
                scraper.driver.close()
        else:
            print(json.dumps(Result.fail_with_msg("Missing Twitter username or password environment variables. Please check your .env file.").to_dict()))
            sys.exit(1)
    except KeyboardInterrupt:
        print(json.dumps(Result.fail_with_msg("Script Interrupted by user. Exiting...").to_dict()))
        sys.exit(1)
    except Exception as e:
        print(json.dumps(Result.fail_with_msg(f"Error: {e}").to_dict()))
        sys.exit(1)
    sys.exit(1)


if __name__ == "__main__":
    main()
