# Wyatt Kirby
# CS 4395.001
# Portfolio Component 2: Word Guessing Game
import sys
import re
import random
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# this is the function used to process the rawtext data as needed
def preprocess(rawtext):
    text = re.sub(r'[.?!,:;()\-\n\d]', ' ', rawtext.lower())  # only using the words and turning them all lowercase
    toke = word_tokenize(text)  # tokenizing
    stop = stopwords.words('english')  # getting the necessary stop words
    tokens = [t for t in toke if t not in stop and len(t) > 5]  # removing stop words and words that are shorted than 5
    # characters
    wnl = WordNetLemmatizer()
    lemmon = [wnl.lemmatize(t) for t in tokens]
    lemmon = set(lemmon)
    tag = nltk.pos_tag(lemmon)
    i = 0
    print('\nFirst 20 tagged:')
    for token in tag:
        if i < 20:
            print(token)
            i += 1
        else:
            continue
    nouns = []
    for token, pos in tag:
        if pos.startswith('N'):
            nouns.append(token)
    print('\nNumber of tokens: ', len(tokens), '\nNumber of nouns: ', len(nouns), '\n')
    return tokens, nouns

#this is the guessing game
def game(wordlist):
    points = 5
    print('\n_____\n Starting Guessing Game\n_____', '\n Game will end when you have negative points or you enter !')
    num = random.randint(0, 49) #choosing a word
    word = wordlist[num]
    num = len(word)
    i = 0
    dash = ''
    #this makes the correct number of dashes for the word chosen
    while i < num:
        dash += '_'
        i += 1
    print(word, dash)
    guess = ''
    #game will continue as long as there are positive points and the user hasn't entered a !
    while points >= 0 and guess != '!':
        print('Number of Points: ', points, '\n', dash)
        guess = input('Guess: ')
        numin = word.count(guess)
        if numin > 0:
            j = 0
            while j < numin:
                pos = word.find(guess)
                w = list(word)
                d = list(dash)
                w[pos] = ' '
                d[pos] = guess
                word = ''.join(w)
                dash = ''.join(d)
                points += 1
                print('Right')
                num -= 1
                j += 1
        elif guess != '!':
            points -= 1
            print('Sorry.')
        if num == 0:
            print('You solved it!\nCurrent Score: ', points)
            num = random.randint(0, 49)
            word = wordlist[num]
            num = len(word)
            i = 0
            dash = ''
            while i < num:
                dash += '_'
                i += 1
            print(word, dash)

    print("Final Score: ", points)


def main():
    #makes sure the file is given when running program
    if len(sys.argv) < 2:
        print('Please enter a file name as a sys arg')
    else:
        fp = sys.argv[1]
        file = open(fp, 'r')
        text = file.read()
        file.close()
        tokens = word_tokenize(text)
        unique = 0
        words = []
        totalw = 0
        for word in tokens:
            totalw += 1
            if words.count(word) == 0:
                words.append(word)
                unique += 1
        lexical = unique / totalw #calculating the lexical diversity of the program
        print('The lexical diversity of the file is: ', lexical)
        tokens, nouns = preprocess(text) #getting the nouns from the document
        nouncommon = {}
        for n in nouns:
            nouncommon[n] = tokens.count(n)
        sortednouns = sorted(nouncommon.items(), key=lambda x: x[1], reverse=True)
        gamewords = []
        i = 0
        print("50 most common words and the number of times used:")
        for w, num in sortednouns:
            if i < 50:
                print(sortednouns[i])
                gamewords.append(w)
                i += 1
            else:
                continue
        game(gamewords)


main()
