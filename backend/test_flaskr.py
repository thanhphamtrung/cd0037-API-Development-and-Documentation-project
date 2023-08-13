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

    def test_create_question_missing_fields(self):
        # Attempt to create a question with missing fields
        new_question_data = {
            'question': 'Test question',
            'answer': 'Test answer',
            # Missing category and difficulty fields
        }
        response = self.client().post('/questions', json=new_question_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Missing required fields.')

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

    def test_delete_nonexistent_question(self):
        # Attempt to delete a question with a non-existent ID
        response = self.client().delete('/questions/9999')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Question not found.')

    # Test for POST /questions/search
    def test_search_questions(self):
        search_data = {'searchTerm': 'Test'}
        response = self.client().post('/questions/search', json=search_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
    
    def test_search_questions_empty_search_term(self):
        # Attempt to search with an empty search term
        search_data = {'searchTerm': ''}
        response = self.client().post('/questions/search', json=search_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Search term is required.')

    # Test for GET /categories/<int:category_id>/questions
    def test_get_questions_by_category(self):
        category_id = 1
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)

    def test_get_questions_by_category_invalid_category(self):
        # Attempt to get questions for an invalid category ID
        response = self.client().get('/categories/9999/questions')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Category not found.')

    # Test for POST /quizzes
    def test_get_quiz_question(self):
        quiz_data = {'previous_questions': [], 'quiz_category': {'id': 1}}
        response = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])
    
    def test_get_quiz_question_invalid_category(self):
        # Attempt to get a quiz question for an invalid category
        quiz_data = {'previous_questions': [], 'quiz_category': {'id': 9999}}
        response = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Category not found.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
