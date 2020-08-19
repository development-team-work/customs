# #-*- coding:utf-8 -*-

import os
# import xlsxwriter
from datetime import date
from datetime import date, timedelta
import datetime
import time
from odoo import api, models, fields
from odoo.exceptions import Warning, ValidationError
from odoo.tools import config
import base64
import string
import sys


class SalarySheet(models.TransientModel):
    _name = "drivers.reward.report"

    form = fields.Date("Start Date")
    to = fields.Date("End Date")
    resigned = fields.Boolean()

    tree_link = fields.Many2many('hr.payslip')
    batch = fields.Many2one('hr.payslip.run', string="Pay Slip Batch")

    @api.onchange('batch')
    def onchange_batch(self):
        if self.batch:
            payslips = []
            for x in self.batch.slip_ids:
                payslips.append(x.id)

            self.tree_link = payslips
            self.form = self.batch.date_start
            self.to = self.batch.date_end

    # @api.multi
    def generate_report(self):
        data = {}
        data['form'] = self.read(['form', 'to'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['form', 'to'])[0])
        return self.env.ref('salary_sheet_eir.report_for_drivers_reward_id').report_action(self, data=data)


class hr_salary_rule_ext(models.Model):
    _inherit = "hr.salary.rule.category"

    sequance = fields.Integer("Sequance")
