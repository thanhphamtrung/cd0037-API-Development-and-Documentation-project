
# Overview:
The Trivia API allows you to interact with a collection of questions organized by categories. You can use this API to retrieve questions, create new questions, search for questions, and play a quiz.

##  1. Base URL

The base URL for the API is `http://localhost:5000`.

## 2. Available Endpoints

### 2. 1. Get Categories

Retrieves a list of all available categories.

**URL:** `/categories`

**Method:** GET

**Request Parameters:** None

**Response Body (Success):**
```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "History"
    },
    ...
  ],
  "success": true
}
```

**Response Body (Error - Internal Server Error):**
```json
{
  "success": false,
  "error": 500,
  "message": "An error occurred while fetching categories."
}
```

### 2.2. Get Paginated Questions

Retrieves a paginated list of questions.

**URL:** `/questions`

**Method:** GET

**Request Parameters:**

- `page` (optional): The page number (default is 1)

**Response Body(Success):**

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 3,
      "difficulty": 2
    },
    ...
  ],
  "total_questions": 10
}
```

**Response Body (Error - Internal Server Error):**
```json
{
  "success": false,
  "error": 500,
  "message": "An error occurred while fetching categories."
}
```

### 2.3. Delete Question

Deletes a question by its ID.

**URL:** `/questions/<int:question_id>`

**Method:** DELETE

**Request Parameters:** None

**Response Body(Success):**

```json
{
  "success": true,
  "deleted": 1
}
```
**Response Body (Error - Question Not Found):**

```json
{
  "success": false,
  "error": 404,
  "message": "Question not found."
}
```

### 2.4. Create Question

Creates a new question.

**URL:** `/questions`

**Method:** POST

**Request Parameters:** None

**Request Body:**

```json
{
  "question": "What is 2 + 2?",
  "answer": "4",
  "category": 4,
  "difficulty": 1
}
```


**Response Body:**

```json
{
  "success": true,
  "created": 11
}

```
**Response Body (Error - Bad Request):**

```json
{
  "success": false,
  "error": 400,
  "message": "Bad request. Missing required fields."
}
```

**Response Body (Error - Unprocessable Entity):**

```json
{
  "success": false,
  "error": 422,
  "message": "An error occurred while processing the request."
}
```


### 2.5. Search Questions

Searches for questions based on a search term.

**URL:** `/questions/search`

**Method:** POST

**Request Parameters:** None

**Request Body:**

```json
{
  "searchTerm": "capital"
}
```
**Response Body:**

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 3,
      "difficulty": 2
    },
    ...
  ],
  "total_questions": 3
}
```

**Response Body (Error - Bad Request):**

```json
{
  "success": false,
  "error": 400,
  "message": "Search term is required."
}
```

**Response Body (Error - Unprocessable Entity):**

```json
{
  "success": false,
  "error": 422,
  "message": "An error occurred while processing the request."
}
```

### 2.6. Get Questions by Category

Retrieves questions based on a category.

**URL:** `/categories/<int:category_id>/questions`

**Method:** GET

**Request Parameters:** None

**Response Body:**

```json
{
  "success": true,
  "questions": [
    {
      "id": 5,
      "question": "Who wrote the play 'Romeo and Juliet'?",
      "answer": "William Shakespeare",
      "category": 2,
      "difficulty": 3
    },
    ...
  ],
  "total_questions": 5,
  "current_category": "History"
}
```

**Response Body (Error - Category Not Found):**

```json
{
  "success": false,
  "error": 404,
  "message": "Category not found."
}
```

**Response Body (Error - Unprocessable Entity):**

```json
{
  "success": false,
  "error": 422,
  "message": "An error occurred while processing the request."
}
```

### 2.7. Get Quiz Question

Retrieves a random question for a quiz.

**URL:** `/quizzes`

**Method:** POST

**Request Parameters:** None

**Request Body:**

```json
{
  "previous_questions": [1, 3],
  "quiz_category": {"id": 2, "type": "Science"}
}
```

**Response Body:**

```json
{
  "success": true,
  "question": {
    "id": 5,
    "question": "What is the chemical symbol for gold?",
    "answer": "Au",
    "category": 1,
    "difficulty": 2
  }
}
```

**Response Body (Error - Bad Request):**

```json
{
  "success": false,
  "error": 400,
  "message": "Quiz category is required."
}
```

**Response Body (Success - No More Questions Available):**

```json
{
  "success": true,
  "question": null
}
```

**Response Body (Error - Category Not Found):**

```json
{
  "success": false,
  "error": 404,
  "message": "Category not found."
}
```

**Response Body (Error - Unprocessable Entity):**

```json
{
  "success": false,
  "error": 422,
  "message": "An error occurred while processing the request."
}
```