import unittest
from unittest.mock import patch
from models import Movies
from main import app

class MoviesTestCase(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()
        # Create a new application context
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop the application context when the test is finished
        self.app_context.pop()

    @patch('main.Movies.query')
    def test_fetch_movie_with_valid_movie_returned_returns_response_201(self, mocked_movie):
        with app.app_context():
            movie = Movies(
                Movie_id="Test",
                Movie_Title="Test",
                Genre="Test",
                Director="Test",
                Rating=5
            )
            mocked_movie.filter_by.return_value.first.return_value = movie

            response = self.client.get('/fetch_movie?movie=Test')

            self.assertEqual(response.status_code, 201)

    def test_fetch_movie_with_no_movie_returned_returns_response_404(self):
        with app.app_context():
            response = self.client.get('/fetch_movie?movie=Test')

            self.assertEqual(response.status_code, 404)

    @patch("main.jsonify")
    @patch('main.db.session')
    @patch('main.Movies.query')
    def test_create_movies_with_new_movie_returns_response_201(self, mock_query, mock_db_session, mocked_json):
        with app.app_context():
            movie = Movies(
                Movie_id="Test",
                Movie_Title="Test",
                Genre="Test",
                Director="Test",
                Rating=5
            )
            mock_query.filter_by.return_value.first.return_value = None
            mock_db_session.add.return_value = movie
            mocked_json(movie.serialize()).return_value = "Test"

            response = self.client.post('/movies', json={'movie_title': 'Create a Movie', 'genre': 'Genre', 'director': 'Director', 'rating': 5})

            self.assertEqual(response.status_code, 201)

    def test_create_movies_with_missing_title_returns_response_422(self):
        with app.app_context():
            response = self.client.post('/movies', json={'genre': 'Genre', 'director': 'Director', 'rating': 5})

            self.assertEqual(response.status_code, 422)


    @patch('main.Movies.query')
    def test_create_movies_with_duplicate_title_returns_response_409(self, mock_query):
        with app.app_context():
            movie = Movies(
                Movie_id="Test",
                Movie_Title="Test",
                Genre="Test",
                Director="Test",
                Rating=5
            )
            mock_query.filter_by.return_value.first.return_value = movie

            response = self.client.post('/movies', json={'movie_title': 'Create a Movie', 'genre': 'Genre', 'director': 'Director', 'rating': 5})

            self.assertEqual(response.status_code, 409)

    @patch('main.db.session')
    @patch('main.Movies.query')
    def test_delete_movie_with_valid_movie_returns_response_200(self, mock_query, mock_db_session):
        with app.app_context():
            movie = Movies(
                Movie_id="Test",
                Movie_Title="Test",
                Genre="Test",
                Director="Test",
                Rating=5
            )
            mock_query.filter_by.return_value.first.return_value = movie
            mock_db_session.delete.return_value = None
            mock_db_session.commit.return_value = None

            response = self.client.delete('/movies/Test')

            self.assertEqual(response.status_code, 200)


    def test_delete_movie_with_invalid_movie_returns_response_404(self):
        with app.app_context():
            response = self.client.delete('/movies/Test')

            self.assertEqual(response.status_code, 404)

    @patch('main.db.session')
    @patch('main.Movies.query')
    def test_update_movie_with_valid_movie_returns_response_200(self, mock_query, mock_db_session):
        with app.app_context():
            movie = Movies(
                Movie_id="Test",
                Movie_Title="Test",
                Genre="Test",
                Director="Test",
                Rating=5
            )
            mock_query.filter_by.return_value.first.return_value = movie
            mock_db_session.commit.return_value = None

            response = self.client.put('/movies/Test', json={'genre': 'Genre', 'director': 'Director', 'rating': 5})

            self.assertEqual(response.status_code, 200)

    def test_update_movie_with_invalid_movie_returns_response_404(self):
        with app.app_context():
            response = self.client.put('/movies/Test', json={'genre': 'Genre', 'director': 'Director', 'rating': 5})

            self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()