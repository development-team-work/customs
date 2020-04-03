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
    is_ribbon = fields.Boolean("Is a Ribbon?", default="True")
    is_medal=fields.Boolean("Is a Medal?")
    # ribbon_id=fields.Many2one('ribbon.medal',"Name Of Ribbon/Medal")
    ribbon_tmpl_id=fields.Many2one("product.template","Ribbon Template")
    medal_tmpl_id=fields.Many2one("product.template",string='Medal Template')
    force_id=fields.Many2one('ribbon.force',"Force Name")
    serial=fields.Integer("Serial")
    acquisition=fields.Many2one("ribbon.acquisition.rule","Acquisition Rule")
    shedule_date=fields.Date("Date of Declaration")
    service_length=fields.Integer("Service Length (Year)")

    # following column should be removed
    big_ribbon = fields.Many2one("product.product")
    small_ribbon = fields.Many2one("product.product")
    big_medal = fields.Many2one("product.product")
    small_medal = fields.Many2one("product.product")
    big_medal_set=fields.Many2one("product.product")
    small_medal_set=fields.Many2one("product.product")
