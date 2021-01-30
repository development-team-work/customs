# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError
import re

class tailorBodyPoint(models.Model):
    _name='tailor.body.point'
    _description="Point of body to measer by tailors"
    name=fields.Char("Points",help="name of the points to measer",translate="True")
    tailor_item_ids=fields.Many2many("tailor.item",'tailor_item_body_point_rel','body_point_ids','tailor_item_ids')
    details=fields.Char("description")
class resPartnerInherit(models.Model):
    _inherit='res.partner'
    measerments=fields.One2many('tailor.party.measerment.value','partner_id')
    gender=fields.Selection([
        ('m', "Male"),
        ('f', "Female")
    ],string="Gender",default="m")
    select_item=fields.Many2one("tailor.item") # this is for show/hide the body point in measerments
    @api.onchange('select_item')
    def select_item_changed(self):
        for rec in self:
            for point in rec.select_item.body_point_ids:
                if point not in rec.measerments.body_point:
                    self.env['tailor.party.measerment.value'].create({'partner_id':rec.id,'body_point':point.id})
class tailorPartyMeasermentvalue(models.Model):
    _name='tailor.party.measerment.value'
    _description="body measurments for partner"
    partner_id=fields.Many2one('res.partner',"Person")
    body_point=fields.Many2one('tailor.body.point',"Measerment Point")
    point_value=fields.Char('Value')
    _sql_constraints = [
        ('partner_pointe_uniq', 'unique(body_point,partner_id)',
         "body point must be unique for Partner.")
    ]

class tailoringItems(models.Model):
    _name='tailor.item'
    _description="input Name of Tailoring Items Here"
    name=fields.Char('Name')
    attribute_ids=fields.Many2many("tailor.item.attribute","tailor_item_attribute_rel","item_ids","attribute_ids","Attributes")
    # attribute_template_id=fields.One2many('tailor.item.attribute.template','item_id',"Template Id")
    related_to = fields.Selection(string='Depends On (Product/Template)', selection=[
        ('template', 'Product Template'),
        ('product', 'Product'), ],
             help='Select dependency ie: Product Template, Product .', default='template')
    product_tmpl_id = fields.Many2one('product.template', ondelete='restrict', auto_join=True,
                                 string='product Template', help='Product-template related data of the Tailoring Item')
    product_id = fields.Many2one('product.product', ondelete='restrict', auto_join=True,
                                 string='Related product', help='Product-related data of the Tailoring Item')
    # measerment_line_ids=fields.One2many('tailor.item.measerment.line','tailor_item_id')
    body_point_ids = fields.Many2many("tailor.body.point", 'tailor_item_body_point_rel',
                                       'tailor_item_ids', 'body_point_ids')

    _sql_constraints = [
        ('item_uniq', 'unique(name)',
         "The product Template  must be unique, this Product is already assigned to another Item."),
        ('item_product_tmpl_uniq','unique(name,product_tmpl_id,product_id)',
         "The product template and product combination must must be unique for an Item")
    ]
    def get_item(self,product):
        if product.id:
            item=self.env['tailor.item'].search([('product_id','=',product.id)])
            if len(item)==0:
                item = self.env['tailor.item'].search([('product_tmpl_id', '=', product.product_tmpl_id.id),('product_id','=',False)])
            return item
        return False
class tailoringItemAttributeTemplate(models.Model):
    _name='tailor.item.attribute.template'
    _description="Tailoring Item Template "
    name=fields.Char('Name',translate="True",required="True")
    item_id=fields.Many2one('tailor.item',"Item")
    attribute_line_ids=fields.One2many("tailor.item.attribute.template.value","item_template_id","Values")
    _sql_constraints = [
        ('name_uniq', 'unique(name)',
         "The Template name  must be unique, this name is already assigned to another Template.")
    ]
    @api.onchange('item_id')
    def item_id_changed(self):
        for rec in self:
            data=[]
            for attrib in rec.item_id.attribute_ids:
                newline=self.env["tailor.item.attribute.template.value"].create({'item_template_id':rec.id,'attribute_id':attrib.id})
                data.append(newline.id)
            rec.attribute_line_ids=[(6,0,data)]

