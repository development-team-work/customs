# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportPartnerLedger(models.AbstractModel):
    _name = 'report.l10n_bd_check_payment.report_check_print'


    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.payment'].browse(docids)

        return {
            'docs': docs,
            'doc_model': self.env['account.payment'],
            'time': time,
        }
