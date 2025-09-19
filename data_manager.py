from models import db, User, Movie, User_Movie

class DataManager:

    def __init__(self):
        pass

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        users = User.query.all()
        return users

    def get_movies(self, user_id):
        """movie_ids = User_Movie.query.filter_by(user_id = user_id).all()
        movies = []
        for movie_id in movie_ids:
            movie = Movie.query.filter_by(movie_id = movie_id)
            movies.append(movie)
        return movies"""
        movies = User_Movie.query.join(User_Movie.movie).filter_by(user_id=user_id)
        return movies


    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()


    def update_movie(self, movie_id, new_title):
        # Can also try edited_movies as dict and
        # the code movie.title = edited_movies.get('title')
        movie = Movie.query.get(movie_id)
        movie.title = new_title
        db.session.commit()

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        db.session.delete(movie)
        db.session.commit()