class tailoringItemAttributes(models.Model):
    _name="tailor.item.attribute"
    _description="Attribute of the tailoring items i;e Pocket, loops, shape etc"
    item_ids=fields.Many2many("tailor.item","tailor_item_attribute_rel","attribute_ids",'item_ids',"Items")
    name=fields.Char("Name")
    details=fields.Char("Details")
    # value=fields.Char("Value")
    # default_value=fields.Char("Default Value")
class tailorItemAttributeValueTemplate(models.Model):
    _name="tailor.item.attribute.template.value"
    _description="Template for attribute values for Item"
    item_template_id=fields.Many2one('tailor.item.attribute.template','Item Template')
    item_id=fields.Many2one('tailor.item',related="item_template_id.item_id")
    name=fields.Char("Name",related="item_template_id.name", translate="True")
    attribute_id=fields.Many2one('tailor.item.attribute','Attribute')
    value=fields.Char("Value")
    _sql_constraints = [
        ('template_attribute_uniq', 'unique(attribute_id,item_template_id)',"Attribute must be unique for Item Template.")
    ]

# class tailorItemMeasermentline(models.Model):
#     _name='tailor.item.measerment.line'
#     _description="Item wise Point list of tailor"
#     _order = 'sequence'
#     name=fields.Char("Name",translate="True")
#     tailor_item_id=fields.Many2one("tailor.item",'Tailor Item')
#     measerment_point_id=fields.Many2one('tailor.measerment.point','Point')
#     sequence=fields.Integer("Sequence")
#     details=fields.Char("Description")
#     _sql_constraints = [
#         ('item_measerment_point_uniq', 'unique(tailor_item_id,measerment_point_id)',

#          "Measerment Point  must be unique, this Point is already asigned."),
#         ('sequence_uniq', 'unique(sequence,tailor_item_id)',
#          "Sequence must be unique"),
#         ('name_uniq', 'unique(tailor_item_id,name)',
#          "Name must be unique")
#     ]

class tailorProductTemplate(models.Model):
    _inherit = "product.template"
    tailoring_item = fields.Boolean("Is a Tailoring Item?", default="False")
    item_id=fields.One2many('tailor.item','product_tmpl_id')
class tailorProductProduct(models.Model):
    _inherit = "product.product"
    tailoring_item_product = fields.Boolean("Is a Tailoring Item?", default="False")
    item_id=fields.One2many('tailor.item','product_id')
# class tailoringAttributeValues(models.Model):
#     _name="tailor.item.attribute.value"
#     _description="Attribute values of the tailoring items i;e Pocket=1, loops=3, shape etc"
#     atribute_ids=fields.Many2many("tailor.item.attribute","tailor_item_attribute_rel","Attribute")
#     name=fields.Char("Name")
#     value=fields.Char("Value")
#     default_value=fields.Char("Default Value")

