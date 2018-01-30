from google.appengine.ext import ndb

class Tweet(ndb.Model):
    id = ndb.IntegerProperty()
    candidate = ndb.StringProperty()
    text = ndb.StringProperty(indexed=False)
    dateRetrieved = ndb.DateTimeProperty(auto_now_add=True)
    dateCreated = ndb.DateTimeProperty()
