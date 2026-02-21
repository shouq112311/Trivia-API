import unittest
import json
import os
from dotenv import load_dotenv


from flaskr import create_app
from models import db, Question, Category
load_dotenv()

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        self.database_path = os.getenv("DATABASE_TEST_URL")
        """Define test variables and initialize app."""

        if not self.database_path:
            raise RuntimeError(
                "DATABASE_TEST_URL is not set. Add it to backend/.env "
                "e.g. DATABASE_TEST_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/trivia_test"
            )
            


        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Seed minimal data for tests
            cat1 = Category(type="Science")
            cat2 = Category(type="Art")
            db.session.add_all([cat1, cat2])
            db.session.commit()

            q1 = Question(
                question="What is H2O?",
                answer="Water",
                category=str(cat1.id),
                difficulty=1
            )
            q2 = Question(
                question="Who painted Mona Lisa?",
                answer="Da Vinci",
                category=str(cat2.id),
                difficulty=2
            )
            db.session.add_all([q1, q2])
            db.session.commit()

            self.category_id = cat1.id
            self.question_id = q1.id

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_categories_success(self):
        res = self.client.get("/categories")
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("categories", data)
        self.assertTrue(len(data["categories"]) > 0)

    def test_get_questions_success(self):
        res = self.client.get("/questions?page=1")
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)
        self.assertIn("categories", data)
        self.assertIn("current_category", data)

    def test_get_questions_404_out_of_range(self):
        res = self.client.get("/questions?page=9999")
        self.assertEqual(res.status_code, 404)

    def test_get_questions_by_category_success(self):
        res = self.client.get(f"/categories/{self.category_id}/questions")
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)
        self.assertIn("current_category", data)

    def test_get_questions_by_category_404(self):
        res = self.client.get("/categories/9999/questions")
        self.assertEqual(res.status_code, 404)

    def test_delete_question_success(self):
        res = self.client.delete(f"/questions/{self.question_id}")
        data = res.get_json() if res.is_json else {}

        self.assertIn(res.status_code, [200, 204])

        if res.status_code == 200:
            self.assertTrue(data["success"])
            self.assertEqual(data.get("deleted"), self.question_id)

        with self.app.app_context():
            deleted = Question.query.get(self.question_id)
            self.assertIsNone(deleted)

    def test_delete_question_404(self):
        res = self.client.delete("/questions/9999")
        self.assertEqual(res.status_code, 404)

 
    def test_create_question_success(self):
        payload = {
            "question": "New test question?",
            "answer": "New test answer",
            "difficulty": 1,
            "category": str(self.category_id)
        }
        res = self.client.post(
            "/questions",
            data=json.dumps(payload),
            content_type="application/json"
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_create_question_400_missing_fields(self):
        payload = {
            "question": "Missing answer/difficulty/category"
        }
        res = self.client.post(
            "/questions",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)

 
    def test_search_questions_success(self):
        payload = {"searchTerm": "H2O"}
        res = self.client.post(
            "/questions",
            data=json.dumps(payload),
            content_type="application/json"
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)

    def test_search_questions_no_results(self):
        payload = {"searchTerm": "zzzz-no-match"}
        res = self.client.post(
            "/questions",
            data=json.dumps(payload),
            content_type="application/json"
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["total_questions"], 0)

 
    def test_play_quiz_success(self):
        payload = {
            "previous_questions": [],
            "quiz_category": {"id": str(self.category_id), "type": "Science"}
        }
        res = self.client.post(
            "/quizzes",
            data=json.dumps(payload),
            content_type="application/json"
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn("question", data)

    def test_play_quiz_400_bad_request(self):
        
        payload = {"quiz_category": {"id": "1", "type": "Science"}}
        res = self.client.post(
            "/quizzes",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()