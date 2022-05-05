from odoo import models, fields

class Course(models.Model):
    _name = "openacademy.course"
    _description = "This is the description of course model."

    name = fields.Char("Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one("res.users", ondelete="restrict")
    session_ids = fields.One2many("openacademy.session", string="Sessions", inverse_name="course_id")
