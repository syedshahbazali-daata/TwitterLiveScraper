import datetime
import time
import tweepy
import json
import csv
from DatabaseManager import add_row


########################################################################################################################
#                                                                                                                      #
#                                        PLEASE DON'T CHANGE ANYTHING BELOW                                            #
#                                                                                                                      #
########################################################################################################################
with open("twitter-credentials.json", "r") as file:
    # Reading the credentials from the json file
    creds_data = json.load(file)

target_username = creds_data["target_username"]
api_key = creds_data["api_key"]
api_secret = creds_data["api_secret"]
access_token = creds_data["access_token"]
access_token_secret = creds_data["access_token_secret"]


# Important Functions
def get_file_data(file):
    """
    :param file: File name with extension (.txt).
    :return: List of rows in the file.
    """
    with open(file, encoding="utf8") as f:
        data = f.read().strip()
        my_file_data = data.split('\n')

    return my_file_data

def convert_to_epoch(my_date_time: str):
    """
    :param my_date_time: get Date into String Format
    :return: epoch time
    """
    date_time = my_date_time
    pattern = '%d-%m-%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    return epoch


def update_data(file, data):
    """
    :param file: File name with extension (.txt).
    :param data: Data to be written in the file.
    :return: None
    """
    with open(file, "a", encoding="utf8") as f:
        f.write(data + '\n')
    return None


# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print(datetime.datetime.now(), "Authenticated to Twitter")
while True:

    try:
        public_tweets = api.user_timeline(screen_name=target_username)  # target_username_data
        tweets = tweepy.Cursor(api.user_timeline, id=target_username).items(200)  # get target_username last 200 tweets

        for index, tweet in enumerate(tweets):
            tweet_text = tweet.text  # get tweet text
            tweet_id = str(tweet.id)  # get tweet id
            account_id = str(tweet.user.id)  # get account id
            account_name = str(tweet.user.screen_name)  # get account name
            current_time = str(datetime.datetime.utcnow())

            # Dates Management to scrape current date Data only
            today_date = str(datetime.date.today().strftime("%d-%m-%Y"))
            created_at = str(tweet._json['created_at']).split(" ")
            created_at_date = f"{created_at[2]}-{created_at[1]}-{created_at[-1]}"
            created_at_time = created_at[3]
            d = datetime.datetime.strptime(created_at_date, '%d-%b-%Y')
            created_at_date_format = str(datetime.date.strftime(d, "%d-%m-%Y"))

            if created_at_date_format == today_date:  # if tweet created at date is today date
                
                epoch_time = convert_to_epoch(f"{created_at_date_format} {created_at_time}")
                record = [tweet_id,account_id,account_name,target_username,tweet_text, created_at_date_format, created_at_time, epoch_time, current_time]
              
                
                
                already_done_text = f"{tweet_text} {created_at_date_format} {created_at_time}"
                already_done = get_file_data(
                    "AlreadyDone.txt")  # This File contains all scraped tweets id

                if tweet_id not in already_done:
                    # to get only tweets that are not scraped before (Non Duplicated Tweets)
                    print("Tweet Received: ", record)
                    update_data("AlreadyDone.txt",
                                str(tweet_id))  # append Tweet ID AlreadyDone.txt file
                    add_row(record)

                    """with open("Live Scraper Data Files/Live Tweets Scraping.csv", "a", encoding="utf8",
                              newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(record)"""

            else:  # if tweet created at date is not today date (to stop scraping) and again start scraping

                print(
                    f"No new tweets last checked at {datetime.datetime.now().strftime('%H:%M:%S')}"
                    f" for Username: {target_username}")

                break
        time.sleep(5)  # to wait 5 seconds before scraping again
    except Exception as e:
        print(e)
        print("Waiting for 1 minute to start scraping again Due to Any Error")
        print(datetime.datetime.now())
        time.sleep(60)  # to wait 1 minute before scraping again (if there is an error)

