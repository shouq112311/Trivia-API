
from tracemalloc import start

from tracemalloc import start

from flask import Flask, app, request, abort, jsonify
from flask_cors import CORS
import random


from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10
from flask import jsonify

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable entity'
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,instance_relative_config=True)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    cors= CORS(app ,resources={r"/*": {"origins": "*"}})

    """
    @✓TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    with app.app_context():
        db.create_all()
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Autherization')
        response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE,OPTIONS')
        return response
    """
    @✓TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():    
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            str(category.id): category.type for category in categories}      
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })    


    """
    @✓TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.order_by(Question.id).all()
        formatted_questions = [q.format() for q in questions]
        current_questions = formatted_questions[start:end]
        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
        str(c.id): c.type
        for c in categories
        }

        return jsonify({
        'questions': current_questions,
        'totalQuestions': len(formatted_questions),
        'categories': formatted_categories,
        'currentCategory': 'All'
    })

    """
    @✓TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question=Question.query.get(question_id)
        if question is None:
            abort(404)

        try:
            question.delete()
        except:
            abort(422)   
        return jsonify({
            'success': True,
            'deleted': question_id
        })
         


        
    """
    @✓TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions', methods=['POST'])
    def create_question_or_search():
        body = request.get_json() or {}

   
        search_term = body.get('searchTerm')
        if search_term is not None:
            selection = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()

            return jsonify({
                'success': True,
                'questions': [q.format() for q in selection],
                'total_questions': len(selection),
                'current_category': None
            })

    # 2) CREATE MODE
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        if not question or not answer or category is None or difficulty is None:
            abort(400)

        try:
            new_q = Question(
                question=question,
                answer=answer,
                category=int(category),
                difficulty=int(difficulty)
            )
            new_q.insert()
            return jsonify({'success': True})
        except:
            abort(422)

    """
    @✓TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @✓TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)

        questions = Question.query.filter(Question.category == str(category_id)).order_by(Question.id).all()
        formatted_questions = [q.format() for q in questions]

        return jsonify({
            'questions': formatted_questions,
            'totalQuestions': len(formatted_questions),
            'currentCategory': category.type
        })
    """
    @✓TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json() or {}
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        if previous_questions is None or quiz_category is None:
            abort(400)
        category_id = quiz_category.get('id', None)
        if category_id in [0, '0', None]:
            query = Question.query
        else:
            query = Question.query.filter(Question.category == str(category_id))
        available = query.filter(~Question.id.in_(previous_questions)).all()
        if len(available) == 0:
            return jsonify({
                'success': True,
                'question': None
            })
        new_question = random.choice(available)
        return jsonify({
            'success': True,
            'question': new_question.format()
        })
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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

