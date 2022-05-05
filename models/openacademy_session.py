from odoo import models, fields

class Session(models.Model):
    _name = "openacademy.session"
    _description = "This is the description of Session model."

    name = fields.Char()
    start_date = fields.Date()
    duration = fields.Integer()
    number_seats = fields.Integer("Number of seats")
    instructor_id = fields.Many2one("res.partner", ondelete="restrict")
    course_id = fields.Many2one("openacademy.course", ondelete="restrict", required=True)
