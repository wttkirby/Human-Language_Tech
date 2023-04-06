
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from profanity import profanity
from nltk.corpus import wordnet as wn
import random
import os
import pickle


# This is a class for the users to hold basic information on them.
class UserPerson:
    def __init__(self, name: str):
        self.user_name = name
        self.score = 150
        self.warning = False  # This is to let the chatbot know if it had warned the user about a particularly
        # disturbing scene in the movie
        self.seen_movie = False
        self.liked_movie = True
        self.trivia = []  # Holds the elements trivia qs that have been given to user
        self.ratings = []  # Holds the ratings that have been shown to user
        self.likes = []  # Holds portions of the movie that the viewer liked
        self.dislikes = []  # Holds portions of the movie that the viewer didn't like

    def addScore(self, num: int):
        self.score += num

    def subScore(self, num: int):
        self.score -= num


# This is a function used to update and add new users to the file. If none were needed then this won't be called.
def add_user(names_list):
    with open('users.txt', 'w', encoding='utf-8') as wfile:
        for name in names_list:
            wfile.write(str(name) + '\n')
        wfile.close()


# This opens any files associated with a previous user
def user_get(name):
    filename = str(name) + '.p'
    user = pickle.load(open(filename, 'rb'))
    return user


# This saves the current object into a pickle for later use
def save_info(user: UserPerson):
    filename = str(user.user_name) + '.p'
    pickle.dump(user, open(filename, 'wb'))


# This function essentially greets the user (similar to what the title says). Basically, it greets the user and deals
# with creating a user profile and saving it, or recovering the one from the last time a user spoke to the chatbot.
# It also accounts for users accidentally trying to use the same name as another user, in case two people have the same
# name.
def greet_user():
    greeting = ["Hi! Nice to meet you! What's your name?\n", "\'Sup dude! Can you enter your name really quickly?\n",
                "Beep, Boop. Enter your name.\n", "Howdy Partner! Mind entering your name?\n"]
    user_name = input(random.choice(greeting))
    all_names = []
    used_name = False
    if os.path.isfile('./users.txt'):
        with open('users.txt', 'r', encoding='utf-8') as rfile:
            all_names = rfile.read()
            all_names = all_names.splitlines()
            rfile.close()
        if user_name in all_names:
            used_name = True
        else:
            all_names.append(user_name)
    else:
        all_names.append(user_name)
    if used_name:
        while True:
            returning_user = input("This name has been used. Just to make sure, we've talked before right? (Enter \'T\'"
                                   "or \'F\')\n")
            if returning_user == "T":
                returning_user_mid = ["Oh hey nice to see you again!", "'Sup dude!", "Glad to see you back!"]
                returning_user_low = ["Oh... good to see you.", "Cool. Did you fix your attitude yet? Actually I don't "
                                                                "care...",
                                      "God really? Gross.", "Well my day's been shot."]
                returning_user_high = ["HI!!!! I missed you.", "Oh good! Wanna keep talking about Llamageddon?",
                                       "Oh. My. God. My day has been made."]
                curr_user = user_get(user_name)
                if curr_user.score < 75:
                    print(random.choice(returning_user_low))
                elif curr_user.score < 200:
                    print(random.choice(returning_user_mid))
                else:
                    print(random.choice(returning_user_high))
                break
            elif returning_user == "F":
                while user_name in all_names:
                    user_name = input("Oops! Enter a new name please! The one you entered has already been used.\n")
                print("Thanks!")
                used_name = False
                all_names.append(user_name)
                break
    if not used_name:
        curr_user = UserPerson(user_name)
        save_info(curr_user)
        new_user = ["Hah, noob. Nice to meet you. My name is Llouie", "AH! I don't think we've met. I'm Llouie.",
                    "Fresh blood... I'm Llouie."]
        print(random.choice(new_user))
        add_user(all_names)
    return curr_user


# This is how I decide if the tone a person is using when talking to the chatbot is nice and affect the score
def userAtt(s, user: UserPerson):
    sentiment_finder = SentimentIntensityAnalyzer()
    score = sentiment_finder.polarity_scores(s)["compound"]
    score = score * 10
    user.addScore(score)
    uhoh = profanity.contains_profanity(s)
    if uhoh:
        user.addScore(-25)
    save_info(user)


if __name__ == '__main__':
    print("--LLAMAGEDDON CHATBOT--\n")
    user = greet_user()
    response = input('')
    userAtt(response, user)
    print(str(user.score))
