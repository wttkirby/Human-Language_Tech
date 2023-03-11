# Wyatt Kirby
# IRK180000
# Cs 4395.001
# WebCrawler
# Importing what is needed
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import pickle


# This function creates the dictionary of all the words used in the files. The words used are the keys and their
# frequency is the item in the dictionary.
def dictmaker(readfiles, stop):
    crawler_dict = {}
    crawler_lines = []
    all_tokens = []
    for filen in readfiles:
        with open(filen, 'r', encoding='utf-8') as rfile:
            text_read = rfile.read()
            rfile.close()
        text_read = text_read.splitlines()
        for line in text_read:
            crawler_lines.append(line)
    for line in crawler_lines:
        text = re.sub(r'[.|?°©—!,:___\”;…•×–\“&™*\’<>=^@/$#\'%+()\-\n\d]', '', line.lower())  # only using the words and turning them all lowercase
        text = re.sub('\'\'', '', text)
        toke = word_tokenize(text)
        tokens = [t for t in toke if t not in stop and t.isalpha() and len(t) > 3]
        all_tokens += tokens
    set_all_tokes = set(all_tokens)
    crawler_dict = {x: all_tokens.count(x) for x in set_all_tokes}
    # This returns both all of the lines from all of the files as well as the generated dictionary as both are needed in
    # other functions
    return crawler_dict, crawler_lines


# This outputs the 25 most frequently used terms
def importantTerm(use_dict):
    use_dict = sorted(use_dict.items(), key =lambda k: k[1], reverse=True)
    count = 0
    for item in use_dict:
        if count < 25:
            print(item)
        else:
            break


# This finds the sentences that contain one of the 10 terms I defined
def findSent(term, all_lines):
    important_sent = []
    for line in all_lines:
        if term in line:
            important_sent.append(line)
    return important_sent


if __name__ == '__main__':
    # Get the stopwords so that we can remove them from the sentences
    stopwords = stopwords.words('english')

    # This gets all of the file names used for the files containing the scraped files.
    with open('filename2.txt', 'r', encoding='utf-8') as rfile:
        file_names = rfile.read()
        rfile.close()

    # Putting the file names in a list, splitting by the line as each filename separated from the others in its own line
    file_names = file_names.splitlines()
    nano_dict, nano_line = dictmaker(file_names, stopwords)
    importantTerm(nano_dict)
    important_terms = ['future', 'technology', 'healthcare', 'improve', 'issue', 'poverty', 'horizon',
                       'federal', 'concerns', 'malpractice', 'complications']
    info_dict = {}
    # This is creating the knowledge base needed for the chatbot being created later
    for term in important_terms:
        info_dict[term] = findSent(term, nano_line)

    pickle.dump(info_dict, open('nano.pickle', 'wb'))

