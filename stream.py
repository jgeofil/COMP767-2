from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import RateLimitError
from tweepy import User as TwUser
import time
from random import randint, choice
import json
import numpy as np

RUN = '_shorts5'
SIZE = 5000

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
        if self.users.size() <= SIZE:
            if self.users.size() % 1000 == 0:
                print(self.users.size())
            return True
        else:
            return False

    def on_error(self, status):
        print(status)

    def _record_tweet(self, tweet):
        self.users.add([TwUser.parse(None, tweet['user'])])

class Users:

    def __init__(self, long_ids=False):
        self.users = []
        self.long_ids = long_ids

    def add(self, user_list):
        for u in user_list:
            if (self.long_ids or self._short_id(u)) and not self._user_exists(u):
                self.users.append(u)

    def _user_exists(self, user):
        for u in self.users:
            if u.id_str == user.id_str:
                return True
        return False

    def _short_id(self, user):
        return True if len(user.id_str) < 18 else False

    def size(self):
        return len(self.users)

    def get_random_ids(self):
        ids = [randint(*choice(self.get_id_ranges())) for _ in range(100)]
        return ids

    def get_ids(self):
        return [int(u.id_str) for u in self.users]

    def get_ids_short(self):
        return [int(u.id_str) for u in self.users if len(u.id_str) < 18]

    def get_ids_long(self):
        return [int(u.id_str) for u in self.users if len(u.id_str) == 18]

    def get_ids_len(self):
        return [len(u.id_str) for u in self.users]

    def get_id_ranges(self):
        s = self.get_ids_short()
        l = self.get_ids_long()
        return [(min(s), max(s)), (min(l), max(l))] if self.long_ids else [(min(s), max(s))]

    def get_num_followers(self):
        return [int(u.followers_count) for u in self.users]

    def get_num_tweets(self):
        return [int(u.statuses_count) for u in self.users]


if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API
    streamObj = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, streamObj)

    # This line filter tweets from the words.
    stream.sample()

    np.save('stream_users_followers'+RUN, streamObj.users.get_num_followers())
    np.save('stream_users_tweets' + RUN, streamObj.users.get_num_tweets())
    np.save('stream_users_ids'+RUN, streamObj.users.get_ids())

    api = API(auth)

    rest_users = Users()

    reqs = 0

    while rest_users.size() <= SIZE:
        reqs += 1
        if reqs % 10 == 0:
            print(rest_users.size())
        try:
            res = api.lookup_users(user_ids=streamObj.users.get_random_ids())
            print(len(res))
            rest_users.add(res)
        except RateLimitError:
            print('rate')
            time.sleep(15*60)

    print(rest_users.size())

    np.save('rest_users_followers'+RUN, rest_users.get_num_followers())
    np.save('rest_users_tweets' + RUN, rest_users.get_num_tweets())
    np.save('rest_users_ids'+RUN, rest_users.get_ids())

