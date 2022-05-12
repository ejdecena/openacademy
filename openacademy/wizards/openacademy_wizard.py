from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = "openacademy.wizard"
    _description = "Openacademy Wizard"

    session_ids = fields.Many2many(
        "openacademy.session",
        required=True,
        string="Sessions",
    )

    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="openacademy_wizard_partner_rel",
        column1="wizard_id",
        column2="partner_id",
        string="Partners",
    )

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        model = self.env.context.get("active_model")
        session_ids = self.env.context.get("active_ids")
        if model == "openacademy.session" and session_ids:
            sessions = [(6, 0, session_ids)]
            result.update({"session_ids": sessions})
        return result

    def save_wizard(self):
        for session in self.session_ids:
            session.attendee_ids |= self.partner_ids
