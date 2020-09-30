# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime
class ProductTemplate(models.Model):
    _inherit = "product.template"
    force_dependent=fields.Boolean("Depends on Force")
    is_ribbon_medal=fields.Boolean("Ribbon/Medal")
    @api.onchange('name')
    def onchange_method(self):
        # todo here to implement automatic name change of related medal and ribbon product
        # self.env['ribbon.ribbon.ribbontest'].search([('product_tmpl_id','=',self.id)]).onchange_name
        return

class ribbonMedalExtension(models.Model):
    _inherits = {'product.template':'product_tmpl_id'}
    _name="ribbon.extension"

class RibbonMedalRibbonProduct(models.Model):
    _name="ribbon.ribbon.product"
    _inherits ={'product.template':'product_tmpl_id'}
    _description = "ribbon and medal relation with product"

    is_medal=fields.Boolean("Medal?")
    medal_id=fields.Many2one('ribbon.medal.product')

    @api.onchange('name')
    def onchange_name(self):
        if self.medal_id.id:
            if self.medal_id.name==self.name.replace('Ribbon','medal'):
                return
            else:
                self.medal_id.name=self.name.replace('Ribbon','medal')
    @api.onchange("is_medal")
    def make_medal(self):
        self.ensure_one()
        if self.is_medal==True:
            if self.medal_id.id==False:
                # TODO here search medal product for this ribbon
                rec=self.env['ribbon.medal.product'].create({
                    "name":self.name +' Medal',
                    "ribbon_id":self.id,
                    "is_ribbon":True,
                })
                self.medal_id=rec.id
                self.is_medal=True

class RibbonMedalMedalProduct(models.Model):
    _name="ribbon.medal.product"
    _description = " medal relation with product"
    _inherits ={'product.template':'product_tmpl_id'}
    is_ribbon=fields.Boolean("Ribbon?")
    product_tmpl_id=fields.Many2one('product.template',"product Template",require=True)
    ribbon_id=fields.Many2one('ribbon.ribbon.product')

    @api.onchange('name')
    def onchange_name(self):
        if self.ribbon_id.id:
            if self.ribbon_id.name==self.name.replace('Medal','Ribbon'):
                return
            else:
                self.ribbon_id.name=self.name.replace('Medal','Ribbon')
    @api.onchange("is_ribbon")
    def make_ribbon(self):
        if self.is_ribbon==True and len(self.name)>0:
            if self.ribbon_id.id==False:

                rec=self.env['ribbon.ribbon.product'].create({
                    "name":self.name.replace('Medal','Ribbon'),
                    "is_medal":True,

                })
                self.ribbon_id=rec.id
                self.is_ribbon=True


class ribbonMedalRanks(models.Model):
    _name = "ribbon.rank"
    _description = "Name of Ranks for Forces"
    name = fields.Char("Rank Name",translate=True)
    force_id=fields.Many2one("ribbon.force","Force")
    superiority=fields.Integer("Superiority")
    code=fields.Char("Rank Code",translate=True)


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
#  Ribbon           serial
#  BPM Gal          100
#  BPM seba         110
#  pPM Gal          150
#  pPM seba         160
#  Ronotaroka       160

#  muktitaroka      160
#  joy padak          160
#  shamar padak          160
#  shangbidhan padak          160

#  Nirapatta padak          160

#  election 91 padak          160
#  election 96 padak          160
#  election 01 padak          160

#  BPA          160
#  PSC          160


#  IG Badge          160
#  IG Badge          160
#  IG Badge          160
#  IG Badge          160
#  IG Badge          160
#  IG Badge          160

#  RajatJayanti padak          160
#  RajatJayanti padak          160

#  seniority 3 padak          160
#  seniority 2 padak          160
#  seniority 1 padak          160
#  Un Mission          160
