from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from create_data import Movie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Str()
    rating = fields.Float()

api = Api(app)

movie_ns = api.namespace("movies")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# Шаг 2 для вывода всех фильмов
@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_query = db.session.query(Movie)

        ### Условие для 3 Шага ###
        director_id = request.args.get("director_id")
        if director_id is not None:
            movies_query = movies_query.filter(Movie.director_id == director_id)

        ### Условие для 4 Шага ###
        genre_id = request.args.get("genre_id")
        if genre_id is not None:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)

        return movies_schema.dump(movies_query.all())

# Шаг 2 для вывода по id фильма
@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie_query = db.session.query(Movie).get(id)
        if not movie_query:
            return "Такого фильма нет"
        return movie_schema.dump(movie_query)

if __name__ == '__main__':
    app.run(debug=True)
