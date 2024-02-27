from flask import Flask, request, session, jsonify
from models import db, Movies, MoveMood, Mood
from config import Config
from sqlalchemy.sql import Select
from sqlalchemy.orm import aliased
from uuid import uuid4
   
   

app = Flask(__name__)
app.config.from_object(Config) #this is getting all the configuration that are needed to create the db
db.init_app(app) # this is creating the connection with the db

with app.app_context():
    db.create_all()  #this is creating the tables we defined in models.py

def add_movie_to_db(new_movie_title, new_genre, new_director, new_rating):
  new_id = uuid4().hex #Generating new id for the new movie

  new_movie = Movies(Movie_id=new_id, Movie_Title=new_movie_title, Genre=new_genre, Director=new_director, Rating=new_rating) # Creating the new movie and its dets

  db.session.add(new_movie) # Adding new movie in db
  db.session.commit() # Commit the changes in db
  return new_movie

def add_mood_to_db(new_mood_name):
  new_id = uuid4().hex

  new_mood = Mood(mood_id=new_id, name=new_mood_name)

  db.session.add(new_mood)
  db.session.commit()
  return new_mood


@app.route('/pick_movie', methods = ["GET"]) #creating first endpoint
def pick_movie():
   try:
     
    args = request.args # using the request object to get the args passed in the URL 
    mood = args.get('mood') # we are extracting the argument using the get method to get the associated value (movie) with the key 'mood'
    
           # SELECT Movie_Title
           # FROM movies 
           # INNER JOIN movemood AS movemood_1 ON movies.`Movie_id` = movemood_1.movie_id, moods 
           # INNER JOIN movemood AS movemood_2 ON moods.mood_id = movemood_2.mood_id
           # WHERE moods.name = 'sceptical'
           # AND movemood_1.id = movemood_2.id;
    
    movie_alias_1 = aliased(MoveMood)
    movie_alias_2 = aliased(MoveMood)
    movie = Select(Movies.Movie_Title).join(movie_alias_1, Movies.moods).join(movie_alias_2, Mood.Movies).where(Mood.name == mood).where(movie_alias_1.id == movie_alias_2.id)
    mv = db.session.execute(movie).all() #using "session" is for ORM functionalities, not RAW SQL, 
                                         # execute method passes through to whatever the session is bound to (the engine)
    return str(mv)
   
   except Exception as e:
    return str(e)
    

@app.route('/movies', methods = ["POST"])
def create_movies():
  try:
    
    movie_title = request.json.get('movie_title') #Getting the movie title (again)
    mvt = Movies.query.filter_by(Movie_Title = movie_title).first() #Searching in Movies table by filtering the titles
    if movie_title == None:
      return jsonify({'error': "Movie Title cannot be null"})
    if mvt is not None:
      return jsonify({'error': "Movie Title already exists"})

    genre = request.json.get('genre')
    director = request.json.get('Director')
    rating = request.json.get('Rating')

    new_movie =add_movie_to_db(new_movie_title=movie_title, new_director=director, new_genre=genre, new_rating=rating)
    return jsonify(new_movie.serialize()),201
  except Exception as e:
    return jsonify({'error':str(e)}), 500
  

# /movies/Wonka
@app.route('/movies/<movie_title>', methods=['DELETE'])
def delete_movie(movie_title):
  try:
    movtt = Movies.query.filter_by(Movie_Title=movie_title).first()
    if movtt is None:
      return jsonify ({"error": "Movie not found"}), 404
    

    db.session.delete(movtt) # deleting the movie
    db.session.commit() 

    return jsonify({'message': 'Deleted succesfully'}),200
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  


@app.route('/movies/<movie_title>', methods=['PUT']) # Updating movie and its dets
def update_movie(movie_title):
  try:
     genre = request.json.get('genre')
     director = request.json.get('Director')
     rating = request.json.get('Rating')

     moovs = Movies.query.filter_by(Movie_Title=movie_title).first()
     if moovs is None:
       
       return jsonify({'error': 'Movie does not exist.' })
  
     moovs.Genre = genre
     moovs.Director = director
     moovs.Rating = rating


     
     db.session.commit()

     return jsonify({'message': 'Succesful Update'}), 200
  except Exception as e:
    return jsonify({'error':str(e)})
    

@app.route('/moods', methods=['POST'])
def add_mood():
  try:
    mood_name = request.json.get('name')
    mdn = Mood.query.filter_by(name = mood_name).first()
    if mood_name == None:
      return jsonify({'error': "Mood cannot be null"})
    if mdn is not None:
      return jsonify({'error': "Mood already exists. Try a diferent one."})


    new_mood = add_mood_to_db(new_mood_name=mood_name)

    return jsonify(new_mood.serialize()),201
  except Exception as e:
    return jsonify({'error':str(e)}), 500
  

@app.route('/moods/<mood_name>', methods=['DELETE'])
def delete_mood(mood_name):
  try:
    moddlt = Mood.query.filter_by(name=mood_name).first()
    if moddlt is None:
      return jsonify ({"error": "Mood not found"}), 404
    

    db.session.delete(moddlt)
    db.session.commit()

    return jsonify({'message': 'Deleted succesfully'}),200
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  

@app.route('/fetch_movie', methods=['GET'])
def fetch_movie():
  
  try:
    args = request.args
    movie = args.get('movie')
    movied = Movies.query.filter_by(Movie_Title = movie).first()
    if movied is None:
      return jsonify({"error":"Movie not found"}), 404
    return jsonify(movied.serialize()),201
    
    
  except Exception as e:
    return jsonify({'error': 'Please try again'})
  


@app.route('/get_mood/<mood_name>', methods=['GET'])
def get_mood(mood_name):
  try:
    mooddet = Mood.query.filter_by(name=mood_name).first()
    if mooddet is None:
      return jsonify({'error': 'Mood not found'}), 404
    return jsonify(mooddet.serialize()), 201
    
  
  except Exception as e:
    return jsonify ({'error': 'Wrong. Again'})
  

@app.route('/movemood', methods=['POST'])
def create_moodmovie():
  try:

    movie_title = request.json.get('movie_title')
    mood_name = request.json.get('name')
    movied = Movies.query.filter_by(Movie_Title = movie_title).first()

    if movied is None:
      movied=add_movie_to_db(new_movie_title=movie_title, new_director=None, new_genre=None, new_rating=None )

    moddlt = Mood.query.filter_by(name=mood_name).first()
    if moddlt is None:
      mooddlt = add_mood_to_db(new_mood_name=mood_name)

    new_id = uuid4().hex

    new_movemood = MoveMood(id=new_id, mood_id=moddlt.mood_id, movie_id=movied.Movie_id)

    db.session.add(new_movemood)
    db.session.commit()

    return jsonify(new_movemood.serialize()),201
  except Exception as e:
    return jsonify({'error':str(e)}), 500




if __name__ == '__main__' :
  app.run(debug=True, port=8080)
