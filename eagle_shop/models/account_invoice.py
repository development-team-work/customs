# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api

# class accountInvoice(models.Model):
#     _inherit = 'account.invoice'
#     balance=fields.Monetary("Balance",coumpute='get_party_balance',store="True")
#     @api.onchange('partner_id')
#     def get_party_balance(self):
#         for rec in self:
#             if rec.partner_id:
#                 rec.balance=self.partner_id.balance


