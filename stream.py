from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import RateLimitError
import time
from random import randint
import sys
import json


# Variables that contains yours credentials to access Twitter API
consumer_key = "Lg9OKIF1UB7QpVR2gAgQbnz53"
consumer_secret = "1hNMIsBpuHTabB4bW6XmnNhjzXUUyoOMB5gaoJPwb4JlnID4cg"
access_token = "3348799768-JOpvWokBTXSlqw4tCooU2GMesgwk93lFbAUA7uL"
access_token_secret = "oQ7uHuCyKy9vROnia8xeV8aCzJhjksBKXukMn3fr4DeoW"


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self):
        self.users = Users()

    def on_data(self, data):
        data = json.loads(data)
        # print(json.dumps(data, indent=4))
        if 'text' in data:
            self._record_tweet(data)
        if self.users.size() < 100:
            if self.users.size() % 100 == 0:
                print(self.users.size())
            return True
        else:
            return False

    def on_error(self, status):
        print(status)

    def _record_tweet(self, tweet):
        self.users.add([tweet['user']])

class Users:

    users = []

    def add(self, user_list):
        for u in user_list:
            if not self._user_exists(u):
                self.users.append(u)

    def _user_exists(self, user):
        print(user)
        for u in self.users:
            if u.id_str == user.id_str:
                return True
        return False

    def size(self):
        return len(self.users)

    def get_random_ids(self):
        ids = [randint(0, 10000000) for _ in range(100)]
        print(ids)
        return ids





if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter tweets from the words.
    stream.sample()

    api = API(auth)

    rest_users = Users()

    #while rest_users.size() < 10:
    for i in range(5):
        try:
            res = api.lookup_users(user_ids=rest_users.get_random_ids())
            rest_users.add(res)
        except RateLimitError:
            print('rate')
            time.sleep(15*60)

    print(rest_users.size())

