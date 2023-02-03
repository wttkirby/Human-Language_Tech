#Wyatt Kirby
#CS 4395.001
#Portfolio Component 1: Text Processing with Python

import sys
import os
import re
import pickle

#This is my person class to store all the information needed from the file
class Person:
    #this is how each object is initialized
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone
    #this is the function that shows all the person's info in an organized manner
    def display(self):
        print('Employee id: ', self.id)
        print('\t', self.first, ' ', self.mi, ' ', self.last)
        print('\t', self.phone)
        return ''

#this checks if the id found in the file is in the correct format
def idCheck(string):
    idCheck1 = re.search('[A-Z][A-Z][0-9][0-9][0-9][0-9]', string)
    idCheck2 = re.search('[a-z][a-z][0-9][0-9][0-9][0-9]', string)
    idCheck3 = re.search('[A-Z][a-z][0-9][0-9][0-9][0-9]', string)
    idCheck4 = re.search('[a-z][A-Z][0-9][0-9][0-9][0-9]', string)
    #if the given id is 2 letters (regardless of capitalization) followed by 4 numbers its good
    if idCheck1 or idCheck2 or idCheck3 or idCheck4:
        return string
    else: #gotta correct it
        print(string,'is incorrect format. ID should be 2 letters followed by 4 digits')
        newString = input('Please try again: ')
        string = idCheck(newString) #will continue looping until a correct one is given
        return string

#checks to see if the given phone number is in the correct format
def phoneCheck(string):
    phone = re.search('[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]', string)
    phone2 = re.search('[0-9][0-9][0-9] [0-9][0-9][0-9] [0-9][0-9][0-9][0-9]', string)
    phone3 = re.search('[0-9][0-9][0-9].[0-9][0-9][0-9].[0-9][0-9][0-9][0-9]', string)
    #returns the phone number if formatted correctly or fixes it and returns it
    if phone:
        return string
    elif phone2:
        string = string.replace(' ', '-')
        return string
    elif phone3:
        string = string.replace('.', '-')
        return string
    elif string.isdigit():
        new = string[0:3] + '-' + string[3:6] + '-' + string[6:]
        return new
    else:
        print('Phone ', string, ' is invalid.')
        print('Enter phone number in form 123-456-7890')
        newPhone = input('Enter phone number: ')
        phoneNum = phoneCheck(newPhone)
        return phoneNum

#reads the file and ensures that all input information is correct before returning info as a dictionary
def read(filePath):
    #opening the file
    with open(os.path.join(os.getcwd(), filePath), 'r') as f:
        next(f)
        text = f.read()
    data = re.split(',|\n', text) #making sure to separate the information correctly
    #correcting data if not in correct format
    for d in data:
        if d.isalpha():
            new = d.capitalize()
            i = data.index(d)
            data[i] = new
        elif d == '':
            i = data.index(d)
            data[i] = 'X'
        elif d.isalnum() and not d.isdigit():
            i = data.index(d)
            new = idCheck(d)
            data[i] = new
        else:
            i = data.index(d)
            new = phoneCheck(d)
            data[i] = new

    i = 0
    people = {}
    #puts the information in a person object and adds that to the dictionary
    while i<len(data):
        person = Person(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
        index = data[i+3]
        people[index] = person
        i += 5 #we know that there should be 5 pieces of info for each person so we can increment by five
    return people

if __name__ == "__main__":
    #making sure data file is given
    if len(sys.argv) < 2:
        print('Please enter a file name as a system arg')
    else:
        info = {}
        fp = sys.argv[1] #gets the filepath from user
        info = read(fp) #gets info

        #pickle time
        pickle.dump(info, open('info.p', 'wb'))
        pickledInfo = pickle.load(open('info.p','rb'))

        #printing data
        print('\nEmployee List:\n')

        for key in info:
           print(pickledInfo[key].display())

        print('Done')
