from . commontest import CommonTest

from odoo.exceptions import ValidationError
from odoo.tools import mute_logger
from odoo.tests import Form


class TestSession(CommonTest):

    def test_10_create_session(self):
        """
        Test create a session.
        """
        course_data = {
            "name": "Test course",
            "description": "This is a test description.",
            "responsible_id": self.user_admin.id,
        }
        course = self.create_course(**course_data)

        instructor_data = {
            "name": "Test instructor",
            "instructor": True,
        }
        instructor = self.create_instructor(**instructor_data)

        session_data = {
            "name": "Test session",
            "number_seats": 10,
            "instructor_id": instructor.id,
            "taken_seats": 5,
            "course_id": course.id,
        }
        session = self.create_session(**session_data)

        self.assertTrue(session.id, "This must be a valid id.")
        self.assertEqual(
            session.name, session_data["name"],
            f"This must be equal to {session_data['name']}.",
        )
        self.assertEqual(
            session.number_seats, session_data["number_seats"],
            f"This must be equal to {session_data['number_seats']}.",
        )
        self.assertEqual(
            session.instructor_id.id, session_data["instructor_id"],
            f"This must be equal to {session_data['instructor_id']}.",
        )
        self.assertEqual(
            session.taken_seats, session_data["taken_seats"],
            f"This must be equal to {session_data['taken_seats']}.",
        )
        self.assertEqual(
            session.course_id.id, session_data["course_id"],
            f"This must be equal to {session_data['course_id']}.",
        )

    @mute_logger("odoo.sql_db")
    def test_20_check_instructor_cannot_be_attendee(self):
        """
        Test instructor cannot be attendee.
        """
        course_data = {
            "name": "Test course",
            "description": "This is a test description.",
            "responsible_id": self.user_admin.id,
        }
        course = self.create_course(**course_data)

        instructor_data = {
            "name": "Test instructor",
            "instructor": True,
        }
        instructor = self.create_instructor(**instructor_data)

        session_data = {
            "name": "Test session",
            "instructor_id": instructor.id,
            "course_id": course.id,
            "attendee_ids": [(6, 0, [instructor.id])],
        }
        with self.assertRaises(ValidationError):
            self.Session.create(session_data)

    def test_30_compute_perc_taken_seats(self):
        """
        Test compute perc taken seats.
        """
        session_form = Form(self.Session)
        session_form.number_seats = 10
        session_form.taken_seats = 5

        perc_taken_seats = (session_form.taken_seats / session_form.number_seats) * 100

        self.assertEqual(
            session_form.perc_taken_seats, perc_taken_seats,
            f"This must be equal to {perc_taken_seats}.",
        )

    def test_40_number_seats_less_than_zero(self):
        """
        Test number_seats less than zero.
        """
        session_form = Form(self.Session)

        with self.assertLogs(level="WARNING"):
            session_form.number_seats = -5

    def test_50_seats_taken_greater_than_number_of_seats(self):
        """
        Test taken_seats greater than number_seats.
        """
        session_form = Form(self.Session)

        with self.assertLogs(level="WARNING"):
            session_form.taken_seats = 20
            session_form.number_seats = 10
