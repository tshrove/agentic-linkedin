from tweepytwitterclient import TweepyTwitterClient

client = TweepyTwitterClient()
client.load()
client.send_tweet("Hello world!")