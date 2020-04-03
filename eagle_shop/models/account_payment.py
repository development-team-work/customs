# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api

class accountInvoice(models.Model):
    _inherit = 'account.payment'
    balance=fields.Monetary("Balance",related='partner_id.balance')


