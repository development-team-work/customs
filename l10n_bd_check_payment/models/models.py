# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang, format_date

INV_LINES_PER_STUB = 9

class AccountPayment(models.Model):
    _inherit = "account.payment"
    def do_print_checks(self):

        return self.env.ref('l10n_bd_check_payment.action_report_print_check').report_action(self, data=[])