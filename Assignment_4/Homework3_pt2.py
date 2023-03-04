# Wyatt Kirby
# IRK180000
# CS 4395.001
# Portfolio Assignment 4: Ngrams pt.2

# Importing what is needed
import pickle
import nltk
from nltk import word_tokenize
from nltk import ngrams


# This is how I'm finding the probability of the line being a certain language
def langProb(text, uniDict, biDict, size):
    uniText = word_tokenize(text)  # unigram of line we want to predict
    biText = list(ngrams(uniText, 2))  # bigrams of line wee want to predict

    prob = 1

    for bi in biText:
        b = biDict[bi] if bi in biDict else 0
        u = uniDict[bi[0]] if bi[0] in uniDict else 0

        prob = prob * ((b + 1) / (u + size))

    return prob


if __name__ == '__main__':
    # Reading pickled files
    uniEng = pickle.load(open('uniEng.p', 'rb'))
    uniFre = pickle.load(open('uniFre.p', 'rb'))
    uniIta = pickle.load(open('uniIta.p', 'rb'))
    biEng = pickle.load(open('biEng.p', 'rb'))
    biFre = pickle.load(open('biFre.p', 'rb'))
    biIta = pickle.load(open('biIta.p', 'rb'))

    vocabLen = len(uniEng) + len(uniFre) + len(uniIta)

    # Reading in the test file
    with open('LangId.test', 'r', encoding="utf-8") as testFile:
        testLines = testFile.read().splitlines()

    correct = 0
    wrong = []
    # In this portion I'm writing my predictions to the file and counting the correct predictions and storing the
    # incorrect ones
    with open('LangId.pred', 'w', encoding="utf-8") as predFile:
        with open('LangId.sol', 'r', encoding="utf-8") as solFile:
            numLine = 0  # Starting at 0, so I can just use this as my line count
            # Looping through the lines in the test file
            for line in testLines:
                sol = solFile.readline()  # Getting the solution for the current line
                # Calculating probabilities of it being one language over another
                engProb = langProb(line, uniEng, biEng, vocabLen)
                freProb = langProb(line, uniFre, biFre, vocabLen)
                itaProb = langProb(line, uniIta, biIta, vocabLen)

                numLine += 1  # Incrementing the line num

                guess = ""  # Creating the prediction

                # Finding the language with the largest probability and creating a guess formatted similarly to the
                # solutions
                if engProb == max(engProb, freProb, itaProb):
                    guess = str(numLine) + " English\n"
                elif freProb == max(engProb, freProb, itaProb):
                    guess = str(numLine) + " French\n"
                elif itaProb == max(engProb, freProb, itaProb):
                    guess = str(numLine) + " Italian\n"

                predFile.write(guess)  # Writing the guess to the predictions file
                # Finding if the prediction was correct or not and storing what is needed
                if guess != sol:
                    wrong.append(numLine)
                else:
                    correct += 1

    accr = (correct / numLine) * 100

    print("The accuracy of the model is: ", accr, "%\n And the lines incorrect are: ", wrong)
