from models import db, User, Movie, User_Movie
from dotenv import load_dotenv
import requests
import os

class DataManager:

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        self.db_commit()

    def get_users(self):
        users = User.query.all()
        return users

    def get_user(self,user_id):
        user = User.query.get(user_id)
        return user

    def get_movies(self, user_id):
        """movie_ids = User_Movie.query.filter_by(user_id = user_id).all()
        movies = []
        for movie_id in movie_ids:
            movie = Movie.query.filter_by(movie_id = movie_id)
            movies.append(movie)
        return movies"""
        """movies = (
            User_Movie.query
            .join(User_Movie.user)
            .join(User_Movie.movie)
            .filter(User_Movie.user_id == user_id)
        )"""
        movies = User_Movie.query.join(User_Movie.movie).filter_by(user_id=user_id)
        return movies

    def add_movie(self, movie, user_id):
        db.session.add(movie)
        self.link_user_to_movie(movie, user_id)
        self.db_commit()

    def update_alt_title(self, user_id, movie_id, new_title):
        user_movie = Movie.query.get(user_id, movie_id)
        user_movie.movie_title = new_title
        self.db_commit()

    def delete_movie(self, user_id, movie_id):
        user_movie = User_Movie.query.get(user_id, movie_id)
        db.session.delete(user_movie)
        # For now don't delete movies from DB if it is not assigned to users
        self.db_commit()

    def get_movie_using_api(self,name, year=None):
        request_url = "http://www.omdbapi.com/"
        load_dotenv()
        api_key = os.getenv('API_KEY')
        query_string = f"?apikey={api_key}&t={name}"
        if year:
            query_string += f"&y={year}"
        url = request_url + query_string
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None
        movie_res = response.json()
        if movie_res["Response"] == 'False':
            return None
        else:
            required_keys = [obj.name for obj in Movie.__table__.columns if obj.name != 'movie_id']
            movie = {key.lower(): value for key, value in movie_res.items()
                      if key.lower() in required_keys }
            return movie

    def link_user_to_movie(self, movie, user_id):
        new_relation = User_Movie(
            user_id = user_id,
            movie_id = movie.movie_id,
            movie_title = movie.title
        )
        db.session.add(new_relation)

    def delete_link(self, movie_id, user_id):
        pass

    def get_movie_by_title(self,user_id, title, year=None):
        query = (
            User.Movie.join(User_Movie.movie).filter(
                User_Movie.user_id == user_id,
                User_Movie.movie.title.ilike(title)
            )
        )
        if year:
            query = query.filter(User_Movie.movie.year == year)
        movie = query.first()
        return movie

    def db_commit(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            msg = "Something went wrong while saving to the database"
            raise Exception(msg)