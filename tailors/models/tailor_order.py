# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.osv.expression import get_unaccent_wrapper
import re


class tailorOrderInherit(models.Model):
    _inherit="sale.order"
    measerment_ids=fields.One2many("tailor.measerment",'order_id','Measerments')
    @api.onchange('partner_id','order_line')
    def measerment_list(self):
        for rec in self:
            data=[]
            for orderline in rec.order_line:
                if orderline.product_template_id.tailoring_item:
                    measermentLine=self.env['tailor.measerment'].search([("partner_id","=",rec.partner_id.id),("product_tmpl_id","=",orderline.product_template_id.id)])
                    if measermentLine.id:
                        data.append(measermentLine.id)
                    else:
                        newMeserment=measermentLine.create({'partner_id': rec.partner_id.id,'tailor_item_id':orderline.product_template_id.item_id.id})
                        data.append(newMeserment.id)
            rec.measerment_ids= [(6,0,data)]