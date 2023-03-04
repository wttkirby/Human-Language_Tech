# Wyatt Kirby
# IRK180000
# CS 4395.001
# Portfolio Assignment 4: Ngrams pt.1

# Importing what is needed
import re
import nltk
from nltk import word_tokenize
from nltk import ngrams
import pickle


# This function reads the given file and processes it before returning a bigram ans unigrams list
def read(inputFile):
    # Opening and reading the file
    with open(inputFile, 'r', encoding="utf-8") as file:
        rawText = file.read()
    # taking out the newlines as requested
    text = re.sub(r'\n', '', rawText)
    # Tokenizing the text
    tokens = word_tokenize(text)
    bigrams = list(ngrams(tokens, 2))
    # making the dictionaries using Mazidi's examples
    unigramDict = {x: tokens.count(x) for x in set(tokens)}
    bigramsDict = {y: bigrams.count(y) for y in set(bigrams)}
    return(unigramDict, bigramsDict)


if __name__ == '__main__':
    inFile1 = 'LangId.train.English'
    inFile2 = 'LangId.train.French'
    inFile3 = 'LangId.train.Italian'
    # Reading in the requested files and processing it into unigram and bigram dictionaries
    uniDict1, biDict1 = read(inFile1)
    uniDict2, biDict2 = read(inFile2)
    uniDict3, biDict3 = read(inFile3)
    # Pickling the files so that they are available for the second file
    pickle.dump(uniDict1, open('uniEng.p', 'wb'))
    pickle.dump(uniDict2, open('uniFre.p', 'wb'))
    pickle.dump(uniDict3, open('uniIta.p', 'wb'))
    pickle.dump(biDict1, open('biEng.p', 'wb'))
    pickle.dump(biDict2, open('biFre.p', 'wb'))
    pickle.dump(biDict3, open('biIta.p', 'wb'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
