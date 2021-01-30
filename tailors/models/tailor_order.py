# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.osv.expression import get_unaccent_wrapper
import re
class TailorProductOrderLine(models.Model):
    _name='tailor.item.order.line'
    _description="tailoring products and Order line Relation, Suppose a Tunic is ordered which contains two tailoring products 1. Coat, 2.Pant"
    order_line_id=fields.Many2one('sale.order.line')
    order_qty = fields.Float('Qty', related='order_line_id.product_uom_qty')
    order_id=fields.Many2one('sale.order',related='order_line_id.order_id')
    product_id=fields.Many2one('product.product',"Product",related='order_line_id.product_id')
    item_id=fields.Many2one('tailor.item',"Item")
    item_tmpl_id = fields.Many2one('tailor.item.attribute.template', "Item Template")

class TailorOrderMeaserment(models.Model):
    _name = "tailor.order.measerment"
    _description = "Tailor Measerment for Items Per Order"
    item_id = fields.Many2one('tailor.item', "Item Name")
    item_tmpl_id = fields.Many2one('tailor.item.attribute.template', "Item Template")
    order_line_id=fields.Many2one('sale.order.line',"Order Line")
    order_id = fields.Many2one('sale.order', "Order No")
    partner_id=fields.Many2one("res.partner","Party",related="order_id.partner_id")
    measerment_lines = fields.Many2many('tailor.order.measerment.line','tailor_order_measerment_rel','measerment_id', "measerment_lines")
    attribute_lines = fields.Many2many('tailor.order.attribute.line','tailor_order_attribute_rel','measerment_id', "attribute_lines")
    # todo import attribute from template
    # @api.onchange('item_tmpl_id')
    # for rec in self:
    #     data=[]
    #     for attrib in rec.item_tmpl_id:
    #         newAttrib=self.env['tailor.order.attribute.line'].create({})

class TailorOrderMeasermentLine(models.Model):
    _name = "tailor.order.measerment.line"
    _description = "Tailor Measerment line for Items Per Order"
    measerment_id = fields.Many2one('tailor.order.measerment')
    order_id = fields.Many2one('sale.order', "Order No", related='measerment_id.order_id')
    partner_id = fields.Many2one("res.partner", "Party", related="order_id.partner_id")
    item_id = fields.Many2one('tailor.item', "Item Name", related='measerment_id.item_id')
    body_point_id = fields.Many2one('tailor.body.point', "Body Point")
    measerment = fields.Char("Measerment")


class TailorOrderAttributeLine(models.Model):
    _name = "tailor.order.attribute.line"
    _description = "Tailor Attribute line for Items Per Order"
    measerment_id = fields.Many2many('tailor.order.measerment','tailor_order_attribute_rel', "attribute_lines",'measerment_id')
    order_id = fields.Many2one('sale.order', "Order No", related='measerment_id.order_id')
    partner_id = fields.Many2one("res.partner", "Party", related="order_id.partner_id")
    item_id = fields.Many2one('tailor.item', "Item Name", related='measerment_id.item_id')
    attribute_id = fields.Many2one('tailor.item.attribute', "Attribute")
    value = fields.Char("Value")

class tailorOrderLineInherit(models.Model):
    _inherit="sale.order.line"
    tailor_item_Lines=fields.One2many("tailor.item.order.line",'order_line_id','Item Order Lines')
class tailorOrderInherit(models.Model):
    _inherit="sale.order"
    measerment_ids=fields.One2many("tailor.order.measerment",'order_id','Measerments')
    tailor_item_order_lines=fields.One2many("tailor.item.order.line",'order_id','Item Order Lines')

    def get_product_kit_boms(self,product,data):
        kit_bom = self.env['mrp.bom'].search([('product_id', '=', product.id), ('type', '=', 'phantom')])
        # if len(kit_bom)>0:
            # for line in kit_bom.bom_line_ids:
            #     kit_bom=self.get_product_kit_boms(line.product_id,data)

        if len(kit_bom)==0:
            kit_bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', product.product_tmpl_id.id),('product_id', '=', False), ('type', '=', 'phantom')])
        if len(kit_bom)>0:
            for line in kit_bom.bom_line_ids:
                kit_bom=self.get_product_kit_boms(line.product_id,data)
        else:
            if product not in data:
                data.append(product)
        return data

    def get_measerment_list(self):
        tailorItemOrderLines=[]
        itemList=[]
        for rec in self.order_line:
            data=[]
            products=(self.get_product_kit_boms(rec.product_id,[]))
            # todo get measerments for products in data
            for product in products:
                item=self.env['tailor.item'].get_item(product)
                item_line=self.env['tailor.item.order.line'].create({'order_line_id':rec.id,'item_id':item.id})
                data.append(item_line.id)
                tailorItemOrderLines.append(item_line.id)
                if item not in itemList:
                    itemList.append(item)
            rec.tailor_item_Lines=[(6,0,data)]
        self.tailor_item_order_lines=[(6,0,tailorItemOrderLines)]
        data=[]
        for item in itemList:
            newMeasurment=self.env['tailor.order.measerment'].create({'item_id':item.id,'order_id':self.id})
            data.append(newMeasurment.id)
        self.measerment_ids=[(6,0,data)]
#
#                 # measerment=self.env["tailor.measerment"].search([("partner_id",'=',self.partner_id.id),("product_id",'=',product.id)])
#                 if len(measerment)==0:
#                     measerment=self.env["tailor.measerment"].search([("partner_id",'=',self.partner_id.id),("product_id",'=',False),("product_tmpl_id",'=',product.product_tmpl_id.id)])
#                 if measerment not in measerment_list:
#                     measerment_list.append(measerment)
#
#         print(measerment_list)
#         data=[]
#         for measerment in measerment_list:
#             print(data)
#
#
#
#
# class TailoringOrderMeaserment(models.Model):
#     _name="tailor.order.measerment"
#     _description="Customers Measerment per order a tailoring Item"
#     # name=fields.Char("Name",compute="get_measerment_name")
#     order_id=fields.Many2one("sale.order","Order ID")
#     tailor_item_id=fields.Many2one("tailor.item","Item Name")
#     partner_id=fields.Many2one('res.partner',"Person",related="order_id.partner_id")
#     product_tmpl_id=fields.Many2one('product.template',related="tailor_item_id.product_tmpl_id")
#     product_id=fields.Many2one('product.product',related="tailor_item_id.product_id")
#     attribute_template_id=fields.Many2one('tailor.item.attribute.template','Template')
#     attribute_value_ids=fields.One2many("tailor.measerment.attribute.value","measerment_id")
#     measerment=fields.Char("Measerments")
#     special_note=fields.Char("Note")