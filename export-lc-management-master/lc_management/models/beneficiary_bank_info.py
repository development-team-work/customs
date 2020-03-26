import itertools
import psycopg2
import re
from datetime import datetime

import eagle.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError



class beneficiary_bank_branch_address(models.Model):
    _name = 'beneficiary_bank_names_branch_address.model'


    name = fields.Char(compute='concatenate_custom_fields',store=True,string='Name')
    bank_name = fields.Char(required=True, string='Bank Name')
    bank_branch = fields.Char(required=True, string='Bank Branch')
    bank_address = fields.Text(required=True, string='Bank Address')
    created_date = fields.Date('Created Dated', default=fields.Date.today())
    s_code = fields.Char(string='Swift Code')
    bank_short = fields.Char(string='Bank Short')

    @api.depends('bank_name','bank_branch','bank_address','s_code')
    def concatenate_custom_fields(self):
        b_n = str(self.bank_name)
        b_brunch = str(self.bank_branch)
        b_addr = str(self.bank_address)
        # b_s_code = str(self.s_code)
        concate_name =  b_n + ', ' + b_brunch + ', ' + b_addr
        if self.s_code: 
            concate_name = b_n + ', ' + b_brunch + ', ' + b_addr + ', Swift Code: '+ str(self.s_code)
        else :
            concate_name = b_n + ', ' + b_brunch + ', ' + b_addr
        self.name = concate_name

class lc_bank_branch_address(models.Model):
    _name = 'lc_bank_names_branch_address.model'


    name = fields.Char(compute='concatenate_custom_fields',store=True,string='Name')
    bank_name = fields.Char(required=True, string='Bank Name')
    bank_branch = fields.Char(required=True, string='Bank Branch')
    bank_address = fields.Text(required=True, string='Bank Address')
    created_date = fields.Date('Created Dated', default=fields.Date.today())
    s_code = fields.Char(string='Swift Code')
    bank_short = fields.Char(string='Bank Short')

    @api.depends('bank_name','bank_branch','bank_address','s_code')
    def concatenate_custom_fields(self):
        b_n = str(self.bank_name)
        b_brunch = str(self.bank_branch)
        b_addr = str(self.bank_address)
        # b_s_code = str(self.s_code)
        concate_name =  b_n + ', ' + b_brunch + ', ' + b_addr
        if self.s_code: 
            concate_name = b_n + ', ' + b_brunch + ', ' + b_addr + ', Swift Code: '+ str(self.s_code)
        else :
            concate_name = b_n + ', ' + b_brunch + ', ' + b_addr
        self.name = concate_name   