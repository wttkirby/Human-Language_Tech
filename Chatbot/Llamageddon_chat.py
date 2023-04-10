# Wyatt Kirby
# IRK180000
# CS 4395.001
# Portfolio Component: Chatbot


import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from profanity import profanity
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
import random
import os
import pickle

negating_terms = ['don\'t', 'no', 'not', 'nah']
pos_terms = ['sure', 'yes', 'of course']
leave_terms = ['goodbye', 'good bye', 'bye', 'have a good one']
repeat_terms = ['again', 'another', 'one more', 'time to go']

# This is a class for the users to hold basic information on them.
class UserPerson:
    def __init__(self, name: str):
        self.user_name = name
        self.score = 150
        self.warning = False  # This is to let the chatbot know if it had warned the user about a particularly
        # disturbing scene in the movie
        self.seen_movie = False
        self.liked_movie = ''
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


# This function reads the input from a user and evaluates how positive or negative it is and penalizes users for cursing
# when being generally negative (when they are more likely to be cursing at the chatbot itself).
def scored_input(user: UserPerson, input_prompt, movie):
    s = input(input_prompt)
    if len(s) > 1:
        sentiment_finder = SentimentIntensityAnalyzer()
        score = sentiment_finder.polarity_scores(s)["compound"]
        tokens = nltk.word_tokenize(s)
        after_tagging = nltk.pos_tag(tokens)
        score = score * 10
        user.addScore(score)
        uhoh = profanity.contains_profanity(s)
        if uhoh and score <= 0:
            user.addScore(-25)
            save_info(user)

        if score <= -.5:
            num = 0
            for tag in after_tagging:
                string_part, part_speech = tag
                if part_speech.startswith('N'):
                    if string_part not in user.dislikes:
                        user.dislikes.append(string_part)
                    if string_part in user.likes:
                        user.likes.remove(string_part)
                num += 1
            if movie:
                user.liked_movie = False
                user.subScore(100)
        elif score >= .5:
            num = 0
            for tag in after_tagging:
                string_part, part_speech = tag
                if part_speech.startswith('N'):
                    user.likes.append(string_part)
                num += 1
            if movie:
                user.liked_movie = True
                user.addScore(100)
        elif movie:
            user.liked_movie = 'meh'
    return s.lower()


# This function adds a user's opinion of the movie after watching it to the ratings.txt file so that it can continue
# to grow as more and more people watch the movie.
def addRating(rating_input):
    with open('llama_ratings.txt', 'r', encoding='utf-8') as rfile:
        ratings = rfile.read()
        ratings = ratings.splitlines()
        ratings.append(rating_input)
        rfile.close()
        with open('llama_ratings.txt', 'w', encoding='utf-8') as wfile:
            for rating in ratings:
                wfile.write(str(rating) + '\n')


# This function opens the trivia file and outputs a fact to the user. It will only show each fact once.
def trivia_game(user:UserPerson):
    user_seen = user.trivia
    with open('llama_trivia.txt', 'r', encoding='utf-8') as rfile:
        trivia = rfile.read()
        trivia = trivia.splitlines()
        rfile.close()
    user_seen, trivia = [seen for seen in user_seen if seen not in trivia], [fact for fact in trivia if fact not in user_seen]
    if trivia:
        choice = random.choice(trivia)
        user.trivia.append(str(choice))
        print(choice)
    else:
        print("Seems like you've seen all of the Trivia currently available!\n")


# This function will show a user the ratings scrapped from the internet as well as those given by past users.
def ratings_game(user:UserPerson):
    user_seen = user.ratings
    with open('llama_ratings.txt', 'r', encoding='utf-8') as rfile:
        ratings = rfile.read()
        ratings = ratings.splitlines()
        rfile.close()
    user_seen, ratings = [seen for seen in user_seen if seen not in ratings], [rate for rate in ratings if rate not in user_seen]
    if ratings:
        choice = random.choice(ratings)
        user.ratings.append(str(choice))
        print(choice)
    else:
        print("Seems like you've seen all of the Ratings currently available! There will be more when more "
              "users watch the movie.\n")


