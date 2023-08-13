import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.drop_all()

    # Test for GET /categories
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']) > 0)

    # Test for GET /questions
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)

    # Test for POST /questions
    def test_create_question(self):
        question_data = {
            'question': 'Test question',
            'answer': 'Test answer',
            'category': 1,
            'difficulty': 1
        }
        response = self.client().post('/questions', json=question_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    # Test for DELETE /questions/<int:question_id>
    def test_delete_question(self):
        # Create a new question for testing
        new_question = Question(
            question='Test question',
            answer='Test answer',
            category=1,
            difficulty=1
        )
        new_question.insert()

        # Get the ID of the newly created question
        question_id = new_question.id

        # Delete the question using DELETE /questions/<int:question_id>
        response = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)

    # Test for POST /questions/search
    def test_search_questions(self):
        search_data = {'searchTerm': 'Test'}
        response = self.client().post('/questions/search', json=search_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

    # Test for GET /categories/<int:category_id>/questions
    def test_get_questions_by_category(self):
        category_id = 1
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)

    # Test for POST /quizzes
    def test_get_quiz_question(self):
        quiz_data = {'previous_questions': [], 'quiz_category': {'id': 1}}
        response = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

    """
    TODO
    Write more test cases for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
