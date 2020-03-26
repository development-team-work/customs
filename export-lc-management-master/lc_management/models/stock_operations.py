import itertools
import psycopg2
import re
from datetime import datetime

import eagle.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError

class StockPickingLcInherit(models.Model):
    _inherit = 'stock.picking'
    _order = "origin desc"

    process = fields.Selection([('set_for_LC', 'Set For LC'),('pandding', 'Pandding')],'Process', default='set_for_LC')
    do_no =  fields.Char(string="Delivery Order No")
    lc_no =  fields.Many2one('lc_informations.model', string="L/C No")


    # raise UserError(_(invoice_id))
    @api.model
    def create(self, vals):
        invoice_id = self.origin
        seq_obj = self.env['ir.sequence']
        do_num = seq_obj.next_by_code('do_num') or 'New'
        sale_order_obj = self.env['sale.order'].search([('name', '=ilike', invoice_id)], limit=1)
        lc_no = sale_order_obj.lc_num_id.id
        sale_order_id = sale_order_obj.ids
        if not vals:
            vals = {}
        if not invoice_id:
            vals['do_no'] = do_num
            vals['lc_no'] = lc_no
            vals['sale_order_id'] = sale_order_id
            return super(StockPickingLcInherit, self).create(vals)
        else:    
            stmt = "SELECT do_no FROM stock_picking WHERE origin = '"+ str(invoice_id) +"'  ORDER BY id DESC LIMIT 1"
            self.env.cr.execute(stmt)
            do_n = self.env.cr.fetchone()[0] or 'PI'
            vals['do_no'] = do_n
            vals['lc_no'] = lc_no
            return super(StockPickingLcInherit, self).create(vals)

