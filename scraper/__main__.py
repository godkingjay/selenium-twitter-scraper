import os
import sys
import argparse
from twitter_scraper import Twitter_Scraper

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
        USER_UNAME = os.getenv('TWITTER_USERNAME')
        USER_PASSWORD = os.getenv('TWITTER_PASSWORD')
    except Exception as e:
        print(f"Error retrieving environment variables: {e}")
        USER_UNAME = None
        USER_PASSWORD = None
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Twitter Scraper')
    parser.add_argument('--tweets', type=int, default=50,
                        help='Number of tweets to scrape (default: 50)')
    args = parser.parse_args()

    if USER_UNAME is not None and USER_PASSWORD is not None:
        try:
            scraper = Twitter_Scraper(
                username=USER_UNAME,
                password=USER_PASSWORD,
                max_tweets=args.tweets
            )

            scraper.scrape_tweets()
            scraper.driver.close()
            scraper.save_to_csv()
        except KeyboardInterrupt:
            print("\nScript Interrupted by user. Exiting...")
            sys.exit(1)
    else:
        print("Missing Twitter username or password environment variables. Please check your .env file.")
        sys.exit(1)


if __name__ == '__main__':
    main()
