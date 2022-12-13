import requests, pgeocode,  pymongo, pprint, os
import pandas as pd

#MONGODB VARIABLES
host_name = "localhost"
port = "27017"

atlas_cluster_name = "sandbox"
atlas_default_dbname = "local"

conn_str = {
    "local" : f"mongodb://{host_name}:{port}/",
}

client = pymongo.MongoClient(conn_str["local"])

print(f"Local Connection String: {conn_str['local']}")



#Load all the data in 
bestMoviesByYear = pd.read_csv("Best Movie by Year Netflix.csv", header=0, index_col=0)
bestMovies = pd.read_csv("Best Movies Netflix.csv", header=0, index_col=0)
bestShowByYear = pd.read_csv("Best Show by Year Netflix.csv", header=0, index_col=0)
bestShows = pd.read_csv("Best Shows Netflix.csv", header=0, index_col=0)
rawCredits = pd.read_csv("raw_credits.csv", header=0, index_col=0)
rawTitles = pd.read_csv("raw_titles.csv", header=0, index_col=0)


#Transform data
bestMovieShowByYear = pd.merge(bestMoviesByYear, bestShowByYear, on='RELEASE_YEAR', how='inner')
bestMovieShowByYear = bestMovieShowByYear.rename(columns={"TITLE_x": "MOVIE_TITLE","SCORE_x": "MOVIE_SCORE", "MAIN_GENRE_x": "MOVIE_MAIN_GENRE", "MAIN_PRODUCTION_x": "MOVIE_MAIN_PRODUCTION"})
bestMovieShowByYear = bestMovieShowByYear.rename(columns={"TITLE_y": "SHOW_TITLE","SCORE_y": "SHOW_SCORE", "MAIN_GENRE_y": "SHOW_MAIN_GENRE", "MAIN_PRODUCTION_y": "SHOW_MAIN_PRODUCTION"})

#Load Data
db = client["netflix_database"]
movieShowData = db['MovieShowData']
credits = db['Credits']
titles = db['Titles']

movieShowData.insert_one({"index":"Sensex","data":bestMovieShowByYear.to_dict("records")})
credits.insert_one({"index":"Sensex","data":rawCredits.to_dict("records")})
titles.insert_one({"index":"Sensex","data":rawTitles.to_dict("records")})








