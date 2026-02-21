Backend - Trivia API
Overview

The Trivia API is a RESTful backend application built using Flask and PostgreSQL.
It provides endpoints to manage trivia questions and categories, perform search operations, delete questions, create new questions, and play a quiz game.

This project follows RESTful principles and includes proper error handling and testing.

Setup Instructions
1. Install Dependencies
Python

Install Python 3.7 or higher.

Virtual Environment

Create and activate a virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
Install Required Packages

Navigate to the /backend folder and run:

pip install -r requirements.txt
Database Setup

Make sure PostgreSQL is running.

Create the database:

createdb trivia

Populate the database:

Mac/Linux:

psql trivia < trivia.psql

Windows PowerShell:

psql -U postgres -d trivia -f trivia.psql
Running the Server

From the /backend directory:

Windows PowerShell:

$env:FLASK_APP="flaskr"
$env:FLASK_ENV="development"
flask run

Mac/Linux:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

The API will run on:

http://127.0.0.1:5000
API Endpoints
GET /categories

Returns all available categories.

Response:

{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
GET /questions?page=<int>

Returns paginated questions (10 per page).

Query Parameters:

page (int, optional, default=1)

Response:

{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "Sample question",
      "answer": "Sample answer",
      "difficulty": 2,
      "category": "1"
    }
  ],
  "total_questions": 21,
  "categories": {},
  "current_category": "All"
}
GET /categories/<int:id>/questions

Returns questions for a specific category.

Response:

{
  "success": true,
  "questions": [],
  "total_questions": 5,
  "current_category": "Science"
}
DELETE /questions/<int:id>

Deletes a question by ID.

Response:

{
  "success": true,
  "deleted": 10
}
POST /questions (Create Question)

Creates a new question.

Request Body:

{
  "question": "New question",
  "answer": "New answer",
  "difficulty": 1,
  "category": "3"
}

Response:

{
  "success": true
}
POST /questions (Search)

Searches for questions containing a substring.

Request Body:

{
  "searchTerm": "title"
}

Response:

{
  "success": true,
  "questions": [],
  "total_questions": 1,
  "current_category": null
}
POST /quizzes

Returns a random quiz question not in previous questions.

Request Body:

{
  "previous_questions": [1, 4],
  "quiz_category": {
    "id": "3",
    "type": "Geography"
  }
}

Response:

{
  "success": true,
  "question": {
    "id": 7,
    "question": "Sample quiz question",
    "answer": "Sample answer",
    "difficulty": 2,
    "category": "3"
  }
}

If no questions remain:

{
  "success": true,
  "question": null
}
Error Handling

Errors are returned in JSON format:

{
  "success": false,
  "error": 404,
  "message": "resource not found"
}

The API handles:

400 Bad Request

404 Resource Not Found

422 Unprocessable Entity

500 Internal Server Error

Testing

To run tests:

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

All endpoints include both success and error test cases.

Code Quality

Follows PEP8 style guidelines

Uses meaningful variable and function names

Properly structured endpoints

Uses Flask-CORS for cross-origin requests

Implements full CRUD operations

Includes structured error handling

Author

Trivia API Project - Backend Developer Nanodegree