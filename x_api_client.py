from requests_oauthlib import OAuth1
import requests

class XApiClient:
    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str):
        self.base_url = "https://api.twitter.com/2"
        self.auth = OAuth1(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )

    def post_tweet(self, text: str) -> bool:
        """
        Post a tweet with the given text using OAuth 1.0a authentication.

        :param text: The text of the tweet to post
        :return: The API response as a dictionary
        """
        try:
            url = f"{self.base_url}/tweets"
            payload = {"text": text}
            response = requests.post(url, json=payload, auth=self.auth)
            
            if response.status_code == 201:
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False