# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv.expression import get_unaccent_wrapper
import datetime
import re

from odoo.addons.base.models.res_partner import Partner

class ribbonAcquisitionRule(models.Model):
    _name="ribbon.acquisition.rule"
    _description="determines how the ribbon is accuired ie; service lenth,service place or awards"
    name=fields.Char("Accquisition",translate=True)
    description=fields.Char("Description" ,translate=True)
class ribbonRegulation(models.Model):
    _name="ribbon.regulation"
    _description = "Force wise shedule of ribbon and medals"
    name=fields.Char("Name")
    # @api.onchange('ribbon_tmpl_id')
    # def ribbon_domain(self):
    #     if  self.ribbon_tmpl_id:
    #         #todo here to create domain for products that have the product_tmpl_id and attribute Id
    #         big_products=self.env['product.product'].search([('product_tmpl_id','=',self.ribbon_tmpl_id.id),('product_template_attribute_value_ids.name','=','Big'),('product_template_attribute_value_ids.name','=','Ribbon')])
    #         small_products=self.env['product.product'].search([('product_tmpl_id','=',self.ribbon_tmpl_id.id),('product_template_attribute_value_ids.name','=','Small'),('product_template_attribute_value_ids.name','=','Ribbon')])
    #         big_domain=[('id', 'in', big_products.ids)]
    #         small_domain=[('id', 'in', small_products.ids)]
    #
    #         return {'domain': {'default_big_ribbon_id': big_domain,'default_small_ribbon_id': small_domain}}
    #
    # @api.onchange('medal_tmpl_id')
    # def medal_domain(self):
    #     if  self.medal_tmpl_id:
    #         # Dynamic Domain Ashraf
    #         big_products=self.env['product.product'].search([('product_tmpl_id','=',self.medal_tmpl_id.id),('product_template_attribute_value_ids.name','=','Big'),('product_template_attribute_value_ids.name','=','Medal')])
    #         small_products=self.env['product.product'].search([('product_tmpl_id','=',self.medal_tmpl_id.id),('product_template_attribute_value_ids.name','=','Small'),('product_template_attribute_value_ids.name','=','Medal')])
    #         big_domain=[('id', 'in', big_products.ids)]
    #         small_domain=[('id', 'in', small_products.ids)]
    #         return {'domain': {'default_big_medal_id': big_domain,'default_small_medal_id': small_domain}}


    is_ribbon = fields.Boolean("Is a Ribbon?", default="True")
    ribbon_tmpl_id=fields.Many2one("product.template","Ribbon Template" ,domain="[('attribute_line_ids.value_ids.name', '=', 'Ribbon')]")
    ribbon_price=fields.Float('Ribbon Price')
    is_medal=fields.Boolean("Is a Medal?")
    ribbon_image = fields.Binary("",related='ribbon_tmpl_id.image_1920'  )
    # product_tmpl_id=fields.Many2one("product.template","Product Template")

    default_big_ribbon_id=fields.Many2one("product.product","Default Big Ribbon" )
    default_small_ribbon_id=fields.Many2one("product.product","Default Small Ribbon")
    default_big_medal_id = fields.Many2one("product.product", "Default Medal")
    default_small_medal_id = fields.Many2one("product.product", "Default Medal")
    medal_tmpl_id=fields.Many2one("product.template",string='Medal Template' ,domain="[('attribute_line_ids.value_ids.name', '=', 'Medal')]")
    medal_image = fields.Binary("", related='medal_tmpl_id.image_1920')
    force_id=fields.Many2one('ribbon.force',"Force Name")
    force_name=fields.Char('Force Name',related="force_id.name")
    attribute_id=fields.Many2one('product.attribute.value',related="force_id.attribute_id")
    serial=fields.Integer("Serial")
    acquisition=fields.Many2one("ribbon.acquisition.rule","Acquisition Rule")
    acquisition_rule=fields.Char("Acquisition Rule",related='acquisition.name')
    shedule_date=fields.Date("Date of Declaration")
    service_length=fields.Integer("Service Length (Year)")
    default_extension = fields.Many2one(comodel_name="ribbon.extension", string="Extension", required=True, )
    extension_image = fields.Binary(string="Extension Image", related="default_extension.image_1920"  )
    # following column should be removed
    big_ribbon = fields.Many2one("product.product")
    small_ribbon = fields.Many2one("product.product")
    big_medal = fields.Many2one("product.product")
    small_medal = fields.Many2one("product.product")
    big_medal_set=fields.Many2one("product.product")
    small_medal_set=fields.Many2one("product.product")