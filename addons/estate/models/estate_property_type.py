from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(string='Name', required=True)

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
