from flask import Flask, request, session
from models import db, Movies, MoveMood, Mood
from config import Config
from sqlalchemy.sql import Select
from sqlalchemy.orm import aliased





# class Movie:
#    def __init__(self, title, mood):
#       self.title = title
#       self.mood = mood

#    def get_choice(self, movie_title):
#       self.movie_title = movie_title

Moviesdict = [{'Title': 'Dogtooth','mood': "sceptical"},
      {'Title':'Eat, Pray, Love', 'mood':'romantic'},
   {'Title':'Joker', 'mood':'depressed'},
    {'Title':'Cruella', 'mood':'powerful'}
]

def MatchMood (inputmood):
   for item in Moviesdict:
    if  inputmood == (item['mood']):
      return (item['Title'])
   return "None"
   
   

# Dogtooth = Movie ("Dogtooth", "sceptical")
# EatPrayLove = Movie("Eat,Pray, Love", "romantic")
# Joker = Movie ("Joker", "depressed")
# Cruella = Movie ("Cruella", "powerful")
# CinemaParadiso = Movie ("Cinema Paradiso", "emotional")
# LaVitaeBella = Movie ("LaVita e Bella", "general")
# Gomorrah = Movie ("Gomorrah", "sadistic")
# Parasites = Movie ("Parasites", "analytical")
# OldBoy    = Movie ("Old Boy", "spicy")
# Elemental = Movie ("Elemental", "childish")


# Mood = input('How are you feeling today?')
# print(MatchMood(Mood.strip()))

app = Flask(__name__)
app.config.from_object(Config) #this is getting all the configuration that are needed to create the db
db.init_app(app) # this is creating the connection with the db

with app.app_context():
    db.create_all()  #this is creating the tables we defined in models.py



@app.route('/hello_movie', methods = ["GET"]) #www.google.com
def hello_movie():
   try:
     
    args = request.args
    mood = args.get('mood') 
    
           # SELECT Movie_Title
           # FROM movies 
           # INNER JOIN movemood AS movemood_1 ON movies.`Movie_id` = movemood_1.movie_id, moods 
           # INNER JOIN movemood AS movemood_2 ON moods.mood_id = movemood_2.mood_id
           # WHERE moods.name = 'sceptical'
           # AND movemood_1.id = movemood_2.id;
    
    movie_alias_1 = aliased(MoveMood)
    movie_alias_2 = aliased(MoveMood)
    movie = Select(Movies.Movie_Title).join(movie_alias_1, Movies.moods).join(movie_alias_2, Mood.Movies).where(Mood.name == mood).where(movie_alias_1.id == movie_alias_2.id)
    print(movie)
    print("annoying_pair_programming_4")
    mv = db.session.execute(movie).all()
    print(mv)
    return str(mv)
   
   except Exception as e:
    return str(e)
    
   
   

    
if __name__ == '__main__' :
  app.run(debug=True, port=8080)
