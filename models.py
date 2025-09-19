from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)


class User_Movie(db.Model):
    __tablename__ = 'user_movies'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable= False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'),
                         nullable= False)
