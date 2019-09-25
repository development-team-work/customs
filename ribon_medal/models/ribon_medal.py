# -*- coding: utf-8 -*-

from eagle import api, fields, models, _
class ribonForce(models.Model):
    _name="ribon.force"
    _description = "Name of the Force ie; Police, Army ..."
    name=fields.Char("Force Name")
    ribon_ids=fields.Many2many("ribon.medal",'ribon_force_medal_rel',column1='force_id',column2="ribon_id",string="Ribons")

class ribonMedal(models.Model):
    _inherits = {"product.template":"product_id"}
    _name="ribon.medal"
    is_ribon=fields.Boolean("Ribon?", default="True")
    ribbon_image=fields.Binary("Ribon Image")
    medal_image=fields.Binary("Medal Image")
    is_medal=fields.Boolean("Is a Medal")
    force_ids=fields.Many2many("ribon.medal",'ribon_force_medal_rel',column1='force_id', column2="ribon_id", string="For the Force",)
    declared_date=fields.Date("Started From")
    service_length=fields.Integer("service Length")
    ribon_category=fields.Many2many("ribon.category")
    product_id=fields.Many2one('product.template',)
class ribonCategory(models.Model):
    _name="ribon.category"
    _description="determines how the ribon is accuired ie; service lenth,service place or awards"
    name=fields.Char("category")
    description=fields.Char("Description")
class ribonSerial(models.Model):
    _name="ribon.serial"
    _description = "Force wise serial of ribon and medals"
    name=fields.Many2one('ribon.medal')
    force_id=fields.Many2one('ribon.force',"Force Name")
    serial=fields.Integer("Serial")
    ribbon_image = fields.Binary("Ribon Image")
    medal_image = fields.Binary("Medal Image")