# class TailoringMeasermentLine(models.Model):
#     _name="tailor.measerment.line"
#     _description="Customers Measerment point values of a tailoring Item"
#     point_id=fields.Many2one("tailor.measerment.point",'Point')
#     measerment_id=fields.Many2one("tailor.measerment")
#     value=fields.Char("Value")
#
# class TailoringMeaserments(models.Model):
#     _name="tailor.measerment"
#     _description="Customers Measerment of a tailoring Item"
#     name=fields.Char("Name",compute="get_measerment_name")
#     tailor_item_id=fields.Many2one("tailor.item","Item Name")
#     partner_id=fields.Many2one('res.partner',"Person")
#     product_tmpl_id=fields.Many2one('product.template',related="tailor_item_id.product_tmpl_id")
#     product_id=fields.Many2one('product.product',related="tailor_item_id.product_id")
#     order_id=fields.Many2one("sale.order","last Order")
#     attribute_template_id=fields.Many2one('tailor.item.attribute.template','Template')
#     attribute_value_ids=fields.One2many("tailor.measerment.attribute.value","measerment_id")
#     measerment_lines=fields.One2many("tailor.measerment.line","measerment_id")
#     special_note=fields.Char("Note")
#     @api.onchange('tailor_item_id')
#     def tailor_item_id_on_change(self):
#         for rec in self:
#             for val in rec.measerment_lines:
#                 val.unlink()
#             for val in self.env['tailor.item.measerment.line'].search([('tailor_item_id','=',rec.tailor_item_id.id)], order="sequence asc"):
#                 self.env['tailor.measerment.line'].create({'point_id':val.id,'measerment_id':rec.id})
#
#     def check_measerment_party_product(self,partner_id,product_id):
#         product=self.env["product.product"].search([('id','=',product_id)])
#         rec=self.search([('partner_id','=',partner_id),('product_id','=',product_id)])
#         if not rec.id:
#             rec=self.search([('partner_id','=',partner_id),('product_tmpl_id','=',product.product_tmpl_id.id)])
#         if not rec.id:
#             if product.item_id:
#                 print("Product is an Item")
#             elif product.product_tmpl_id.item_id.id:
#                 print("Product template is an Item")
#         if not rec.id:
#             item_id=product.item_id
#             if not item_id.id:
#                 item_id=product.product_tmpl_id.item_id
#             if not item_id:
#                 message="create item for product"+product.name
#                 raise UserError(message)
#             print(item_id)
#
#             print('product measerment is none')
#         return rec
#
#     @api.onchange('attribute_template_id')
#     def attribute_template_onchange(self):
#         values={}
#         for rec in self:
#             newRecords=[]
#             for line in rec.attribute_template_id.value_line_ids:
#                 # todo here to copy default values from template
#                 values.update({'attribute_id':line.attribute_id.id,'value':line.value,'measerment_id':rec.id})
#                 newRecord=self.env["tailor.measerment.attribute.value"].create(values)
#                 newRecords.append(newRecord.id)
#             rec.attribute_value_ids=[(6,0,newRecords)]
#
#     @api.model
#     def get_measerment_party_product(self,party,product):
#         result=self.check_measerment_party_product(party.id,product.id)
#         print(result)
#     @api.model
#     def get_measerment_name(self):
#         for rec in self:
#             namestr=" "
#             if rec.tailor_item_id.name:
#                 namestr=rec.tailor_item_id.name
#             if rec.partner_id.name:
#                 if namestr:
#                     namestr=namestr +" "+rec.partner_id.name
#             rec.name=namestr
#     _sql_constraints = [
#         ('product_uniq', 'unique(tailor_item_id,partner_id)',
#          "Measerment of an item must be unique for a Customer, This customer allready has measerment for this Item.")
#     ]
#
# class tailorMeasermentAttributeValue(models.Model):
#     _name="tailor.measerment.attribute.value"
#     _description="Personal attribute values for Item"
#     name=fields.Char("Name",compute='get_name')
#     measerment_id=fields.Many2one("tailor.measerment")
#     partner_id=fields.Many2one('res.partner',"Person",related="measerment_id.partner_id")
#     tailor_item_id=fields.Many2one("tailor.item","Item Name",related="measerment_id.tailor_item_id")
#     attribute_id=fields.Many2one('tailor.item.attribute','Attribute')
#     value=fields.Char("Value")
#     _sql_constraints = [
#         ('measerment_attribute_uniq', 'unique(measerment_id,attribute_id)',
#          "Attribute Name must be unique.")
#     ]
#     @api.onchange('attribute_id')
#     def get_name(self):
#         for rec in self:
#             if rec.attribute_id.name and rec.value:
#                 rec.name=rec.attribute_id.name + "-"+rec.value

#