# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv.expression import get_unaccent_wrapper
import datetime
import re

from odoo.addons.base.models.res_partner import Partner


class ribbonAcquisitionRule(models.Model):
    _name = "ribbon.acquisition.rule"
    _description = "determines how the ribbon is accuired ie; service lenth,service place or awards"
    name = fields.Char("Accquisition", translate=True)
    description = fields.Char("Description", translate=True)


class atributeFilterByProductTemplate(models.Model):
    _name = "ribbon.regulation.attribute.filter"
    _discription = " filter product Attributes for Ribbo Regulations"
    regulation_id=fields.Many2many("ribbon.regulation")
    attribute_id = fields.Many2one("product.attribute", "Attribute")
    attribute_value_id = fields.Many2one("product.attribute.value", "Value")


class productTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"
    ribbon_regulation_ids = fields.Many2many('ribbon.regulation',"regulation_attribute_rel")


class ribbonRegulation(models.Model):
    _name = "ribbon.regulation"
    _description = "Force wise shedule of ribbon and medals"
    name = fields.Char("Name")
    is_ribbon = fields.Boolean("Is a Ribbon?", default="True")
    is_medal = fields.Boolean("Is a Medal?")
    attribute_ids = fields.Many2many("product.attribute")
    attribute_value_ids = fields.Many2many('product.template.attribute.value', relation='regulation_attribute_rel',
                                           string="Attribute Values")
    attribute_value_list = fields.Char("attributes")
    ribbon_ids = fields.Many2many('product.product', domain="[('product_tmpl_id', '=',ribbon_tmpl_id)]")
    ribbon_id = fields.Many2one('product.product', "Defalt Ribbon")
    ribbon_tmpl_id = fields.Many2one("product.template", "Ribbon Template")
    medal_tmpl_id = fields.Many2one("product.template", string='Medal Template')
    force_id = fields.Many2one('ribbon.force', "Force Name")
    serial = fields.Integer("Serial")
    acquisition = fields.Many2one("ribbon.acquisition.rule", "Acquisition Rule")
    shedule_date = fields.Date("Date of Declaration")
    service_length = fields.Integer("Service Length (Year)")

    # following column should be removed
    big_ribbon = fields.Many2one("product.product")
    small_ribbon = fields.Many2one("product.product")
    big_medal = fields.Many2one("product.product")
    small_medal = fields.Many2one("product.product")
    big_medal_set = fields.Many2one("product.product")
    small_medal_set = fields.Many2one("product.product")

    @api.onchange('ribbon_tmpl_id')
    def get_attribute_ids(self):
        data = []
        for value in self.env["product.template.attribute.value"].search(
                [('product_tmpl_id', '=', self.ribbon_tmpl_id.id)]):
            data.append(value.id)
        self.attribute_value_ids = [(6, 0, data)]
        self.attribute_value_list=data
        print('pp')
        print(self.attribute_value_list)

    @api.onchange("attribute_value_ids")
    def get_products(self):
        for rec in self:
            prod_list = []
            attribute_list = []

            for value in rec.attribute_value_ids:
                attribute_list.append(value._origin.id)

            for pd in self.env["product.product"].search([('product_tmpl_id', '=', self.ribbon_tmpl_id.id)]):
                rem = False
                prod_list.append(pd.id)
                for attrbt in pd.product_template_attribute_value_ids:
                    if attrbt.id not in attribute_list:
                        rem = True
                if rem:
                    prod_list.remove(pd.id)
            self.ribbon_ids=[(6,0,prod_list)]
            print(self.ribbon_ids)
            print(prod_list)