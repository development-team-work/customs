import itertools
import psycopg2
import re
import datetime

import eagle.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
from odoo.tools import amount_to_text_en
import random


class ForwardingLetterModel(models.Model):
    _name = 'forwarding_letter.model'

    commercial_invoice_id = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.')
    name = fields.Char(string='Ref.No')
    date = fields.Date(string='Created Date',default=fields.Date.today())

    for_whom = fields.Char(string='Forwarding To')
    bank_name = fields.Char(string='Bank Name')
    bank_brunch = fields.Char(string='Bank Branch')
    bank_address = fields.Text(string='Bank Address')
    swift_code = fields.Char(string='Swift Code')

    lc_num = fields.Char(string='L/C No')
    lc_date = fields.Date(string='L/C Date')
    lc_num2 = fields.Char(string='lc_num')
    lc_date2 = fields.Date(string='lc_date')
    lc_bank_name = fields.Char(string='lc_bank_name')
    lc_bank_brunch = fields.Char(string='lc_bank_brunch') 
    lc_bank_address = fields.Char(string='lc_bank_address')
    currency_name = fields.Char(string='currency_symbol')
    currency_symbol = fields.Char(string='currency_symbol')
    ordered_products_total_amount = fields.Char(string='Total')

    transfer_per = fields.Integer(string='Transfer Per', default="10")
    fc_account_no = fields.Char(string='F/C Account No')

    sir_madam = fields.Char(string="sir_madam", default="Sir")

    c1 = fields.Char(string='c1', required=True, default="8")
    c2 = fields.Char(string='c2', required=True, default="6")
    c3 = fields.Char(string='c3', required=True, default="1")
    c4 = fields.Char(string='c4', required=True, default="1")
    c5 = fields.Char(string='c5', required=True, default="3")
    c6 = fields.Char(string='c6', required=True, default="3")
    c7 = fields.Char(string='c7', required=True, default="1")
    c8 = fields.Char(string='c8', required=True, default="1")
    c9 = fields.Char(string='c9', required=True, default="3")

    @api.onchange('commercial_invoice_id')
    def onchange_commercial_invoice_id(self):
        res= {}
        name = self.commercial_invoice_id.id
        if name:
            all_data_of_commercial_invoice = self.env['commercial_invoice.model'].browse(name)
            proforma_invoice_id = all_data_of_commercial_invoice.pi_id  
            proforma_invoice_uniq_id = all_data_of_commercial_invoice.proforma_invoice_id
            ordered_products_total_amount = all_data_of_commercial_invoice.ordered_products_total_amount

            service_obj= self.env['sale.order'].browse(proforma_invoice_id.id) 
            beneficiary_bank_name = service_obj.beneficiary_bank_name2 
            beneficiary_bank_branch = service_obj.beneficiary_bank_branch
            beneficiary_bank_address = service_obj.beneficiary_bank_address
            swift_code = service_obj.swift_code
            currency_symbol= self.env['res.currency'].browse(service_obj.currency_id.id)
            
            lc_id = service_obj.lc_num_id
            lc_info_pool_ids = self.env['lc_informations.model'].browse(lc_id.id)
            lc_num = lc_info_pool_ids.name
            lc_date = lc_info_pool_ids.created_date
            lc_bank_name = lc_info_pool_ids.bank_name2
            lc_bank_branch = lc_info_pool_ids.bank_branch
            lc_bank_address = lc_info_pool_ids.bank_address
            
            if lc_bank_name == 'Bank Asia Ltd':
                for_whome_data = 'Exeutive Vice President'
            elif lc_bank_name == 'Pubali Bank Ltd':
                for_whome_data = 'General Manager/Branch In-Charge'
            elif lc_bank_name == 'Dutch-Bangla Bank Ltd':
                for_whome_data = 'Exeutive Vice President'
            elif lc_bank_name == 'Shahjalal Islami Bank Ltd':
                for_whome_data = 'DMD/Branch In Charge'
            elif lc_bank_name == 'Al-Arafah Islami Bank Ltd':
                for_whome_data = 'Manager'
            elif lc_bank_name == 'Islami Bank':
                for_whome_data = 'Exeutive Vice President'                  
            else:
                for_whome_data = 'Exeutive Vice President'    

            now = datetime.datetime.now()
            uniq_num = 'AAYML-CERT/'+str(now.year)

            res = {'value':{
                'name': uniq_num,
                'lc_num':lc_num,
                'lc_date':lc_date,
                'lc_num2':lc_num, 
                'lc_date2':lc_date,
                'lc_bank_name':lc_bank_name,
                'lc_bank_brunch':lc_bank_branch,
                'lc_bank_address':lc_bank_address,
                'currency_name':currency_symbol.name,
                'currency_symbol':currency_symbol.symbol,
                'ordered_products_total_amount':ordered_products_total_amount,
                'bank_name':beneficiary_bank_name,
                'bank_brunch':beneficiary_bank_branch,
                'bank_address':beneficiary_bank_address, 
                'swift_code':swift_code,  
                'for_whom':for_whome_data,
            }}

        else:
            res={}  
        return res         

    def split_from_list(self,list_name,data_field):
        save = []
        for r in list_name:
            save.append(r[data_field])
            combine = '\n'.join([str(i) for i in save])
        return combine 

    def products_total_amount(self,invoice_lines_product_amount):
        total_amount= []
        idx = 0
        for r in invoice_lines_product_amount:
            total_amount.append(r['price_subtotal'])
            combine = sum(total_amount)
        return combine