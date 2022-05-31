from . commontest import CommonTest

from psycopg2.errors import CheckViolation, UniqueViolation
from odoo.tools import mute_logger


class TestCourse(CommonTest):

    def test_10_create_course(self):
        """
        Test create a course.
        """
        course_data = {
            "name": "Test course",
            "description": "This is a test description.",
            "responsible_id": self.user_admin.id,
        }
        course = self.create_course(**course_data)

        self.assertTrue(course.id, "This must be a valid id.")
        self.assertEqual(
            course.name, course_data["name"],
            f"This must be equal to {course_data['name']}.",
        )
        self.assertEqual(
            course.description, course_data["description"],
            f"This must be equal to {course_data['description']}.",
        )
        self.assertEqual(
            course.responsible_id.id, course_data["responsible_id"],
            f"This must be equal to {course_data['responsible_id']}.",
        )

    @mute_logger("odoo.sql_db")
    def test_20_description_and_title_different(self):
        """
        Test description and title different.
        """
        course_data = {
            "name": "Test course",
            "description": "Test course",
            "responsible_id": self.user_admin.id,
        }
        with self.assertRaises(CheckViolation):
            self.create_course(**course_data)

    @mute_logger("odoo.sql_db")
    def test_30_unique_course_name(self):
        """
        Test unique course name.
        """
        course_data = {
            "name": "Test course",
            "description": "Test description",
            "responsible_id": self.user_admin.id,
        }
        self.create_course(**course_data)

        with self.assertRaises(UniqueViolation):
            self.create_course(**course_data)

    def test_40_copy_course(self):
        """
        Test copy course.
        """
        course_data = {
            "name": "Test course",
            "description": "Test description",
            "responsible_id": self.user_admin.id,
        }
        self.create_course(**course_data)
        course = self.Course.search([("name", "=", course_data["name"])])
        copy_course = course.copy()
        self.assertEqual(
            copy_course.name, f"Copy of {course_data['name']}.",
            f"This must be equal to Copy of {course_data['name']}.",
        )
