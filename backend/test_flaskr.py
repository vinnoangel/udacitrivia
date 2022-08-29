import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, User, Score


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.DB_PATH = 'postgresql://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)

        setup_db(self.app, self.DB_PATH)

        # set new question for insertion
        self.new_question = {
            "question": "New question", 
            "answer": "New answer", 
            "difficulty": 3, 
            "category": 1, 
            "rating": 2
        }

        # get the last question
        self.question = Question.query.order_by(Question.id.desc()).first()
        # get question ID to be used for testing question delete
        self.question_id_to_delete = self.question.id

        # set new category for insertion
        self.new_category = {
            "type": "New Category",
        }

        # set new user for insertion
        self.new_user = {
            "username": "hazard", 
            "fullname": "Eden Hazard", 
            "gender": "Male"
        }

        # get the last user
        self.user1 = User.query.order_by(User.id.desc()).first()
        # get user ID to be used for testing user delete
        self.user_id_to_delete = self.user1.id

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # 1
    """ Test Categories With Correct Endpoint """
    def test_categories_with_correct_endpoint(self):
        res = self.client().get("/api/v1/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))
    # =================================================

    """ Test Categories With Incorrect Endpoint """
    def test_404_for_categories_with_incorrect_endpoint(self):
        res = self.client().get("/api/v1/categoriese")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    # =================================================

    # 2
    """ Test Get Questions, Current Categories and All Categories With Valid Page """
    def test_get_questions_and_current_category_and_all_categories_with_valid_page(self):
        res = self.client().get("/api/v1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 10)
        self.assertEqual(data["total_questions"], 23)
        self.assertTrue(len(data["categories"]))
    # =================================================

    """ Test Get Questions, Current Categories and All Categories With Invalid Page """
    def test_404_for_get_question_and_current_category_and_all_categories_with_invalid_page(self):
        res = self.client().get("/api/v1/questions?page=250")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    # =================================================

    # 3
    """ Test Delete Question IF Question ID Exist"""
    def test_delete_question(self):
        res = self.client().delete("/api/v1/questions/" + str(self.question_id_to_delete))
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == self.question_id_to_delete).one_or_none()

        self.assertTrue(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["question_id"], self.question_id_to_delete)
        self.assertEqual(question, None)
    # =================================================

    """ Test Delete Question If Question ID Does Not Exist"""
    def test_delete_question_if_not_exist(self):
        res = self.client().delete("/api/v1/questions/1999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")
    # =================================================

    # 4
    """ Test Create Question """
    def test_create_question(self):
        res = self.client().post("/api/v1/questions", json=self.new_question)
        data = json.loads(res.data)

        question = Question.query.get(data["question_id"])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question_id"])
        self.assertTrue(question)
    # =================================================

    """ Test Create Question If Method Is Not Allowed """
    def test_405_if_create_question_method_is_not_allowed(self):
        res = self.client().post("/api/v1/questions/2", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    # =================================================

    # 5
    """ Test Search Question With Result """
    def test_search_question_with_result(self):
        res = self.client().post("/api/v1/questions/search", json={"searchTerm": "question"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), 2)
        self.assertEqual(data["total_questions"], 2)
    # =================================================

    """ Test Search Question Without Result """
    def test_search_question_without_result(self):
        res = self.client().post("/api/v1/questions/search", json={"searchTerm": "questionss"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(data["total_questions"], 0)
    # =================================================

    # 6
    """ Test Get Questions Based On Category With Correct Category ID """
    def test_get_questions_based_on_category_with_correct_category_id(self):
        res = self.client().get("/api/v1/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), 5)
        self.assertEqual(data["total_questions"], 5)
    # =================================================

    """ Test 404 Get Questions Based On Category With Incorrect Category ID """
    def test_404_to_get_questions_based_on_category_with_correct_category_id(self):
        res = self.client().get("/api/v1/categories/134/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")
    # =================================================

    # 7
    """ Test Get Quizzes With Result """
    def test_get_quizzes_with_result(self):
        res = self.client().post("/api/v1/quizzes", json={"previous_questions": [16, 17], "quiz_category": 2})
        data = json.loads(res.data)

        message = "question already answered"
        container = {16, 17}
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["question"]))
        self.assertNotIn(data["question"]["id"], container, message)
    # =================================================
    
    """ Test Get Quizzes Without Result """
    def test_get_quizzes_without_result(self):
        res = self.client().post("/api/v1/quizzes", json={"previous_questions": [16, 17, 18, 19, 24], "quiz_category": 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertFalse(len(data["question"]))
    # =================================================

    # 8
    """ Test Create Category """
    def test_create_category(self):
        res = self.client().post("/api/v1/categories", json=self.new_category)
        data = json.loads(res.data)

        category = Category.query.get(data["category_id"])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category_id"])
        self.assertTrue(category)
    # =================================================

    """ Test Create Category If Page Not Found """
    def test_404_if_create_category_page_not_found(self):
        res = self.client().post("/api/v1/categories/2", json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    # =================================================

     # 9
    """ Test Users With Correct Endpoint """
    def test_users_with_correct_endpoint(self):
        res = self.client().get("/api/v1/users")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["users"]))
    # =================================================

    """ Test Users With Incorrect Endpoint """
    def test_404_for_users_with_incorrect_endpoint(self):
        res = self.client().get("/api/v1/userse")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    # =================================================

     # 10
    """ Test Create User """
    def test_create_user(self):
        res = self.client().post("/api/v1/users", json=self.new_user)
        data = json.loads(res.data)

        user = User.query.get(data["user_id"])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["user_id"])
        self.assertTrue(user)
    # =================================================

    """ Test Create User With Bad Method """
    def test_404_if_create_user_page_not_found(self):
        res = self.client().post("/api/v1/users/2", json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    # =================================================

    # 11
    """ Test Delete User IF User ID Exist"""
    def test_delete_user(self):
        res = self.client().delete("/api/v1/users/" + str(self.user_id_to_delete))
        data = json.loads(res.data)

        user = User.query.filter(User.id == self.user_id_to_delete).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["user_id"], self.user_id_to_delete)
        self.assertEqual(user, None)
    # =================================================

    """ Test Delete User If User ID Does Not Exist"""
    def test_delete_user_if_not_exist(self):
        res = self.client().delete("/api/v1/users/1999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")
    # =================================================



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
