from odoo import models, fields

class Partner(models.Model):
    _inherit = "res.partner"

    instructor = fields.Boolean()
    session_ids = fields.Many2many(
        comodel_name="openacademy.session",
        relation="openacademy_session_partner_rel",
        column1="partner_id",
        column2="session_id",
        string="Sessions",
    )
