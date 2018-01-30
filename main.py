import webapp2
import twitter
from datetime import datetime

import app_config
import twitter_token
from model.tweet import Tweet


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class RefreshData(webapp2.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(RefreshData, self).__init__(*args, **kwargs)
        self.api = twitter.Api(consumer_key=twitter_token.CONSUMER_KEY,
                               consumer_secret=twitter_token.CONSUMER_SECRET,
                               access_token_key=twitter_token.ACCESS_TOKEN_KEY,
                               access_token_secret=twitter_token.ACCESS_TOKEN_SECRET)

    def getTweetsforCandidate(self, screen_name):
        storedTweets = Tweet.query().filter(Tweet.candidate == screen_name).order(Tweet.id).fetch()
        if not storedTweets:
            tweets = self.api.GetUserTimeline(screen_name=screen_name, count=100)
        else:
            tweets = self.api.GetUserTimeline(screen_name=screen_name, since_id=storedTweets[-1].id, count=100)
        for t in tweets:
            tweet = Tweet()
            tweet.candidate = screen_name
            tweet.text = t.text
            tweet.id = t.id
            tweet.dateCreated = datetime.strptime(t.created_at, '%a %b %d %H:%M:%S +0000 %Y')
            tweet.put()
            self.response.write('\n' + str(tweet))

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Refreshing data from Twitter...')
        for candidate in app_config.TRACKED_POLITICIANS_SCREENAME:
            self.response.write('\nLoading ' + candidate + '...')
            self.getTweetsforCandidate(candidate)
        self.response.write('\nFinished loading.')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/refresh', RefreshData),
], debug=True)
