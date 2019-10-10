# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

import itertools
import psycopg2
import re
from datetime import datetime

import eagle.addons.decimal_precision as dp

from eagle import api, fields, models, tools, _
from eagle.exceptions import ValidationError, except_orm, UserError

class SaleOrderInherited(models.Model):
    _inherit = 'sale.order'

    pi_type =  fields.Selection([('LOCAL', 'LOCAL'),('L/C', 'L/C'),('L/C-DELAY', 'L/C Delay')],'PI Type',required=True)

    commodity = fields.Char(string='Commodity')
    method_of_payment =  fields.Many2one('method_of_payment.model',string='Method of Payment')
    terms_note = fields.Many2one('terms_conditions.model','Terms and conditions')
    # erc_no =  fields.Char(string='ERC NO.', default=lambda self: self._default_erc_no())
    erc_no =  fields.Char(string='ERC NO.')
    # bin_no =  fields.Char(string='BIN', default=lambda self: self._default_bin_no())
    bin_no =  fields.Char(string='BIN')
    agent_code = fields.Char(string='Agent Code')
    bags_of_packing =  fields.Char(string='Packing',default='50')
    country_of_origin =  fields.Many2one('country_origin.model',string='Country Of Origin')
    
    lc_num_id =  fields.Many2one('lc_informations.model', string='L/C No')
    lc_num =  fields.Char(string='L/C No')
    lc_created_date =  fields.Char(string='L/C Created Date')
    amend_no =  fields.Char(string='Amend No/Date')
    org_beneficiary_bank_name =  fields.Many2one('beneficiary_bank_names_branch_address.model',string='Beneficiary Bank Name', required=True)
    beneficiary_bank_name2 =  fields.Char(string='beneficiary_bank_name2')
    beneficiary_bank_branch =  fields.Char(string='Beneficiary Bank Branch')
    beneficiary_bank_address =  fields.Text(string='Beneficiary Bank Address')
    swift_code =  fields.Char(string='Swift Code')
    account_number =  fields.Char(string='Account Number')
    validity_date = fields.Datetime(string='Validity Date', required=True)
    beneficiary_bank_branch =  fields.Char(string='Beneficiary Bank Branch')

    time_of_delivery =  fields.Char(string='Time of Delivery',default='Within 30 days from the date.')
    reimbursement =  fields.Many2one('reimbursement.model',string='Reimbursement')
    posted_by = fields.Char(string='Posted By', default='SMS')
    hs_code = fields.Char(string='H.S Code', default='5203.00.00')
    remarks = fields.Char(string='Remarks')
    product_type =  fields.Many2one('product_type.model',string='Type')
    terms_of_delivery =  fields.Many2one('terms_of_delivery.model',string='Terms of Delivery')
    # place_of_delivery_addr =  fields.Char(string='Delivery Factory Address', default=lambda self: self._default_place_of_delivery_addr())
    place_of_delivery_addr =  fields.Char(string='Delivery Factory Address')
    signature = fields.Many2one('signature_upload.model',string='Signature')
    signature_image = fields.Binary(
            'Signarute_image',help="Select signature image here"
        )
    unity_of_mesure2 = fields.Many2one('product.uom', string='Unit Of Mesure') 
    # quantity_total = fields.Monetary(string='Total Quantity', store=True, readonly=True, compute='_amount_all', track_visibility='always')  
    # benificiary_name = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))

    # 'quantity_total': fields.function(_amount_all_wrapper, string='Total Quantity', type='integer', store=True,multi='sums', help="The total quantity."), 

    def onchange_lc_num(self, lc_num_id):
        lc_num_id = lc_num_id 
        service_obj = self.env['lc_informations.model'].browse(lc_num_id)
        lc_num = service_obj.name   
        lc_created_date = service_obj.created_date     
        if lc_num:
            res = {
                'value': {  
                    'lc_num': lc_num,
                    'lc_created_date': lc_created_date,
                }
            }
        else : 
            res = {}
        return res      

    @api.onchange('org_beneficiary_bank_name')  
    def onchange_org_beneficiary_bank_name(self):
        org_beneficiary_bank_name_id = self.org_beneficiary_bank_name.id
        # raise UserError(_(org_beneficiary_bank_name_id))   
        service_obj= self.env['beneficiary_bank_names_branch_address.model'].browse(org_beneficiary_bank_name_id)
        b_name = service_obj.bank_name  
        b_branch = service_obj.bank_branch 
        b_addr = service_obj.bank_address 
        swift_code = service_obj.s_code 

        if b_name:
            res = {
                    'value': { 
                        'beneficiary_bank_name2': b_name,
                        'beneficiary_bank_branch': b_branch,  
                        'beneficiary_bank_address': b_addr,
                        'swift_code': swift_code
                    }
                } 
        else:
            res = {}

        return res    


    def onchange_signature(self,signature):
        signature_id = signature

        if signature_id : 
            service_obj= self.env['signature_upload.model'].browse(signature_id)
            name = service_obj.my_binary_field_name

            res = {
                    'value': { 
                        'signature_image': name
                    }
                }
        else :        
            res = {
                    'value': {
                        'signature_image': ''
                    }
                } 

        return res        

    # @api.depends('amount_total', 'currency_id')
    # def numToWords(self,join=True):
    #     words = amount_to_text_en.amount_to_text(self.amount_total, 'en', 'Dollars')       

class MethodOfPaymentInherited(models.Model):
    _name = 'method_of_payment.model'    
    name = fields.Text(string="Method Of Payment" ,required=True)

class TermsConditionsInherited(models.Model):
    _name = 'terms_conditions.model'    
    name = fields.Text(string="Terms and Conditions" ,required=True)    

class CountryOriginInherited(models.Model):
    _name = 'country_origin.model'    
    name = fields.Char(string="Country" ,required=True)     

class ReimbursementInherited(models.Model):
    _name = 'reimbursement.model'    
    name = fields.Char(string="Reimbursement" ,required=True)     

class ProductTypeInherited(models.Model):
    _name = 'product_type.model'    
    name = fields.Text(string="Product Type" ,required=True)     

class TermsOfDeliveryInherited(models.Model):
    _name = 'terms_of_delivery.model'    
    name = fields.Text(string="Terms Of Delivery " ,required=True)      

class Signature(models.Model):
    _name = 'signature_upload.model'
    name = fields.Char(required=True, string='Name')
    my_binary_field_name = fields.Binary(
       'Signarute',help="Select signature image here"
    )
    created_date = fields.Date('Created Dated', default=fields.Date.today())    

    

    