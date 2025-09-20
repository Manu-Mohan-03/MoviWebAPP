from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    movie = db.relationship("Movie", back_populates='user')


class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50))
    year = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
    # nullable=False)
    poster_url = db.Column(db.String)

    user = db.relationship("User_Movie", back_populates='movie')

class User_Movie(db.Model):
    __tablename__ = 'user_movies'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        primary_key=True, nullable= False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'),
                         primary_key=True,  nullable= False)
    movie_title = db.Column(db.String(50), nullable=False)

    user = db.relationship("User", back_populates='link')
    movie = db.relationship("Movie", back_populates='link')

