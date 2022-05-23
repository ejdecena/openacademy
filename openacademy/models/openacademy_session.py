from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Session(models.Model):
    _name = "openacademy.session"
    _description = "This is the description of Session model."

    name = fields.Char()
    start_date = fields.Date(default=fields.Date.context_today)
    duration = fields.Integer()
    number_seats = fields.Integer("Number of seats")
    instructor_id = fields.Many2one(
        "res.partner",
        domain=[
            '|',
            ('instructor', '=', True),
            ('category_id.name', '=', 'Teacher / Level 1'),
            ('category_id.name', '=', 'Teacher / Level 2')
        ],
        ondelete="restrict",
    )
    course_id = fields.Many2one("openacademy.course", ondelete="restrict", required=True)
    attendee_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="openacademy_session_partner_rel",
        column1="session_id",
        column2="partner_id",
        string="Attendees",
    )
    taken_seats = fields.Integer()
    perc_taken_seats = fields.Float(digits=(3, 2), compute="_compute_perc_taken_seats", store=True)
    active = fields.Boolean(default=True)

    @api.depends("taken_seats", "number_seats")
    def _compute_perc_taken_seats(self):
        for session in self:
            if session.number_seats != 0:
                session.perc_taken_seats = 100*(session.taken_seats/session.number_seats)
            else:
                session.perc_taken_seats = 0

    @api.onchange("number_seats", "taken_seats")
    def _onchange_seats(self):
        if self.number_seats < 0:
            return {
                "warning": {
                    "title": "Error in the number of seats.",
                    "message": "The number of seats cannot be negative.",
                }
            }
        if self.taken_seats > self.number_seats:
            return {
                "warning": {
                    "title": "Error in the seating configuration.",
                    "message": "The number of participants cannot be greater than the number of seats.",
                }
            }

    @api.constrains("instructor_id")
    def _check_instructor(self):
        for session in self:
            if session.instructor_id in session.attendee_ids:
                raise ValidationError("The instructor cannot be attendee.")
