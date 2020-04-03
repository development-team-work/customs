# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime
class ribbonMedalForce(models.Model):
    _name="ribbon.force"
    _description = "Name of the Force ie; Police, Army ..."
    name=fields.Char("Force Name")
    image=fields.Binary("Logo")
    description=fields.Char("Description")
    ribbon_ids=fields.Many2many("ribbon.regulation",'ribbon_force_prb_rel',string="ribbons")
    ranks=fields.One2many("ribbon.rank",'force_id')

# class ribbonMedal(models.Model):
#     _name="ribbon.medal"
#     name=fields.Char("Ribbon Name")
#     is_ribbon=fields.Boolean("Is a Ribbon?",default="True")
#     is_medal=fields.Boolean("Is a Medal?")
#     ribbon_template=fields.Many2one("product.template","Ribbon Template")
#     medal_template=fields.Many2one("product.template","Medal Template")
class ribbonMedalExtension(models.Model):
    _name="ribbon.extension"
    name=fields.Char("Ribbon Extensions")
    image=fields.Binary("extension Image")
    related_product=fields.Many2one("product.product")
    product_tmpl=fields.Many2one("product.template")
class RibbonMedalRibbonProduct(models.Model):
    _name="ribbon.ribbon.product"
    _description = "ribbon and medal relation with product"
    name=fields.Char("Name")
    big_ribbon=fields.Many2one("product.product")
    small_ribbon=fields.Many2one("product.product")
    big_medal=fields.Many2one("product.product")
    small_medal=fields.Many2one("product.product")


class ribbonMedalRanks(models.Model):
    _name = "ribbon.rank"
    _description = "Name of Ranks for Forces"
    name = fields.Char("Rank Name",translate=True)
    force_id=fields.Many2one("ribbon.force","Force")
    superiority=fields.Integer("Superiority")
    code=fields.Char("Rank Code",translate=True)

class ribbonMedalForceUnit(models.Model):
    _name = "ribbon.force.unit"
    _description = "Name of Units of a Force"
    name = fields.Char("Unit",translate=True)
    force_name=fields.Many2one("ribbon.force","Force")
    address=fields.Char("address",translate=True)
    parent_unit=fields.Many2one("ribbon.force.unit","Parent Unit",translate=True)
    chief_rank=fields.Many2one("ribbon.rank","Rank of Chief",translate=True)
    chief=fields.Many2one("ribbon.post","Chief",translate=True)

class RibbonMedalsPost(models.Model):
    _name="ribbon.post"
    _description = "Post of a force different of his rank ie; Comissioner, director etc"
    name=fields.Char("Name of The Post",translate=True)
    code=fields.Char("Abbreviation",translate=True)
    force_name=fields.Many2one("ribbon.force","Force")

class ribbonMedalMissions(models.Model):
    _name="ribbon.mission"
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