import itertools
import psycopg2
import re
from datetime import datetime

import eagle.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError



class LCinformations(models.Model):
    _name = 'lc_informations.model'

    # default get default invoice id start
    def _get_default_invoice_id(self):
        if self._context.get('invoice_id'):
            invoice_id = self._context.get('invoice_id')
            return invoice_id
            # raise UserError(_(invoice_id))
        else:
            return ''
    # default get default invoice id end

    name = fields.Char(required=True, string='L/C No.')
    pi_no_id = fields.Many2one('sale.order',string='P/I No',required=True,default=_get_default_invoice_id)
    pi_no = fields.Char(string='Invoice No')
    created_date = fields.Date('L/C Created Dated', default=fields.Date.today())
    org_bank_name = fields.Many2one('lc_bank_names_branch_address.model',required=True, string='LC Bank Name')
    bank_name2 = fields.Char(required=True, string='LC Bank Name')
    bank_branch = fields.Char(required=True, string='LC Bank Branch')
    bank_address = fields.Text('Bank Address',required=True,)
    vat_no = fields.Char('VAT/BIN No.')
    irc_no = fields.Char('IRC No.')
    bin_no = fields.Char('BIN No.')
    tin_no = fields.Char('TIN No.')
    erc_no = fields.Char('ERC No.')
    shipment_last_date = fields.Date('Last Date Of Shipment')
    expire_date = fields.Date('Date of Expire')

    export_con_no = fields.Char('Export Contract No.')
    export_con_no_created_date = fields.Date('Dated')
    export_lc_no = fields.Char('Export L/C No.')
    export_lc_no_created_date = fields.Date('Dated')
    sales_con_no = fields.Char('Sales Contract No.')
    sales_con_no_created_date = fields.Date('Dated')
    tt_no = fields.Char('TT No.')
    tt_no_created_date = fields.Date('Dated')
    exp_sale_con_no = fields.Char('Export Sales Contract No.')
    exp_sale_con_no_created_date = fields.Date('Dated')
    pur_con_no = fields.Char('Purchase Contract No.')
    pur_con_no_created_date = fields.Date('Dated')
    exp_dc_no = fields.Char('Export D/C No.')
    exp_dc_no_created_date = fields.Date('Dated')
    bg_bank_dc_no = fields.Char('Bangladesh Bank D/C No.')
    bg_bank_dc_no_created_date = fields.Date('Dated')
    extra_field = fields.Char('Extra Field Name/No./Date')


    _order = "id desc, created_date desc"
    
   
    def onchange_bank_name_branch(self, bank_name, context=None):
        bank_name_id = bank_name
        if bank_name_id :
            service_obj = self.env['lc_bank_names_branch_address.model'].browse(bank_name_id)
            lc_bank_name = service_obj.bank_name
            lc_bank_branch = service_obj.bank_branch
            lc_bank_address = service_obj.bank_address
            lc_bank_swift_code = service_obj.s_code
            lc_b_addr_swift_code = lc_bank_address +", Swift Code: "+ lc_bank_swift_code

            if lc_bank_branch and lc_bank_address:
                res = {
                    'value': {
                        'bank_name2': lc_bank_name,
                        'bank_branch': lc_bank_branch,
                        'bank_address': lc_b_addr_swift_code,
                    }
                }
            else :
                res = {
                    'value': {
                        'bank_name2': '',
                        'bank_branch': '',
                        'bank_address': ''
                    }
                }
        else:
            res = {}
        return res

    def onchange_pi_no_id(self, pi_no_id, context=None):   
        pi_no_id = pi_no_id
        if pi_no_id:
            service_obj = self.env['sale.order'].browse(pi_no_id)
            pi_no = service_obj.name
            if pi_no:
                res = {
                    'value': {
                        'pi_no': pi_no,
                    }
                } 
            else:
                res = {}
            return res                   

    
    def split_bank_address(self,bank_address_in_list):
        address= []
        idx = 0
        for r in bank_address_in_list:
            address.append(r['address']) 
            combine = '\n \n \n'.join([str(i) for i in address])