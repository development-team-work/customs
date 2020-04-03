# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api
from odoo.osv.expression import get_unaccent_wrapper
import re

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_print_product_barcode(self):
        self.ensure_one()
        scraps = self.env['stock.scrap'].search([('picking_id', '=', self.id)])
        domain = [('id', 'in', (self.move_lines + scraps.move_id).stock_valuation_layer_ids.ids)]
        action = self.env.ref('eagle_shop.action_print_barcode_product').read()[0]
        # context = literal_eval(action['context'])
        # context.update(self.env.context)
        # context['no_at_date'] = True
        # return dict(action, domain=domain, context=context)