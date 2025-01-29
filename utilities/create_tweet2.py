from requests_oauthlib import OAuth1
import requests
import os

class XApiClient:
    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str):
        self.base_url = "https://api.twitter.com/2"
        self.auth = OAuth1(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )

    def post_tweet(self, text: str) -> dict:
        """
        Post a tweet with the given text using OAuth 1.0a authentication.

        :param text: The text of the tweet to post
        :return: The API response as a dictionary
        """
        url = f"{self.base_url}/tweets"
        payload = {"text": text}
        response = requests.post(url, json=payload, auth=self.auth)
        
        if response.status_code == 201:
            print("Tweet posted successfully!")
        else:
            print(f"Failed to post tweet: {response.status_code} {response.text}")
        
        return response.json()

# Example usage:
# Replace the placeholders with your actual credentials
if __name__ == "__main__":
    client = XApiClient(
        consumer_key=os.environ.get("X_CONSUMER_API_KEY"),
        consumer_secret=os.environ.get("X_CONSUMER_API_KEY_SECRET"),
        access_token=os.environ.get("X_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET")
    )
    tweet_text = "AI News Alert: China's DeepSeek shocks the tech world with their resource-saving AI model, surpassing U.S. giants!"
    response = client.post_tweet(tweet_text)
    print(response)