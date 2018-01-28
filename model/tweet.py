from google.appengine.ext import ndb

class Tweet(ndb.Model):
    politician = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    dateRetrieved = ndb.DateTimeProperty(auto_now_add=True)
    dateCreated = ndb.DateTimeProperty()
