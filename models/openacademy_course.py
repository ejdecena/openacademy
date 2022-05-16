from odoo import models, fields


class Course(models.Model):
    _name = "openacademy.course"
    _description = "This is the description of course model."

    name = fields.Char("Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one("res.users", ondelete="restrict")
    session_ids = fields.One2many("openacademy.session", string="Sessions", inverse_name="course_id")

    _sql_constraints = [
        ("description_and_title_different",
            "CHECK(name != description)",
            "The title and description of the course must be different."),

        ("unique_course_name",
            "UNIQUE(name)",
            "The name of the course must be unique."),
    ]

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.update({
            "name": f"Copy of {self.name}.",
        })
        return super().copy(default)
