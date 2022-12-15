### Ary Suri ahs8gup, Brian Yoon byy2yt
import nltk 
nltk.download('punkt')
from nltk import word_tokenize,sent_tokenize

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
#read more on the steamer https://towardsdatascience.com/stemming-lemmatization-what-ba782b7c0bd8
import numpy as np 
import tflearn 
import tensorflow as tf
import random
import json
import pickle
import pymongo
import re
#MONGODB VARIABLES
host_name = "localhost"
port = "27017"

atlas_cluster_name = "sandbox"
atlas_default_dbname = "local"

conn_str = {
    "local" : f"mongodb://{host_name}:{port}/",
}

client = pymongo.MongoClient(conn_str["local"])


db = client["netflix_database"]
movieShowData = db['MovieShowData']
credits = db['Credits']
titles = db['Titles']


with open("intents.json") as file:
    data = json.load(file)



try:
    with open("data.picklefadfdasfdsaf","rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)



net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)


def chat():
    print("Start talking with the bot! (type quit to stop)")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        elif inp.lower() == "help":
            print("Here are examples of questions you can ask me: ") 
            for intent in data["intents"]:
                if intent["patterns"][0] != "Hi" and intent["patterns"][0] != "cya":
                    print(intent["patterns"][0])
        result = model.predict([bag_of_words(inp, words)])
        result_index = np.argmax(result)
        tag = labels[result_index]
        
        '''
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
        '''
        if tag == "Top Movie in Year Question":
            year =  re.search(r"(\d{4})", inp)
            if year:
                year = year.group(0)
                for x in movieShowData.find({"RELEASE_YEAR": int(year)}):
                    print(x['MOVIE_TITLE'])
                    
            else:
                print("No year given, try asking the question again")
            
        elif tag == "Top Show in Year Question":
            year =  re.search(r"(\d{4})", inp)
            if year:
                year = year.group(0)
                for x in movieShowData.find({"RELEASE_YEAR": int(year)}):
                    print(x['SHOW_TITLE'])
                    
            else:
                print("No year given, try asking the question again")
            
        elif tag == "Actors in Top Movie in Year Question":
            year =  re.search(r"(\d{4})", inp)
            if year:
                year = year.group(0)
                for x in movieShowData.find({"RELEASE_YEAR": int(year)}):
                    title = x['MOVIE_TITLE']

                for y in titles.find({"title": title}):
                    id = y["id"]
                for z in credits.find({"id": id}):
                    if z["role"] == "ACTOR":
                        print(z['name'])
            else:
                print("No year given, try asking the question again")
        elif tag == "Actors in Top Show in Year Question":
            year =  re.search(r"(\d{4})", inp)
            if year:
                year = year.group(0)
                for x in movieShowData.find({"RELEASE_YEAR": int(year)}):
                    title = x['SHOW_TITLE']

                for y in titles.find({"title": title}):
                    id = y["id"]
                for z in credits.find({"id": id}):
                    if z["role"] == "ACTOR":
                        print(z['name'])
            else:
                print("No year given, try asking the question again")
        elif tag == "Director in Top Movie in Year Question":
            year =  re.search(r"(\d{4})", inp)
            if year:
                year = year.group(0)
                for x in movieShowData.find({"RELEASE_YEAR": int(year)}):
                    title = x['MOVIE_TITLE']

                for y in titles.find({"title": title}):
                    id = y["id"]
                for z in credits.find({"id": id}):
                    if z["role"] == "DIRECTOR":
                        print(z['name'])
            else:
                print("No year given, try asking the question again") 
        elif tag == "Director in Top Show in Year Question":
            year =  re.search(r"(\d{4})", inp)
            if year:
                year = year.group(0)
                for x in movieShowData.find({"RELEASE_YEAR": int(year)}):
                    title = x['SHOW_TITLE']

                for y in titles.find({"title": title}):
                    id = y["id"]
                for z in credits.find({"id": id}):
                    if z["role"] == "DIRECTOR":
                        print(z['name'])
            else:
                print("No year given, try asking the question again") 
        elif tag == "Average Seasons of Top Show":
            seasons = []
            for x in movieShowData.find():
                for y in titles.find({"title": x["SHOW_TITLE"]}):
                    seasons.append(y["seasons"])
            print(round(np.mean(seasons)))
        elif tag == "Top rated movie from all years":
            top_movie = ""
            top_rating = 0
            for x in movieShowData.find():
                if x["MOVIE_SCORE"] > top_rating:
                    top_movie = x['MOVIE_TITLE']
                    top_rating = x['MOVIE_SCORE']
            print(top_movie)
            print("Rating: " + str(top_rating))
        elif tag == "Genre of Top Show in Year":
            year =  re.search(r"(\d{4})", inp)
            if year:
                year = year.group(0)
                for x in movieShowData.find({"RELEASE_YEAR": int(year)}):
                    print(x['SHOW_MAIN_GENRE'])

            else:
                print("No year given, try asking the question again")
        elif tag == "Genre of Top Movie in Year":
            year =  re.search(r"(\d{4})", inp)
            if year:
                year = year.group(0)
                for x in movieShowData.find({"RELEASE_YEAR": int(year)}):
                    print(x['MOVIE_MAIN_GENRE'])
                    break
            else:
                print("No year given, try asking the question again")

        else:
            print("I didnt get that. Try again")
chat()
