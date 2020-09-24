"""
Logan Curd
logan.r.curd@vanderbilt.edu
09/25/2020
TweetGame.py - guess tweets from two users
Change++ Application

Notes: I could not get the endpoint to return 3200 tweets for each handle,
       but it does return enough to play the game

To Run: Should just be able to type py TweetGame.py into the terminal - at least for Windows
"""

import requests
import random
import sys

# Global Vars
INCLUDE_RTS = "false"
TWEET_RETURN_COUNT = '3200'
BEARER_TOKEN = \
    'AAAAAAAAAAAAAAAAAAAAABkxHwEAAAAAKjt2fpGK4jcPceLPZQFopReK4HA%3DweHzQwUw9w6afoMXOopKZ5x1GsZiGSueNc2QyeJ1F11oIiTBBc'
AT_STRING = '@'
RETWEET_STRING = 'https://t.co/'
URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"


class Tweet:

    # Constructor: creates a tweet object using the twitter handle and message from each tweet
    # params: message = tweet text, handle = username of person who tweeted
    def __init__(self, message, handle):
        self.message = message
        self.handle = handle


class TweetGame:

    # Constructor: takes two twitter handles and creates a tweet object (self.tweets)
    # params: two twitter handles to be used in API calls
    def __init__(self, handle1, handle2):
        self.handle1 = handle1
        self.handle2 = handle2
        self.tweets = self.add_tweets()
        self.score = 0
        self.streak = 0
        self.rounds_played = 0

    # add_tweets(): gets tweets from both handles and combines them into one tweet list
    # return: tweets list of Tweet objects containing valid tweets
    def add_tweets(self):
        tweets = []

        if self.handle1 == self.handle2:
            sys.exit("Error: handles can not be the same")

        self.get_tweets(self.handle1, tweets)
        self.get_tweets(self.handle2, tweets)

        return tweets

    # get_tweets(): performs API call for handle and finds valid tweets to append into tweet_list
    # params: handle = twitter handle of user, tweet_list = list to append Tweet objects to
    def get_tweets(self, handle, tweet_list):

        params = {'screen_name': handle, 'include_rts': INCLUDE_RTS, 'count': TWEET_RETURN_COUNT}
        header = {'authorization': 'Bearer ' + BEARER_TOKEN}

        response = requests.get(URL, params=params, headers=header)  # GET request

        if response.status_code != 200:  # If API call did not work for this handle
            sys.exit(f"API call unsuccessful. Twitter handle \'{handle}\' may be invalid.")

        for x in response.json():
            tweet_string = x['text']
            if AT_STRING not in tweet_string and RETWEET_STRING not in tweet_string:  # If valid tweet
                tweet_list.append(Tweet(tweet_string, handle))

    # get_random_tweet(): returns and removes random Tweet object in self.tweets
    # return: random Tweet object
    def get_random_tweet(self):
        num_tweets = len(self.tweets)
        if num_tweets > 0:
            index = random.randint(0, num_tweets - 1)
            return self.tweets.pop(index)
        else:  # User has guessed all Tweet objects
            sys.exit("No more tweets remain - Game Over.\n"
                     f"You played {self.rounds_played} round(s) and had {self.score} correct answer(s)")

    # play_round(): handles one round of the game
    # (gets random tweet, prompts input, checks correctness, updates variables)
    def play_round(self):
        rand_tweet = self.get_random_tweet()
        print(rand_tweet.message)
        response = input(f"Who tweeted this? (  {self.handle1}  ) or (  {self.handle2}  )? ")
        if response == rand_tweet.handle:
            self.score += 1
            self.streak += 1
            print("Correct")
            if self.streak >= 3:
                print(f"That makes {self.streak} in a row!")
        else:
            self.streak = 0
            print("Incorrect: This was tweeted by", rand_tweet.handle)

        self.rounds_played += 1

    # play_again(): prompts user to play again and takes input
    # return: bool indicating user response
    def play_again(self):
        response = input("Play again? (y/n) ")

        return response.lower() == 'y'

    # run(): acts as game loop; plays new round while play_again is true and gives final score when game is over
    def run(self):
        play_again = True

        while play_again:
            self.play_round()
            play_again = self.play_again()

        print("Game Over: You played ", self.rounds_played, " round(s) and had ", self.score, " correct answer(s)")


def main():
    print("Input two twitter handles (do not include \'@\' symbol)")
    handle1 = input("Input handle 1 (ex: kanyewest): ")
    handle2 = input("Input handle 2 (ex: elonmusk): ")
    game = TweetGame(handle1, handle2)

    # uncomment line below and comment lines above to play with only elon and kanye
    # game = TweetGame("kanyewest", "elonmusk")

    game.run()


if __name__ == "__main__":
    main()
