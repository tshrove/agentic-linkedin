import os
from requests_oauthlib import OAuth1Session
import json


class TweepyTwitterClient:
    def __init__(self):
        self.bearer_token = os.environ.get("X_BEARER_TOKEN")
        self.consumer_api_key = os.environ.get("X_CONSUMER_API_KEY")
        self.consumer_api_key_secret = os.environ.get("X_CONSUMER_API_KEY_SECRET")
        self.access_token = os.environ.get("X_ACCESS_TOKEN")
        self.access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")
        self.verifier = os.environ.get("X_VERIFIER")

    def load(self):
        # Get request token
        # request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        # oauth = OAuth1Session(self.consumer_api_key, client_secret=self.consumer_api_key_secret)
        
        # try:
        #     fetch_response = oauth.fetch_request_token(request_token_url)
        # except ValueError as ex:
        #     raise ex
        
        # resource_owner_key = fetch_response.get("oauth_token")
        # resource_owner_secret = fetch_response.get("oauth_token_secret")
        # print("Got OAuth token: %s" % resource_owner_key)
        
        # # Get authorization
        # #base_authorization_url = "https://api.twitter.com/oauth/authorize"
        # #authorization_url = oauth.authorization_url(base_authorization_url)
        
        # # Get the access token
        # access_token_url = "https://api.twitter.com/oauth/access_token"
        # oauth = OAuth1Session(
        #     self.consumer_api_key,
        #     client_secret=self.consumer_api_key_secret,
        #     resource_owner_key=resource_owner_key,
        #     resource_owner_secret=resource_owner_secret,
        #     verifier=self.verifier,
        # )
        # oauth_tokens = oauth.fetch_access_token(access_token_url)

        # access_token = os.environ.get("X_ACCESS_TOKEN")
        # access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

        # Make the request
        self.oauth = OAuth1Session(
            self.consumer_api_key,
            client_secret=self.consumer_api_key_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

    def send_tweet(self, message):
        try:
            payload = {"text": message}
            # Making the request
            response = self.oauth.post(
                "https://api.twitter.com/2/tweets",
                json=payload,
            )

            if response.status_code != 201:
                raise Exception(
                    "Request returned an error: {} {}".format(response.status_code, response.text)
                )

            print("Response code: {}".format(response.status_code))

            # Saving the response as JSON
            json_response = response.json()
            print(json.dumps(json_response, indent=4, sort_keys=True))
        except Exception as e:
            print("An error occurred while sending the tweet:", e)
