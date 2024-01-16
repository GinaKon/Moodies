from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

host="127.0.0.1"
user="root"
password = "G1nain3dinburgh!"
port = 3306
database="moodies"

def get_mysql_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            host, user, password, port, database
        )
       
    )

if __name__ == '__main__':
 
    try:
        engine = get_mysql_connection()
        print(
            f"Connection to the {host} for user {user} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

db = SQLAlchemy()

class Moovies(db.Model):
    __tablename__ = "movies"
    Movie_id = db.Column(db.String(36), primary_key=True, unique=True)
    Movie_Title = db.Column(db.String(70))
    Genre = db.Column(db.String(100))
    Director = db.Column(db.String(50))
    Rating = db.Column(db.Integer)
    moods = db.relationship('Mood', backref = 'movie')


class Mood(db.Model):
    __tablename__ = "moods"
    id = db.Column(db.String(50), primary_key=True, unique=True)
    name = db.Column(db.String(70))
    Movies= db.relationship('Moovies', cascade = "all")


    def serialize(self):
        return {

            'id':self.id,
            'name': self.mood
        }
    


