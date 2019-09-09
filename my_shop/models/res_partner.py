# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from eagle import _,fields, models,api

class res_partner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(index=True, translate=True)
    is_writer=fields.Boolean("Is a Writer",default=False , translate=True)
    is_publisher=fields.Boolean("Is a Publisher",default=False , translate=True)
    # book_ids=fields.Many2many('product.template',string="Books")
    published=fields.One2many('product.template','publisher_id',string="Publications", translate=True)
    written=fields.Many2many('product.template','writer_ids',string="Written Books", translate=True)
    balance=fields.Monetary(string="Balance",compute='calculate_balance',  help="Balance for this account.")

    @api.onchange('debit','credit')
    def calculate_balance(self):
        for rec in self:
            rec.balance=rec.credit-rec.debit
