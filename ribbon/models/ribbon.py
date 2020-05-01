# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime
class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange('name')
    def onchange_method(self):
        # todo here to implement automatic name change of related medal and ribbon product
        self.env['ribbon.ribbon.ribbontest'].search([('product_tmpl_id','=',self.id)]).onchange_name
class medaltestProduct(models.Model):
    _inherits ={'product.template':'product_tmpl_id'}
    _name='ribbon.medaltest'
    has_medal=fields.Boolean("Medal?")
    ribbon_id=fields.Many2one('ribbon.ribbon.ribbontest')

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
    _inherits = {'product.template':'product_template_id'}
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
        if self.is_ribbon==True:
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

class ribbonMedalForceUnit(models.Model):
    _name = "ribbon.force.unit"
    _description = "Name of Units of a Force"
    name = fields.Char("Unit",translate=True)
    divsign=fields.Binary("Div Sign")
    image=fields.Binary("Div Sign", compute='_compute_image_1920', inverse='_set_image_1920')
    force_name=fields.Many2one("ribbon.force","Force")
    address=fields.Char("address",translate=True)
    parent_unit=fields.Many2one("ribbon.force.unit","Parent Unit",translate=True)
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