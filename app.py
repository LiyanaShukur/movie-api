from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask and Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/nurliyanaabdshukur/pythonProjects/instance/movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)

# Define Movie Model (should ideally be in a separate database.py file)
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)

# Create tables
with app.app_context():
    db.create_all()
    # Add sample data if empty
    if not Movie.query.first():
        sample_movies = [
            Movie(title="Inception", genre="Sci-Fi", year=2010, rating=8.8),
            Movie(title="The Shawshank Redemption", genre="Drama", year=1994, rating=9.3),
            Movie(title="Pulp Fiction", genre="Crime", year=1994, rating=8.9)
        ]
        db.session.add_all(sample_movies)
        db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/movies')
def get_movies():
    movies = Movie.query.all()
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'genre': m.genre,
        'year': m.year,
        'rating': m.rating
    } for m in movies])

@app.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.json
    new_movie = Movie(
        title=data.get('title'),
        genre=data.get('genre'),
        year=data.get('year'),
        rating=data.get('rating')
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'message': 'Movie added', 'id': new_movie.id}), 201

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'Movie deleted'})
    return jsonify({'error': 'Movie not found'}), 404

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=True)
