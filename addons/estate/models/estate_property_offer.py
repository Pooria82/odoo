from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity = fields.Integer(string='Validity (Days)', default=7)
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
                days_difference = (offer.date_deadline - create_date).days
                offer.validity = days_difference

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise UserError("An offer has already been accepted for this property.")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = 0.0
            offer.status = 'refused'