# This is where the chatbot will converse with a person. It'll show trivia, ratings, and attempt at conversing with
# users (to the best of my ability now).
def general_chat(user: UserPerson):
    did_trivia = False
    did_rating = False
    initial_response = 'Alrighty so, this is a chatbot for a true masterpiece. One of the greatest movies I have\n' \
                       'ever had the chance to experience: LLamageddon. There are a couple things we can do from here' \
                       ':\n we can just generally chat about the movie, you can ask about trivia, or you can ask for' \
                       '\nratings. As we chat be mindful of the tone you use. I am fairly opinionated and fairly \n' \
                       'childish so if I get too mad there\'s really no telling what might happen. I also really\n' \
                       'care about this film, so being too critical will also rub me the wrong way.\n'
    print(initial_response)
    if not user.seen_movie:
        user_response = scored_input(user, 'It seems like you\'ve never had the chance to see LLamageddon! I can '
                                           'totally give you a synopsis if you\'d like!\nI do have to say there is a '
                                           'portion of the movie I would like to warn you about though before you '
                                           'watch it.\n', False)
        if not [ele for ele in negating_terms if(ele in user_response)] and 'synopsis' in user_response or 'summary' in user_response or [ele for ele in pos_terms if(ele in user_response)]:
            user_response = scored_input(user,
                                         'When a killer llama from outerspace crash lands in a rural town, a college '
                                         'student\'s party turns\n'
                                         'to bloodshed. Giving away anything more than this would be a crime, though '
                                         'I will say there is a\n'
                                         'particularly disturbing scene that I could warn you about if you\'d like.\n',
                                         False)
            if not [ele for ele in negating_terms if(ele in user_response)]:
                print('Near the end of the movie, one of the main cast is changed into a llama and proceeds to lay\n '
                      'Llama eggs for like WAY too long. The special effects are really good too, which makes it that\n'
                      'much worse to watch. The actor has a stellar performance as well. The horror elements in the\n '
                      'movie definitely build but this scene takes the cake and is absolutely horrifying.\n'
                      '\nWhat\'d you like to talk about?\n')
                user.warning = True
            else:
                print('Got it! How else can I help you!')
        elif 'seen' in user_response:
            user_response = scored_input(user, 'Oh nice! What\'d you think?', True)
            user.seen_movie = True
            addRating(user_response)
            user.ratings.append(str(user_response))
            print('Thanks! How else can I help you?')
        else:
            print('Okay! What\'d you like to talk about.')
    while True:
        user_response = scored_input(user, '', False)
        if user.score > 0:
            if 'trivia' in user_response and not [ele for ele in negating_terms if(ele in user_response)]:
                did_rating = False
                did_trivia = True
                trivia_game(user)
                print('Would you like another?')
            elif did_trivia and ([ele for ele in repeat_terms if(ele in user_response)] or [ele for ele in pos_terms if(ele in user_response)]):
                trivia_game(user)
                print('Would you like another?')
            elif ('trivia' in user_response and [ele for ele in negating_terms if(ele in user_response)]) or (did_trivia and [ele for ele in negating_terms if(ele in user_response)]):
                print('Got it! Is there anything else you\'d like to talk about?')
                did_trivia = False
            elif 'ratings' in user_response and not [ele for ele in negating_terms if(ele in user_response)]:
                did_rating = True
                did_trivia = False
                ratings_game(user)
                print('Would you like another?\n')
            elif did_rating and ([ele for ele in repeat_terms if(ele in user_response)] or [ele for ele in pos_terms if(ele in user_response)]):
                ratings_game(user)
                print('Would you like another?\n')
            elif ('ratings' in user_response and [ele for ele in negating_terms if(ele in user_response)]) or (did_trivia and [ele for ele in negating_terms if(ele in user_response)]):
                print('Got it! Is there anything else you\'d like to talk about?')
                did_rating = False
            elif ' spit ' in user_response:
                print('Howie Dewin talked about how he will never forget the taste of llama spit, so it seems like '
                      'Louie definitely spat everwhere.\nI genuinely feel bad for those who were spat on.')
            elif 'animal cruelty' in user_response:
                print('Louie was given plenty of breaks and was never forced to do a scene he didn\'t want '
                      'to.\nThat\'s why most of his scenes are just him walking ( usually lured with treats I assmume'
                      ' ).')
            elif 'special effects' in user_response or 'practical effects' in user_response or 'movie effects' in user_response:
                print('I love the special effects in this movie. Some of them are so good while others remain so '
                      'cheesy.\nI don\'t think I need to say the Louie does not, infact, shoot lasers out of his '
                      'eyes.\n Some of the practical effects were mildly dangerous ( specifically the explosions '
                      'during the chase sequence ), but even then the safety of everyone involded was the main '
                      'priority of the director.\nThe heart and egg scene really take the cake, though, '
                      'and were genuinely impressive effects amongst the more jokey effects.')
            elif 'favorite' in user_response:
                if 'scene' in user_response:
                    print('My favorite scene is when Shaddy stares at the scene with a glass piece in his hand for a '
                          'full minute. It always makes me go insane.')
                elif 'effect' in user_response:
                    print('I really love the effects from fourth and fifth deaths. So cheesy. So bad.')
                elif 'joke' in user_response or 'gag' in user_response:
                    print('I really love when Dan changes his shirt to a startrek shirt during his inspirational '
                          'speech.')
            elif [ele for ele in negating_terms if(ele in user_response)] and 'like' in user_response:
                    print('I really didn\'t like the egg scene. The horror elements in the movie definitely build to '
                          'that\nscene, but the actor\'s performance combined with the sudden quality of the '
                          'practical effects really make the scene that much more horrifying.\nIt makes me deeply '
                          'uncomfortable, despite the quality of the scene ( as it is meant to do ).')
            elif 'bad movies' in user_response:
                print('I really love horrible movies. The worse a movie is, the more charm and the funnier I find '
                      'them.\nOut of all, Llamageddon takes the cake for me. I love sci-fi and the movie is genuinely '
                      'hilarious.')
            elif [ele for ele in leave_terms if(ele in user_response)]:
                print('Okay! Have a good one!')
                save_info(user)
                break
            else:
                print('Hi! I\'m unsure exactly what you want to talk about unfortunately. If you\'d like to end our '
                      'conversation, simply say goodbye!')
        else:
            print('Dude you\'ve been so rude to me since you started talking to me. I think it\'s time for a fresh\n'
                  'start. As of now, your user file is being deleted. Fix the attitude or get better movie opinions.')
            name = user.user_name
            filename = str(name) + '.p'
            os.remove(filename)
            break


if __name__ == '__main__':
    print("--LLAMAGEDDON CHATBOT--\n")
    user = greet_user()
    general_chat(user)