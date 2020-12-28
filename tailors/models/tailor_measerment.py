# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.osv.expression import get_unaccent_wrapper
import re


class tailorProductTemplate(models.Model):
    _inherit = "product.template"
    tailoring_item = fields.Boolean("Is a Tailoring Item?", default="True")

class tailoringItemAttributes(models.Model):
    _name="tailor.item.attribute"
    _description="Attribute of the tailoring items i;e Pocket, loops, shape etc"
    item_ids=fields.Many2many("tailor.item","tailor_item_attribute_rel","attribute_ids",'item_ids',"item Name")
    name=fields.Char("Name")
    value=fields.Char("Value")
    default_value=fields.Char("Default Value")
# class tailoringAttributeValues(models.Model):
#     _name="tailor.item.attribute.value"
#     _description="Attribute values of the tailoring items i;e Pocket=1, loops=3, shape etc"
#     atribute_ids=fields.Many2many("tailor.item.attribute","tailor_item_attribute_rel","Attribute")
#     name=fields.Char("Name")
#     value=fields.Char("Value")
#     default_value=fields.Char("Default Value")
class tailoringItems(models.Model):
    _name='tailor.item'
    _description="input Name of Tailoring Items Here"
    name=fields.Char('Name')
    attribute_ids=fields.Many2many("tailor.item.attribute","tailor_item_attribute_rel","item_ids","attribute_ids","Attributes")
    product_tmpl_id = fields.Many2one('product.template', required=True, ondelete='restrict', auto_join=True,
                                 string='Related product', help='Product-related data of the Tailoring Item')
    @api.onchange
    def update_product_template(self):
        for rec in self:
            rec.name.tailoring_item=True

    _sql_constraints = [
        ('product_uniq', 'unique(name)',
         "The product Template  must be unique, this Product is already assigned to another Item."),
        ('name_tmpl_uniq','unique(name,product_tmpl_id)',
         "The item name and product template must be unique")
    ]
class TailoringMeaserments(models.Model):
    _name="tailor.measerment"
    _description="Customers Measerment of a tailoring Item"
    name=fields.Char("Name",compute="get_measerment_name")
    tailor_item_id=fields.Many2one("tailor.item","Item Name")
    partner_id=fields.Many2one('res.partner',"Person")
    attribute_value_ids=fields.One2many("tailor.measerment.attribute.value","measerment_id")
    measerment=fields.Char("Measerments")
    special_note=fields.Char("Note")
    @api.model
    def get_measerment_name(self):
        for rec in self:
            namestr=" "
            if rec.tailor_item_id.name:
                namestr=rec.tailor_item_id.name
            if rec.partner_id.name:
                if namestr:
                    namestr=namestr +" "+rec.partner_id.name
            rec.name=namestr
    _sql_constraints = [
        ('product_uniq', 'unique(tailor_item_id,partner_id)',
         "Measerment of an item must be unique for a Customer, This customer allready has measerment for this Item.")
    ]

class tailorMeasermentAttributeValue(models.Model):
    _name="tailor.measerment.attribute.value"
    _description="Personal attribute values for Item"
    measerment_id=fields.Many2one("tailor.measerment")
    partner_id=fields.Many2one('res.partner',"Person",related="measerment_id.partner_id")
    attribute_id=fields.Many2one('tailor.item.attribute','Attribute')
    value=fields.Char("Value")
    _sql_constraints = [
        ('measerment_attribute_uniq', 'unique(measerment_id,attribute_id)',
         "Measerment and attribute combination must be unique.")
    ]