from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie
import os
app = Flask(__name__)

#To avoid path issues with Flask, set the database URI using an absolute path:
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] \
    = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link the database and the app.
# This is the reason need to import db from models
db.init_app(app)

# Create an object of DataManager class
data_manager = DataManager()


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('home.html', users = users)


@app.route('/users', methods=['POST'])
def add_user():
    username = request.form.get('username')
    data_manager.create_user(username)
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def show_movies():
    """
    When clicking on a username,
    retrieves that user’s list of favorite movies and displays it."""
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to a user’s list of favorite movies."""
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update',
           methods=['POST'])
def update_title(movie_id):
    """
    Modify the title of a specific movie in a user’s list,
    without depending on OMDb for corrections.
    """
    pass

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete',
           methods=['POST'])
def delete_movie(movie_id):
    """
    Remove a specific movie from a user’s favorite movie list.
    """
    pass


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()