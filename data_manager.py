from models import db, User, Movie, User_Movie
from dotenv import load_dotenv
import requests
import os

class DataManager:

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


    def add_movie(self, movie, user_id):
        db.session.add(movie)
        self.link_user_to_movie(movie, user_id)
        db.session.commit()


    def update_alt_title(self, user_id, movie_id, new_title):
        user_movie = Movie.query.get(user_id, movie_id)
        user_movie.movie_title = new_title
        db.session.commit()

    def delete_movie(self, user_id, movie_id):
        user_movie = User_Movie.query.get(user_id, movie_id)
        db.session.delete(user_movie)
        # For now don't delete movies from DB if it is not assigned to users
        db.session.commit()

    def get_movie_using_api(self,name):
        request_url = "http://www.omdbapi.com/"
        load_dotenv()
        api_key = os.getenv('API_KEY')
        query_string = f"?apikey={api_key}&t={name}"
        url = request_url + query_string
        response = requests.get(url)
        movie_res = response.json()
        if movie_res["Response"] == 'False':
            msg = movie_res.get('Error', 'Something is wrong')
            raise Exception(msg)
        else:
            required_keys = [obj.name for obj in Movie.__table__.columns]
            movie = {key: value for key, value in movie_res.items()
                      if key in required_keys }
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