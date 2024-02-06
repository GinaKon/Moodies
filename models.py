from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movies(db.Model):
    __tablename__ = "movies"
    Movie_id = db.Column(db.String(70), primary_key=True, unique=True)
    Movie_Title = db.Column(db.String(70))
    Genre = db.Column(db.String(100))
    Director = db.Column(db.String(50))
    Rating = db.Column(db.Integer)
    moods = db.relationship('MoveMood', cascade = "all, delete")


class MoveMood(db.Model):
    __tablename__ = "movemood"
    id = db.Column(db.String(70), primary_key=True, unique=True)
    movie_id = db.Column(db.String(70), db.ForeignKey("movies.Movie_id"))
    mood_id = db.Column(db.String(70), db.ForeignKey("moods.mood_id"))
    

class Mood(db.Model):
    __tablename__ = "moods"
    mood_id = db.Column(db.String(70), primary_key=True, unique=True)
    name = db.Column(db.String(70))
    Movies= db.relationship('MoveMood', cascade = "all, delete")


    def serialize(self):
        return {

            'id':self.id,
            'name': self.mood
        }
    


