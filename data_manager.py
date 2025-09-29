from models import db, User, Movie, User_Movie
from dotenv import load_dotenv
import requests
import os

# For API Key
load_dotenv()
API_KEY = os.getenv('API_KEY')

class DataManager:

    def create_user(self, name):
        """To create user using name from parameter"""
        new_user = User(name=name)
        db.session.add(new_user)
        self.db_commit()

    def get_users(self):
        """To fetch all the users available"""
        users = User.query.all()
        return users

    def get_user(self,user_id):
        """To fetch specific user with user_id"""
        user = User.query.get(user_id)
        return user

    def get_movies(self, user_id):
        """
        To fetch all the movies the belong to a particular user
        :param - user_id:integer unique id of the user
        :return - movie details
        """
        # Get all the movie details using innerjoin of user_movie and movie table
        movies = User_Movie.query.join(User_Movie.movie).filter(
                                    User_Movie.user_id==user_id )
        return movies

    def add_movie(self, movie, user_id):
        """
        Add movie to the database tables
        :param movie: object of class Movie
        :param user_id: integer unique user id
        """
        # Check movie exist in movie table
        """movie_exist = self.get_movie_by_title(movie.title, year=movie.year)
        if not movie_exist:
            # Add movie to the table
            db.session.add(movie)
            self.db_commit()"""
        # Add movie to the table
        db.session.add(movie)
        self.db_commit()
        # Update the movie to the user list of movies in user_movies table
        self.link_user_to_movie(movie, user_id)

    def update_alt_title(self, user_id, movie_id, new_title):
        """
        To update alternate movie title, in case user want to personalize
        :param user_id: Unique user ID(integer)
        :param movie_id: Unique movie ID (integer)
        :param new_title: Personalized title
        """
        # Fetch the existing data
        user_movie = User_Movie.query.get((user_id, movie_id))
        # Update the new data
        user_movie.movie_title = new_title
        self.db_commit()

    def delete_movie(self, user_id, movie_id):
        """ To delete a movie from user's list"""
        user_movie = User_Movie.query.get((user_id, movie_id))
        db.session.delete(user_movie)
        # For now don't delete movies from DB if it is not assigned to users
        self.db_commit()

    def get_movie_using_api(self,name, year=None):
        """To use OMDB API to fetch the movie details"""
        request_url = "http://www.omdbapi.com/"

        # Populate the url
        query_string = f"?apikey={API_KEY}&t={name}"
        if year:
            query_string += f"&y={year}"
        url = request_url + query_string

        # Fetch the response from API (API call )
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None
        movie_res = response.json()

        if movie_res["Response"] == 'False':
            return None
        else:
            # Get the column names into a list of strings
            required_keys = [obj.name for obj in Movie.__table__.columns if obj.name != 'movie_id']
            # Create a dictionary with column names as keys and movie details as values
            movie = {key.lower(): value for key, value in movie_res.items()
                      if key.lower() in required_keys }
            return movie

    def link_user_to_movie(self, movie, user_id):
        """Adding a movie into a user's list of movies"""
        #Create a new entry in user_movies table
        new_relation = User_Movie(
            user_id = user_id,
            movie_id = movie.movie_id,
            movie_title = movie.title
        )
        db.session.add(new_relation)
        db.session.commit()

    def delete_link(self, movie_id, user_id):
        """To be implemented"""
        pass

    def get_movie_by_title(self,title, user_id=None, year=None):
        """
        To get a movie details from table. If you need to find if the movie is
        assigned to a user, user_id needs to be provided
        :param title: Movie name mandatory
        :param user_id: Unique ID of a user (Optional)
        :param year: Year in which movie was released (Optional)
        :return: Object of the class Movie
        """
        if user_id:
            # Query using join of user_movies and movies table
            query = (
                User_Movie.query.join(User_Movie.movie).filter(
                    User_Movie.user_id == user_id,
                    Movie.title.ilike(title)
                )
            )
        else:
            # Query from movies table
            query = (Movie.query.filter(Movie.title.ilike(title)))
        if year:
            query = query.filter(Movie.year == year)
        movie = query.first()
        #movie = query.one_or_none()
        return movie

    def db_commit(self):
        """To save the Database Updates to underlying database"""
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            msg = "Database operation Failed:"
            raise RuntimeError(f"{msg}{str(error)}") from error