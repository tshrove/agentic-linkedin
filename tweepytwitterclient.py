import os
import tweepy


class TweepyTwitterClient:
    def __init__(self):
        bearer_token = os.environ.get("X_BEARER_TOKEN")
        consumer_api_key = os.environ.get("X_CONSUMER_API_KEY")
        consumer_api_key_secret = os.environ.get("X_CONSUMER_API_KEY_SECRET")
        access_token = os.environ.get("X_ACCESS_TOKEN")
        access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

        # Authenticate with the Twitter API
        # _auth = tweepy.OAuth2BearerHandler(bearer_token=bearer_token)
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_api_key,
            consumer_secret=consumer_api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def send_tweet(self, message):
        try:
            self.client.create_tweet(text=message)
            print("Tweet sent successfully!")
        except Exception as e:
            print("An error occurred while sending the tweet:", e)
