# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.osv.expression import get_unaccent_wrapper
import re


class tailorMrpBomInherit(models.Model):
    _inherit="mrp.bom"
    _sql_constraints = [
        ('template_product_unique', 'unique (product_tmpl_id,product_id)',
         'only one BOM is posible for specific product !')]


    @api.onchange('partner_id','order_line')
    def get_measerment_list(self):
        for rec in self:
            data=[]
            for orderline in rec.order_line:
                if orderline.product_template_id:
                    kit_boms=check_kit_for_product_template(orderline.product_template_id.id)
            #         tmpl_boms=self.env['mrp.bom'].search([('product_tmpl_id','=',orderline.product_template_id.id)])
            #         product_boms=self.env['mrp.bom'].search([('product_id','=',orderline.product_id.id)])
            #         if len(product_boms)>0:
            #             for rec_bom in product_boms:
            #                 if rec_bom.type='phantom':
            #                     kit_products=product_boms=self.env['mrp.bom'].search([('product_id','=',rec.product_id.id)])
            #         measermentLine=self.env['tailor.measerment'].search([("partner_id","=",rec.partner_id.id),("product_tmpl_id","=",orderline.product_template_id.id)])
            #         if measermentLine.id:
            #             data.append(measermentLine.id)
            #         else:
            #             newMeserment=measermentLine.create({'partner_id': rec.partner_id.id,'tailor_item_id':orderline.product_template_id.item_id.id})
            #             data.append(newMeserment.id)
            #     else:
            #         measermentLine=self.env['tailor.measerment'].search([("partner_id","=",rec.partner_id.id),("product_tmpl_id","=",orderline.product_template_id.id)])
            #         print(measermentLine.id)
            # rec.measerment_ids= [(6,0,data)]