from operator import and_, or_
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, User, Score, db

QUESTIONS_PER_PAGE = 10
USERS_PER_PAGE = 10
SCORES_PER_PAGE = 10

"""
Paginate questions and format where neccesary
"""


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


# ===========================================================


"""
Paginate users and format where neccesary
"""


def paginate_users(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * USERS_PER_PAGE
    end = start + USERS_PER_PAGE

    users = [user.format() for user in selection]
    current_users = users[start:end]

    return current_users


# ===========================================================


"""
Paginate scores and format where neccesary
"""


def paginate_scores(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * SCORES_PER_PAGE
    end = start + SCORES_PER_PAGE

    scores = [user.format() for user in selection]
    current_scores = scores[start:end]

    return current_scores


# ===========================================================


"""
Error handler
"""


def error_handler(error_code, message):
    return jsonify({
        "success": False,
        "error_code": error_code,
        "message": message
    }), error_code


# ===========================================================


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'*': {"origins": "*"}}, supports_credentials=True)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    # 1
    @app.route('/api/v1/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        categories_formatted = {category.id: category.type for category in categories}

        return jsonify({
            "success": True,
            "categories": categories_formatted
        })

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

    # 2
    @app.route('/api/v1/questions', methods=['GET'])
    def get_questions():
        # get all questions
        selection = Question.query.order_by(Question.id.asc()).all()
        questions = paginate_questions(request, selection)

        if len(questions) == 0:
            abort(404)

        # get all categories
        categories = Category.query.all()
        categories_formatted = {category.id: category.type for category in categories}

        # Get the first category as current category
        current_category = Category.query.first().type

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(selection),
            "categories": categories_formatted,
            "current_category": current_category
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    # 3
    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                "success": True,
                "message": "Question deleted successfully",
                "question_id": question_id,
            })
            
        except IndexError:
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

    # 4
    @app.route('/api/v1/questions', methods=['POST'])
    def create_question():
        try:
            # get post requests
            body = request.get_json()
            question = body.get("question")
            answer = body.get("answer")
            difficulty = body.get("difficulty")
            rating = body.get("rating")
            category = body.get("category")

            # insert new question and persist question in the database
            new_question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category,
                rating=rating
            )
            new_question.insert()

            return jsonify({
                "success": True,
                "message": "Question created successfully",
                "question_id": new_question.id
            })

        except Exception:
            db.session.rollback()
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

    # 5
    @app.route('/api/v1/questions/search', methods=['POST'])
    def search_question():
        current_category = []
        search_term = request.get_json()['searchTerm']
        search_term = "%{}%".format(search_term)

        selection = Question.query.filter(Question.question.ilike(search_term)).all()
        questions = paginate_questions(request, selection)

        if len(questions) > 0:
            current_category = Category.query.get(questions[0]['category']).type

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(selection),
            "current_category": current_category
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    # 6
    @app.route('/api/v1/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            selection = Question.query.order_by(Question.id.desc()).filter(Question.category == category_id).all()
            questions = paginate_questions(request, selection)

            if len(questions) == 0:
                abort(404)

            current_category = Category.query.get(category_id).type

            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(selection),
                "current_category": current_category
            })

        except IndexError:
            abort(404)

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

    # 7
    @app.route('/api/v1/quizzes', methods=['POST'])
    def get_quizzes():

        try:
            question = []

            # get request body parameters
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            """
            Check if previous question exist while quiz category is empty
            Previous question is dependent on quiz category
            And as such should not contain any value when quizcategory is empty
            """

            if quiz_category is None and len(previous_questions) > 0:
                abort(422)

            if quiz_category == 0:
                # fetch a default category since it's empty
                quiz_category = Category.query.first().id

            # fetch all questions for the current category and remove previous category questions
            query_selection = Question.query \
                .filter(and_(Question.category == quiz_category, Question.id.not_in(previous_questions)))

            # get total number of remaining questions for this current category
            remaining_rows = query_selection.count()
            if remaining_rows > 0:
                offset = int(remaining_rows * random.random())
                # randomly pick one question from the remaining questions for this current category
                question = query_selection.offset(offset).first().format()

            return jsonify({
                "success": True,
                "question": question,
            })
        except Exception:
            abort(422)

    # Suggested endpoints for project to stand out
    """ 
    Create New Category
    """

    # 8
    @app.route('/api/v1/categories', methods=['POST'])
    def create_category():
        try:
            # get post requests
            type = request.get_json()["type"]

            # insert new category and persist category in the database
            category = Category(type=type)
            category.insert()

            return jsonify({
                "success": True,
                "message": "Category created successfully",
                "category_id": category.id
            })

        except Exception:
            db.session.rollback()
            abort(422)

    """
    Endpoint that handles GET requests
    for all users.
    """

    # 9
    @app.route('/api/v1/users', methods=['GET'])
    def get_users():
        p = request.args.get("p", "", type=str)

        # get all users
        selection = User.query.order_by(User.id.desc()).all()

        if p == 'all':
            users = {user.id: user.username for user in selection}
        else:
            users = paginate_users(request, selection)

        return jsonify({
            "success": True,
            "users": users,
            "total_users": len(selection)
        })

    """
    Endpoint that handles GET requests
    for a single user.
    """

    # 10
    @app.route('/api/v1/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        return jsonify({
            "success": True,
            "user": user.format()
        })

    """ 
    Create New User
    """

    # 10
    @app.route('/api/v1/users', methods=['POST'])
    def create_user():
        try:
            # get post requests
            body = request.get_json()
            username = body.get("username")
            fullname = body.get("fullname")
            gender = body.get("gender")

            # insert new user and persist user in the database
            user = User(username=username, fullname=fullname, gender=gender)
            user.insert()

            return jsonify({
                "success": True,
                "message": "User created successfully",
                "user_id": user.id
            })

        except Exception:
            db.session.rollback()
            abort(422)

    """
    Endpoint to DELETE user using a user ID.
    """

    # 11
    @app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            if user is None:
                abort(404)

            user.delete()  # delete user

            # delete associated game scores
            scores = Score.query.filter(Score.user_id == user_id).all()
            if scores:
                scores.delete()

            return jsonify({
                "success": True,
                "message": "User deleted successfully",
                "user_id": user_id,
            })

        except IndexError:
            abort(404)

    """
    Endpoint to SEARCH for a user using by either username or fullname.
    """

    # 12
    @app.route('/api/v1/users/search', methods=['POST'])
    def search_user():
        search_term = request.get_json()['searchTerm']
        search_term = "%{}%".format(search_term)

        selection = User.query.filter(or_(User.username.ilike(search_term), User.fullname.ilike(search_term))).all()

        users = paginate_users(request, selection)

        return jsonify({
            "success": True,
            "users": users,
            "total_users": len(selection)
        })

    """
    Endpoint that handles GET requests
    for all scores.
    """

    # 13
    @app.route('/api/v1/scores', methods=['GET'])
    def get_scores():
        # get all scores
        selection = Score.query.order_by(Score.id.desc()).all()
        scores = paginate_scores(request, selection)

        return jsonify({
            "success": True,
            "scores": scores,
            "total_scores": len(selection)
        })

    """
    Endpoint that handles GET requests
    for all scores for a specific user.
    """

    # 14
    @app.route('/api/v1/users/<int:user_id>/scores', methods=['GET'])
    def get_scores_by_user_id(user_id):
        # get all scores
        selection = Score.query.order_by(Score.id.desc()).filter(Score.user_id == user_id).all()
        scores = paginate_scores(request, selection)
        user = User.query.filter(User.id == user_id).one_or_none()

        return jsonify({
            "success": True,
            "scores": scores,
            "total_scores": len(selection),
            "user": user.format()
        })

    """ 
    Save New Score
    """

    # 15
    @app.route('/api/v1/scores', methods=['POST'])
    def create_score():
        try:
            # get post requests
            body = request.get_json()
            user_id = body.get("user_id")
            your_score = body.get("your_score")
            expected_score = body.get("expected_score")

            if int(expected_score) <= 0:
                abort(400)

            # insert new score and persist score in the database
            score = Score(user_id=user_id, your_score=your_score, expected_score=expected_score)
            score.insert()

            return jsonify({
                "success": True,
                "message": "Your score has been saved.",
                "score_id": score.id
            })

        except Exception:
            db.session.rollback()
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def not_found(error):
        return error_handler(400, "bad request")

    @app.errorhandler(404)
    def not_found(error):
        return error_handler(404, "resource not found")

    @app.errorhandler(405)
    def not_found(error):
        return error_handler(405, "method not allowed")

    @app.errorhandler(409)
    def not_found(error):
        return error_handler(409, "request conflicts")

    @app.errorhandler(422)
    def not_found(error):
        return error_handler(422, "unprocessable")

    @app.errorhandler(500)
    def not_found(error):
        return error_handler(500, "internal server error")

    return app
