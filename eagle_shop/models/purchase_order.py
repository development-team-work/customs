# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api

class purchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'
    balance = fields.Monetary("Balance",related="partner_id.balance")
    def action_open_partner_ledger(self):
        """ return the action to open partner Ledger for the specific Partner"""
        action = self.env.ref('eagle_shop.action_account_partner_ledger_menus').read()[0]
        action['context'] ={'default_partner_id' : [(6,0,[self.partner_id.id])]}
        return action



