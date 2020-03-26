# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime
class ribbonMedalForce(models.Model):
    _name="ribbon_bk.medal.force"
    _description = "Name of the Force ie; Police, Army ..."
    name=fields.Char("Force Name")
    image=fields.Binary("Logo")
    description=fields.Char("Description")
    ribbon_ids=fields.Many2many("ribbon_bk.medal",'ribbon_force_medal_rel',column1='force_id',column2="ribbon_id",string="ribbons")
    ranks=fields.One2many("ribbon_bk.medal.rank",'force_id')

class ribbonMedal(models.Model):
    _name="ribbon_bk.medal"
    name=fields.Char("Ribbon Name")
    is_ribbon=fields.Boolean("Is a Ribbon?",default="True")
    is_medal=fields.Boolean("Is a Medal?")
    ribbon_template=fields.Many2one("product.template","Ribbon Template")
    ribbon_set_tmpl=fields.Many2one("product.template","Ribbon Set Template")
    medal_template=fields.Many2one("product.template","Medal Template")
    medal_set_tmpl=fields.Many2one("product.template","Medal Set Template")
class ribbonMedalExtension(models.Model):
    _name="ribbon_bk.medal.extension"
    name=fields.Char("Ribbon Extensions")
    image=fields.Binary("extension Image")
    related_product=fields.Many2one("product.product")
class RibbonMedalRibbonProduct(models.Model):
    _name="ribbon_bk.medal.ribbon_bk.product"
    _description = "ribbon_bk and medal relation with product"
    name=fields.Char("Name")
    big_ribbon=fields.Many2one("product.product")
    small_ribbon=fields.Many2one("product.product")
    big_medal=fields.Many2one("product.product")
    small_medal=fields.Many2one("product.product")
class ribbonAcquisitionRule(models.Model):
    _name="ribbon_bk.medal.acquisition.rule"
    _description="determines how the ribbon_bk is accuired ie; service lenth,service place or awards"
    name=fields.Char("Accquisition",translate=True)
    description=fields.Char("Description" ,translate=True)

class ribbonRegulation(models.Model):
    _name="ribbon_bk.medal.regulation"
    _description = "Force wise shedule of ribbon_bk and medals"
    name=fields.Char("Name",related='ribbon_id.name')
    ribbon_id=fields.Many2one('ribbon_bk.medal',"Name Of Ribbon/Medal")
    ribbon_tmpl_id=fields.Integer("Ribbon Template",related="ribbon_id.ribbon_template.id")
    ribbon_set_tmpl_id=fields.Integer(related="ribbon_id.ribbon_set_tmpl.id")
    medal_tmpl_id=fields.Integer(related="ribbon_id.medal_template.id")
    medal_set_tmpl_id=fields.Integer(related="ribbon_id.medal_set_tmpl.id")
    force_id=fields.Many2one('ribbon_bk.medal.force',"Force Name")
    serial=fields.Integer("Serial")
    acquisition=fields.Many2one("ribbon_bk.medal.acquisition.rule","Acquisition Rule")
    shedule_date=fields.Date("Date of Declaration")
    service_length=fields.Integer("Service Length (Year)")
    big_ribbon = fields.Many2one("product.product")
    small_ribbon = fields.Many2one("product.product")
    big_medal = fields.Many2one("product.product")
    small_medal = fields.Many2one("product.product")
    big_medal_set=fields.Many2one("product.product")
    small_medal_set=fields.Many2one("product.product")
    ribbon_set=fields.Many2one("product.product")

class ribbonMedalRanks(models.Model):
    _name = "ribbon_bk.medal.rank"
    _description = "Name of Ranks for Forces"
    name = fields.Char("Rank Name",translate=True)
    force_id=fields.Many2one("ribbon_bk.medal.force","Force")
    superiority=fields.Integer("Superiority")
    code=fields.Char("Rank Code",translate=True)

class ribbonMedalForceUnit(models.Model):
    _name = "ribbon_bk.medal.force.unit"
    _description = "Name of Units of a Force"
    name = fields.Char("Unit",translate=True)
    force_name=fields.Many2one("ribbon_bk.medal.force","Force")
    address=fields.Char("address",translate=True)
    parent_unit=fields.Many2one("ribbon_bk.medal.force.unit","Parent Unit",translate=True)
    chief_rank=fields.Many2one("ribbon_bk.medal.rank","Rank of Chief",translate=True)
    chief=fields.Many2one("ribbon_bk.medal.post","Chief",translate=True)

class RibbonMedalsPost(models.Model):
    _name="ribbon_bk.medal.post"
    _description = "Post of a force different of his rank ie; Comissioner, director etc"
    name=fields.Char("Name of The Post",translate=True)
    code=fields.Char("Abbreviation",translate=True)
    force_name=fields.Many2one("ribbon_bk.medal.force","Force")

class ribbonMedalMissions(models.Model):
    _name="ribbon_bk.medal.mission"
    _description = "all about missions"
    partner_id=fields.Many2one('res.partner')
    name=fields.Char("Mission")
    country=fields.Char("Country")
    ext=fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),])