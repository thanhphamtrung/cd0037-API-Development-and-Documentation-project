import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            res = []
            for category in categories:
                res.append({
                    "id": category.id,
                    "type": category.type
                })

            return jsonify({"success": True, "categories": res})
        except Exception as e:
            # Handle any unexpected errors
            print(e)
            abort(500, description='An error occurred while fetching categories.')
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions',  methods=['GET'])
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * 10
            end = start + 10

            questions = Question.query.all()
            paginated_questions = [question.format()
                                   for question in questions[start:end]]

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(questions)
            })
        except Exception as e:
            # Handle any unexpected errors
            print(e)
            abort(500, description='An error occurred while fetching questions.')
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if question is None:
                print('Create an endpoint to DELETE question using a question ID.')
                abort(404, description='Question not found.')

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            data = request.get_json()

            question_text = data.get('question', None)
            print(question_text)
            answer_text = data.get('answer', None)
            category = data.get('category', None)
            difficulty = data.get('difficulty', None)

            if not (question_text and answer_text and category and difficulty):
                abort(400, description='Missing required fields.')

            question = Question(
                question=question_text,
                answer=answer_text,
                category=category,
                difficulty=difficulty
            )
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })

        except Exception as e:
            print(e)
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            data = request.get_json()
            search_term = data.get('searchTerm', '')

            if search_term == '':
                abort(400, description='Search term is required.')

            search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            formatted_results = [question.format() for question in search_results]

            return jsonify({
                'success': True,
                'questions': formatted_results,
                'total_questions': len(formatted_results)
            })

        except:
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)

            if category is None:
                abort(404, description='Category not found.')

            questions = Question.query.filter_by(category=category_id).all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': category.type
            })

        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            data = request.get_json()
            previous_questions = data.get('previous_questions', [])
            quiz_category = data.get('quiz_category', None)

            if quiz_category is None:
                abort(400, description='Quiz category is required.')

            if 'id' in quiz_category:
                category_id = int(quiz_category['id'])
                category = Category.query.get(category_id)

                if category is None:
                    abort(404, description='Category not found.')
                else:
                    questions = Question.query.filter_by(category=category_id).all()
            else:
                questions = Question.query.all()

            remaining_questions = [question.format() for question in questions if question.id not in previous_questions]

            if remaining_questions:
                next_question = random.choice(remaining_questions)
            else:
                next_question = None

            return jsonify({
                'success': True,
                'question': next_question
            })

        except:
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request.'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found.'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity.'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error.'
        }), 500
    
    return app
