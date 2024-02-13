from flask import Flask, request, session, jsonify
from models import db, Movies, MoveMood, Mood
from config import Config
from sqlalchemy.sql import Select
from sqlalchemy.orm import aliased
from uuid import uuid4





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
    

@app.route('/movies', methods = ["POST"])
def create_movies():
  try:
    
    movie_title = request.json.get('movie_title')
    mvt = Movies.query.filter_by(Movie_Title = movie_title).first()
    if movie_title == None:
      return jsonify({'error': "Movie Title cannot be null or exists already"})
    if mvt is not None:
      return jsonify({'error': "You fucked up"})

    print(movie_title)
    genre = request.json.get('genre')
    print(genre)
    director = request.json.get('Director')
    print(director)
    rating = request.json.get('Rating')
    print(rating)

    new_id = uuid4().hex
    print(new_id)

    new_movie = Movies(Movie_id=new_id, Movie_Title=movie_title, Genre=genre, Director=director, Rating=rating)
    print(new_movie)

    db.session.add(new_movie)
    db.session.commit()
    print("confirmation")

    return jsonify(new_movie.serialize()),201
  except ValueError:
    return jsonify ({'error': 'Invalid request data'}), 400
  except Exception as e:
    return jsonify({'error':str(e)}), 500
  

# /movies/Wonka
@app.route('/movies/<movie_title>', methods=['DELETE'])
def delete_movie(movie_title):
  try:
    movtt = Movies.query.filter_by(Movie_Title=movie_title).first()
    print (f'you fucked up {movtt}')
    if movtt is None:
      print('hello')
      return jsonify ({"error": "Movie not found"}), 404
    

    db.session.delete(movtt)
    db.session.commit()
    print("confirmation")

    return jsonify({'message': 'Deleted succesfully'}),200
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  


@app.route('/movies/<movie_title>', methods=['PUT'])
def update_movie(movie_title):
  try:
     genre = request.json.get('genre')
     director = request.json.get('Director')
     rating = request.json.get('Rating')

     moovs = Movies.query.filter_by(Movie_Title=movie_title).first()
     if moovs is None:
       
       return jsonify({'error': 'Not good enough' })
  
     moovs.Genre = genre
     moovs.Director = director
     moovs.Rating = rating


     
     db.session.commit()

     return jsonify({'message': 'Succesful Update'}), 200
  except Exception as e:
    return jsonify({'error':str(e)})
    

   
    

   

    
if __name__ == '__main__' :
  app.run(debug=True, port=8080)
