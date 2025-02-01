from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types. Lower is better.")

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers"
    )
    offer_count = fields.Integer(
        string="Offer Count", compute="_compute_offer_count", store=True
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)',
         'The property type name must be unique.')
    ]

    # @api.constrains('name')
    # def _check_unique_case_insensitive_name(self):
    #     """Ensure the name is unique regardless of case sensitivity."""
    #     for record in self:
    #         existing_type = self.env['estate.property.type'].search([
    #             ('id', '!=', record.id),
    #             ('name', '=ilike', record.name)
    #         ])
    #         if existing_type:
    #             raise ValidationError("Property Type Name must be unique (case insensitive)!")

    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties',
    )
