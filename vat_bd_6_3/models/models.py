# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_partner_bin(models.Model):
    _inherit="res.company"
    bin=fields.Char("BIN")

class res_partner_bin_field(models.Model):
    _inherit = 'res.partner'
    bin=fields.Char("BIN")

class account_invoice(models.Model):
    _inherit = 'account.move'
    time_invoice = fields.Datetime(string="Invoice Time" ,default=lambda self: fields.datetime.now())


    def vat_63_challan_print(self):
        """ Print the Vat 6.3 Challan and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True
        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref('vat_bd_6_3.account_vat_63_challan').report_action(self)
        # else:
        #     return self.env.ref('account.account_vat_63_challan').report_action(self)
class account_invoice_line(models.Model):
    _inherit="account.move.line"
    invoice_line_supplimentary_tax = fields.Monetary(string='Supplementary Duty', currency_field='company_currency_id',default="0")
