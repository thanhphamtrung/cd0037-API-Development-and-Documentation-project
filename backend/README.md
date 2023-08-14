# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

1. `GET '/categories'`

- Fetches all available categories.
- Request Arguments: None
- Returns: An object with two keys, `success` and `categories`, where `categories` is an array of objects with keys `id` and `type`.

```json
{
  "success": True,
  "categories": [
    {"id": 1, "type": "Science"},
    {"id": 2, "type": "Art"}
  ]
}
```

2. `GET '/questions'`

- Fetches questions with pagination (every 10 questions).
- Request Arguments: `page` (optional, default value is 1)
- Returns: An object with keys `success`, `questions`, and `total_questions`.

```json
{
  "success": True,
  "questions": [
    {
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 3,
      "difficulty": 2
    }
  ],
  "total_questions": 50
}
```

3. `DELETE '/questions/int:question_id'`

- Deletes a question using the question ID.
- Request Arguments: `question_id`
- Returns: An object with keys `success` and `deleted` (the ID of the deleted question).

```json
{
  "success": True,
  "deleted": 10
}
```

4. `POST '/questions'`

- Posts a new question with required fields.
- Request Body: `question`, `answer`, `category`, `difficulty`
- Returns: An object with keys `success` and `created` (the ID of the created question).

```json
{
  "success": True,
  "created": 30
}
```

5. `POST '/questions/search'`

- Searches questions based on a search term.
- Request Body: `searchTerm`
- Returns: An object with keys `success`, `questions`, and `total_questions`.

```json
{
  "success": True,
  "questions": [
    {
      "question": "What is the title of the book?",
      "answer": "The Title",
      "category": 1,
      "difficulty": 3
    }
  ],
  "total_questions": 5
}
```

6. `GET '/categories/int:category_id/questions'`

- Gets questions based on category.
- Request Arguments: `category_id`
- Returns: An object with keys `success`, `questions`, `total_questions`, and `current_category`.

```json
{
  "success": True,
  "questions": [
    {
      "question": "Who painted the Mona Lisa?",
      "answer": "Leonardo da Vinci",
      "category": 2,
      "difficulty": 4
    }
  ],
  "total_questions": 20,
  "current_category": "Art"
}
```

7. `POST '/quizzes'`

- Gets questions to play the quiz.
- Request Body: `previous_questions` (optional), `quiz_category` (required)
- Returns: An object with keys `success` and `question`.

```json
{
  "success": True,
  "question": {
    "question": "What is the capital of Italy?",
    "answer": "Rome",
    "category": 3,
    "difficulty": 3
  }
}
```

`## Error Handlers`

- 400: Bad request.
- 404: Resource not found.
- 422: Unprocessable entity.
- 500: Internal server error.

```json
{
  "success": False,
  "error": 404,
  "message": "Resource not found."
}
```

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
