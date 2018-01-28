import webapp2
import twitter

from model.tweet import Tweet
import twitter_token

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class RefreshData(webapp2.RequestHandler):
    def get(self):
        api = twitter.Api(consumer_key=twitter_token.CONSUMER_KEY,
                          consumer_secret=twitter_token.CONSUMER_SECRET,
                          access_token_key=twitter_token.ACCESS_TOKEN_KEY,
                          access_token_secret=twitter_token.ACCESS_TOKEN_SECRET)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Refreshing data from Twitter...')
        tweet = Tweet()
        tweet.politician = "TestPolitician"
        tweet.content = "Test tweet"
        tweet.put()
        self.response.write('\nFinished loading.\n')
        statuses = api.GetUserTimeline(screen_name='pietrograsso')
        for s in statuses:
            self.response.write(str(s)+ '\n')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/refresh', RefreshData),
], debug=True)
