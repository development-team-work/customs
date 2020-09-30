# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime


class ribbonMedalForce(models.Model):
    _inherits = {'product.attribute.value': 'attribute_id'}
    _name="ribbon.force"
    _description = "Name of the Force ie; Police, Army ..."
    name=fields.Char("Force Name")
    attribute_id=fields.Many2one('product.attribute.value',"Product Attribute",required="True",ondelete="cascade")

    image=fields.Binary("Logo")
    description=fields.Char("Description")
    ribbon_ids=fields.Many2many("ribbon.regulation",'ribbon_force_prb_rel',string="ribbons")
    ranks=fields.One2many("ribbon.rank",'force_id')

class ribbonMedalForceUnit(models.Model):
    _name = "ribbon.force.unit"
    _description = "Name of Units of a Force"
    name = fields.Char("Unit",translate=True)
    divsign=fields.Binary("Div Sign")
    image=fields.Binary("Div Sign", compute='_compute_image_1920', inverse='_set_image_1920')
    force_name=fields.Many2one("ribbon.force","Force")
    address=fields.Char("address",translate=True)
    parent_unit=fields.Many2one("ribbon.force.unit","Parent Unit",translate=True)
    child_units = fields.One2many('ribbon.force.unit', 'parent_unit', string='Child Units')
    chief_rank=fields.Many2one("ribbon.rank","Rank of Chief",translate=True)
    chief=fields.Many2one("ribbon.post","Chief",translate=True)

    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Post Code', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    phone = fields.Char('Phone', tracking=50)
    mobile = fields.Char('Mobile')

    def _compute_image_1920(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            if record.divsign==False:
                record.image =  record.parent_unit.image
            else:
                record.image = record.divsign

    def _set_image_1920(self):
        for rec in self:
            rec.divsign=rec.image

class RibbonMedalsPost(models.Model):
    _name="ribbon.post"
    _description = "Post of a force different of his rank ie; Comissioner, director etc"
    name=fields.Char("Name of The Post",translate=True)
    code=fields.Char("Abbreviation",translate=True)
    force_name=fields.Many2one("ribbon.force","Force")
