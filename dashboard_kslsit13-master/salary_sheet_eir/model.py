#-*- coding:utf-8 -*-
########################################################################################
########################################################################################
##                                                                                    ##
##    OpenERP, Open Source Management Solution                                        ##
##    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved       ##
##                                                                                    ##
##    This program is free software: you can redistribute it and/or modify            ##
##    it under the terms of the GNU Affero General Public License as published by     ##
##    the Free Software Foundation, either version 3 of the License, or               ##
##    (at your option) any later version.                                             ##
##                                                                                    ##
##    This program is distributed in the hope that it will be useful,                 ##
##    but WITHOUT ANY WARRANTY; without even the implied warranty of                  ##
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   ##
##    GNU Affero General Public License for more details.                             ##
##                                                                                    ##
##    You should have received a copy of the GNU Affero General Public License        ##
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.           ##
##                                                                                    ##
########################################################################################
########################################################################################

from odoo import api, models, fields
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning

class BranchesLedgerReportSalesRevenue(models.AbstractModel):
    _name = 'report.salary_sheet_eir.drivers_reward_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        record_wizard = self.env[self.model].browse(self.env.context.get('active_id'))

        
        form = record_wizard.form
        to = record_wizard.to

        if record_wizard.batch:
            records = record_wizard.batch.slip_ids
        else:
            records = record_wizard.tree_link

        to = record_wizard.to
        form = record_wizard.form
        resigned = record_wizard.resigned

        salary_rules = self.env['hr.salary.rule'].search([('active','=',True)])
        salary_categs = self.env['hr.salary.rule.category'].search([])

        categs = []

        for x in salary_categs:
            for y in records:
                for z in y.line_ids:
                    if z.category_id.id == x.id and x not in categs:
                        categs.append(x)
        

        categs = sorted(categs, key=lambda x: x.sequance)

        rules = []
        rule_name = []
        for x in records:
            for y in x.line_ids:
                if y.name not in rule_name:
                    rule_name.append(y.name)
                    rules.append(y)

        # rules = sorted(rules, key=lambda x: x.sequance)
        allowance = []
        deduction = []
        advances  = []

        for x in salary_rules:
            if x.category_id.name == 'Allowance':
                allowance.append(x)

        for x in salary_rules:
            if x.category_id.name == 'Deduction':
                deduction.append(x)

        for x in salary_rules:
            if x.category_id.name == 'Advances To Employee ':
                advances.append(x)

        departments = []
        for x in records:
            if x.employee_id.department_id not in departments:
                departments.append(x.employee_id.department_id)


        # if not resigned:

        employee = []
        def collect_records(depart):
            del employee[:]
            for x in records:
                if x.employee_id.department_id == depart:
                    employee.append(x)


        # if resigned:

        #     employee = []
        #     def collect_records(depart):
        #         del employee[:]
        #         for x in records:
        #             if x.employee_id.department_id == depart and x.employee_id.resigned:
        #                 employee.append(x)



        def depart_totale(rule):
            amount = 0
            for x in employee:
                for y in x.line_ids:
                    if y.code == rule:
                        if y.amount:
                            amount = amount + y.amount
            return amount
            
        def get_amount(emp,rule):
            amount = 0
            for x in records:
                if x == emp:
                    for y in x.line_ids:
                        if y.code == rule:
                            if y.amount:
                                amount = y.amount
                    return amount
            return amount
            
        def get_payslip(emp):
            for x in records:
                if x == emp:
                    return x.number
            
        # def sig(emp):
        #     for x in records:
        #         if x == emp:
        #             pass
        #             # if x.payment_journal.type == 'bank':
        #             return True

        # if not resigned:

        def totaled(rule):
            amount = 0
            for x in records:
                for y in x.line_ids:
                    if y.code == rule:
                        if y.amount:
                            amount = amount + y.amount
            return amount

        # if resigned:
        #     def totaled(rule):
        #         amount = 0
        #         for x in records:
        #             if x.employee_id.resigned:
        #                 for y in x.details_by_salary_rule_category:
        #                     if y.code == rule:
        #                         if y.amount:
        #                             amount = amount + y.amount
        #         return amount


        def date_getter():
            month = int(form[5:7])
            months_in_words = {
             1:'January',
             2:'February',
             3:'March',
             4:'April',
             5:'May',
             6:'June',
             7:'July',
             8:'August',
             9:'September',
            10:'October',
            11:'November',
            12:'December',
            }

            month = months_in_words[month]
            return month

        def GetCategRules(attr):
            allRules = []
            allRulesName = []

            for x in records:
                for y in x.line_ids:
                    if y.category_id.id == attr.id and y.name not in allRulesName:
                        allRules.append(y)
                        allRulesName.append(y.name)

            allRules = sorted(allRules, key=lambda x: x.sequence)
            return allRules

        def GetCategSize(attr):
            lists = []
            lists_name = []

            for x in records:
                for y in x.line_ids:
                    if y.category_id.id == attr.id and y.name not in lists_name:
                        lists.append(y)
                        lists_name.append(y.name)

            return len(lists)


            
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': departments,
            'data': data,
            'allowance': allowance,
            'deduction': deduction,
            'advances': advances,
            'get_amount': get_amount,
            # 'date_getter': date_getter,
            'totaled': totaled,
            'employee': employee,
            'collect_records': collect_records,
            'depart_totale': depart_totale,
            'rules': rules,
            'salary_categs': salary_categs,
            'GetCategRules': GetCategRules,
            'GetCategSize': GetCategSize,
            'categs': categs,
            'get_payslip': get_payslip,
            # 'sig': sig
        }

