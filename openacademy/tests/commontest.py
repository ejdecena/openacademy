from odoo.tests import common


class CommonTest(common.TransactionCase):
    """Test Base class from which all tests inherit."""

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.user_admin = self.env.ref("base.user_admin")
        self.Course = self.env["openacademy.course"].with_user(self.user_admin)
        self.Session = self.env["openacademy.session"].with_user(
            self.user_admin
        )
        self.Instructor = self.env["res.partner"].with_user(self.user_admin)

    def create_course(self, name, description, responsible_id):
        """Create and return a course object."""
        course = self.Course.create({
            "name": name,
            "description": description,
            "responsible_id": responsible_id,
        })
        return course

    def create_instructor(self, name, instructor: bool):
        """Create and return an instructor object."""
        instructor = self.Instructor.create({
            "name": name,
            "instructor": instructor,
        })
        return instructor

    def create_session(
        self, name, number_seats, instructor_id, taken_seats, course_id
    ):
        """Create and return a session object."""
        session = self.Session.create({
            "name": name,
            "number_seats": number_seats,
            "instructor_id": instructor_id,
            "taken_seats": taken_seats,
            "course_id": course_id,
        })
        return session
