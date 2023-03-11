# Human-Language_Tech
This is the git for my human language technologies class (CS 4395.001)

# Assignment 0: Overview of NLP
For this assignment I had to set up my github for the class and write a small [overview](Overview_of_NLP.pdf) of natural language processing.

# Assignment 1: Text Processing in Python
For this assignment I had to read in and process data from a .csv file in python. I had to make sure that everything was formatted correctly. To run it using the command prompt, navigate to the folder the file is in and type in **python Homework1_irk180000.py** followed by the location of the data. For me the full command looked like **python Homework1_irk180000.py Data\data.csv** but it may look different depending where you have the data located. I really liked processing text in python. It felt a lot easier than Java in my opinion, as the regex import made a lot of it easier. I had some difficulty figuring out how to iterate through the list so that I could make sure all the inputted data was correctly formatted but that was most likely due to my lack of experience in python, not by any fault of python itself. I was mostly overthinking it. I overall feel a lot more confident in python and my ability to figure out what I need to do to program in it. Overall, its an easy language to learn and it makes sense to me. This is the [program](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_1/Homework1_irk180000.py).

# Assignment 2: Word Guess Game
For this assignment I had to use NLTK to explore a text file and familiarize myself with the given tools. After using various tools imported from NLTK I made a simple word guessing [game](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_2/Homework2_IRK180000.py). To use the program it is similar to assignment one as you must go to the command prompt and write **python Homework2_IRK180000.py anat19.txt**, but should run normally after that point.

# Assignment 3: WordNet
For this assignment I had to explore WordNet, SentiWordNet, and collocation. This helped introduce new topics and was generally pretty interesting. I used various words in conjunction with the previously mentioned libraries and concepts to learn about how words are catagorized when processing them for use with computers and chatbots. This is the [pdf](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_3/Portfolio%20Component%203_%20Wordnet.pdf) of my notebook. If you would like to download the file and put in your own inputs look in this [folder](https://github.com/wttkirby/Human-Language_Tech/tree/main/Assignment_3).

# Assignment 4: Ngrams
For this assignment we read in training files for three languages (English, French, and Italian) and then, make unigrams and bigrams for each language, and then pickle them in this [file](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_4/Homework3_pt1.py). Then, in this [file](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_4/Homework3_pt2.py) I read in a test file and went line by line to try and figure out if each line was in a specific language. After that, the predictions were stored in a seperate file (found in the Assignment_4) folder. When running the files, the first one must be run before the second, and after completion of the second you can view the predictions in the file mentioned previously and the accuracy and the list of incorrect lines will be displayed. This is a [paper](https://github.com/wttkirby/Human-Language_Tech/blob/main/NGrams.docx) written about NGrams.

# Assignment 5: Parsing
For this assignment I created a sentence and parsed it in three different ways (PSG, Dependency Tree, SRL) and wrote a small paragraph on my thought of each n this [paper](https://github.com/wttkirby/Human-Language_Tech/blob/main/Parsing.pdf).

# Assignment 6: WebCrawler
## WebCrawler:
For this assignment I made a webcrawler for three different topics: [Frida Kahlo](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_6/scrapenprocess.py), [Nanotechnology](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_6/nanotech.py), and current [Transgender Legislation](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_6/transleg.py). These all find other urls based on an initial google search about the chosen topic. While we only needed to use one topic, I did three as I had a hard time finding one with enough useable links. If I was able to generate 15 links, only some of those links were able to be scraped due to anti-scraping bots. I had the most luck with useable links with the Transgender Legislation topic, getting 12 links that were able to be scraped.

## Reading Info and Outputting Terms
This file takes the information scraped from the generated files and outputs the most frequently used terms for the topics: [Frida Kahlo](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_6/readnterm.py), [Nanotech](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_6/nanoread.py), [Transgender Legislation](https://github.com/wttkirby/Human-Language_Tech/blob/main/Assignment_6/transread.py). It also pickles a dictionary of 10 terms I picked that I thought were integral to each topic. These dictionaries use the terms as keys and store each sentence that contains the term.

## File naming:
The files have a pretty easy naming convention: < Topic >_ File _< Link Number >.txt. This means that all of the information scraped for Frida Kahlo would be named like: Frida_File_[1...*].txt. The files named like this hold all of the information scraped from the urls found and had some general preprocessing done on them to seperate the sentences with a "\n".

The files named url['', 2, 3].txt hold all of the urls found by the webcrawler. This does include those that are not able to be scraped.

The files named filename['', 2, 3].txt hold the names of all of the files that hold information for a topic. This makes it easy to read in between the two files used for this webcrawler.