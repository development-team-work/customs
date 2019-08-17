import itertools
import psycopg2
import re
import datetime

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
from odoo.tools import amount_to_text_en
import random


class ToWhomModel(models.Model):
    _name = 'to_whom.model'

    name = fields.Char(string='Benificiary Certificate Ref.No', default=lambda self: self._default_sort_name1())
    c_of_o_name = fields.Char(string='Certificate Of Origin Ref.No', default=lambda self: self._default_sort_name2())
    quality_name = fields.Char(string='Quality Ref.No', default=lambda self: self._default_sort_name3())
    commercial_invoice_id = fields.Many2one('commercial_invoice.model',string='Commercial Invoice No.')
    date = fields.Date(string='Created Date',default=fields.Date.today())


    letter1 = fields.Text(string="Benificiary Certificate Let1")  
    letter2 = fields.Text(string="Benificiary Certificate Let2")
    letter3 = fields.Text(string="Certificate Of Origin Let1")
    letter4 = fields.Text(string="Quality Let1")
    letter5 = fields.Text(string="Quality Let2")
    letter6 = fields.Text(string="Non Uzbek Let1")
    letter7 = fields.Text(string="Non Uzbek Let2")

    country_of_origin = fields.Char(string="Towhom Let1")

    ordered_products_total_quantity = fields.Char(string='ordered_products_total_quantity')
    commodity = fields.Char(string='commodity')
    customer_name = fields.Char(string='Buyer') 
    customer_full_address = fields.Char(string='Buyer Address') 
    commercial_invoice_no = fields.Char(string='Commercial Invoice no')
    commercial_invoice_created_date = fields.Date(string='commercial_invoice_created_date')
    proforma_invoice_no = fields.Char(string='proforma_invoice_no')
    proforma_invoice_created_date = fields.Date(string='proforma_invoice_created_date')

    truck_receipt_no = fields.Char(string='Truck Receipt No') 
    truck_challan_created_date = fields.Date(string='truck_challan_created_date')

    delivery_challan_no = fields.Char(string='Delivery Challan No.')
    delivery_challan_created_date = fields.Date(string='delivery_challan_created_date')

    lc_num = fields.Char(string='L/C No.')
    lc_date = fields.Date(string='lc_date')
    contact_no = fields.Char(string='contact_no')
    dealer_factory_name = fields.Char(string='Delivery From')


    # raise UserError(_(comm_name))
    @api.onchange('commercial_invoice_id')
    def onchange_commercial_invoice_id(self):
        res= {}
        name = self.commercial_invoice_id.id
        if name:
            all_data_of_commercial_invoice = self.env['commercial_invoice.model'].browse(name)
            commodity = all_data_of_commercial_invoice.commodity  
            ordered_products_total_quantity = all_data_of_commercial_invoice.ordered_products_total_quantity
            truck_challan_created_date = all_data_of_commercial_invoice.commercial_invoice_created_date
            country_of_origin = all_data_of_commercial_invoice.country_of_origin

            cus_name = all_data_of_commercial_invoice.customer_name
            customer_full_address = all_data_of_commercial_invoice.customer_full_address
            commercial_invoice_no = all_data_of_commercial_invoice.name
            commercial_invoice_created_date = all_data_of_commercial_invoice.commercial_invoice_created_date
            proforma_invoice_id = all_data_of_commercial_invoice.pi_id
            proforma_invoice_uniq_id = all_data_of_commercial_invoice.proforma_invoice_id
            proforma_invoice_created_date = all_data_of_commercial_invoice.proforma_invoice_created_date
            contact_no = all_data_of_commercial_invoice.contact_no
            only_seq_num = all_data_of_commercial_invoice.only_seq_num
            supplier_factory_address= all_data_of_commercial_invoice.supplier_factory_address

            service_obj= self.env['sale.order'].browse(proforma_invoice_id.id)
            lc_id = service_obj.lc_num_id
            lc_info_pool_ids = self.env['lc_informations.model'].browse(lc_id.id)
            lc_num = lc_info_pool_ids.name
            lc_date = lc_info_pool_ids.created_date

            product_type_id = service_obj.product_type
            product_type = product_type_id.name

            letter1 = "This is to certify that we are the manufacturer of cotton spun yarn and supplied "+ ordered_products_total_quantity + "kgs. of "+ commodity + " to "+ cus_name +" "+ customer_full_address +" under our Commercial Invoice No. "+ commercial_invoice_no +" dated "+ commercial_invoice_created_date+" Proforma Invoice No. "+ proforma_invoice_uniq_id +" Truck Receipt No. "+ only_seq_num +" dated "+ truck_challan_created_date + " Delivery Challan No. "+ only_seq_num +" dated "+ truck_challan_created_date + " against L/C No. "+ lc_num + " dated "+ lc_date +" which is issued against "+ contact_no +" and Locally manufactured at our factory "+ supplier_factory_address
            
            letter2 = "We also certify that we have not availed any Bonded Warehouse Facilities for the aforesaid supply and we did not or shall not apply for any duty draw back or cash Assistance facility against the aforesaid supply."

            letter3 = "We hereby declare that the 'Yarn' supplied against L/C No."+ lc_num +" dated "+ lc_date +" against "+ contact_no +" under our Commercial Invoice No. "+ commercial_invoice_no +" dated "+ commercial_invoice_created_date +" Delivery Challan No. "+ only_seq_num +" dated "+ truck_challan_created_date +" is of "+ country_of_origin +" origin which have been manufactured in our factory at "+ supplier_factory_address

            letter4 = "We hereby declare that the 'Quality Yarn' have been supplied by usagainst L/C No."+ lc_num +" dated "+ lc_date +" against "+ contact_no +" under our Commercial Invoice No. "+ commercial_invoice_no +" dated "+ commercial_invoice_created_date +" Delivery Challan No. "+ only_seq_num +" dated "+ truck_challan_created_date

            letter5 = "We also declare that 'Supplied Quantity of Yarn' against aforesaid L/C is as per Proforma Invoice No. "+ proforma_invoice_uniq_id 

            letter6 = "This is to certify that we are the manufacturer of cotton spun yarn and supplied "+ ordered_products_total_quantity +" kgs. of "+ product_type +" to "+ cus_name +" "+ customer_full_address +" under our Commercial Invoice No. "+ commercial_invoice_no +" dated "+ commercial_invoice_created_date+" Proforma Invoice No. "+ proforma_invoice_uniq_id +" Truck Receipt No. "+ only_seq_num +" dated "+ truck_challan_created_date + " Delivery Challan No. "+ only_seq_num +" dated "+ truck_challan_created_date + " against L/C No. "+ lc_num + " dated "+ lc_date +" which is issued against "+ contact_no +" and Locally manufactured at our factory "+ supplier_factory_address

            letter7 = 'We also certify that the supplied yarn was made from "NON UZBEK" cotton only.' 

            res = {'value':{
                'letter1':letter1,
                'letter2':letter2,  
                'letter3':letter3,
                'letter4':letter4,
                'letter5':letter5,
                'letter6':letter6,
                'letter7':letter7,
                'country_of_origin':country_of_origin,
                'ordered_products_total_quantity':ordered_products_total_quantity,
                'customer_name':cus_name, 
                'customer_full_address':customer_full_address, 
                'commercial_invoice_no':commercial_invoice_no,  
                'commercial_invoice_created_date':commercial_invoice_created_date,
                'proforma_invoice_no':proforma_invoice_uniq_id,
                'proforma_invoice_created_date':proforma_invoice_created_date,
                'lc_num':lc_num,
                'lc_date':lc_date,
                'contact_no':contact_no, 
                'commodity':commodity,
                'truck_receipt_no':only_seq_num,
                'delivery_challan_no':only_seq_num, 
                'dealer_factory_name':supplier_factory_address,
            }}

        else:
            res={}  
        return res  

    @api.model
    def _get_company(self):
        return self._context.get('company_id', self.env.user.company_id.id)

    def _default_sort_name1(self):  
        company_id = self.env['res.users']._get_company()
        company = self.env['res.company'].browse(company_id.id)
        company_name = company.name
        now = datetime.datetime.now()
        if company_name =='MSA Spinning Mills Limited':
            return 'MSASL-CERT/'+str(now.year)
        if company_name =='AA Yarn Mills Ltd':
            return 'AAYML-CERT/'+str(now.year)
        if company_name =='MSA Textiles Ltd':
            return 'MSATL-CERT/'+str(now.year) 
        if company_name =='AA Coarse Spun Ltd':
            return 'AACSL-CERT/'+str(now.year)   
        if company_name =='AA Synthetic Fibres Ltd':
            return 'AASFL-CERT/'+str(now.year)
        if company_name =='Kader Compact Spinning Ltd':
            return 'KCSL-CERT/'+str(now.year)
        else:
            return 'TO-CERT/'+str(now.year) 

    def _default_sort_name2(self):  
        company_id = self.env['res.users']._get_company()
        company = self.env['res.company'].browse(company_id.id)
        company_name = company.name
        now = datetime.datetime.now()
        if company_name =='MSA Spinning Mills Limited':
            return 'MSASL-CO/'+str(now.year)
        if company_name =='AA Yarn Mills Ltd':
            return 'AAYML-CO/'+str(now.year)
        if company_name =='MSA Textiles Ltd':
            return 'MSATL-CO/'+str(now.year) 
        if company_name =='AA Coarse Spun Ltd':
            return 'AACSL-CO/'+str(now.year)   
        if company_name =='AA Synthetic Fibres Ltd':
            return 'AASFL-CO/'+str(now.year)
        if company_name =='Kader Compact Spinning Ltd':
            return 'KCSL-CO/'+str(now.year)
        else:
            return 'TO-CO/'+str(now.year)

    def _default_sort_name3(self):  
        company_id = self.env['res.users']._get_company()
        company = self.env['res.company'].browse(company_id.id)
        company_name = company.name
        now = datetime.datetime.now()
        if company_name =='MSA Spinning Mills Limited':
            return 'MSASL-CO'+str(now.year)
        if company_name =='AA Yarn Mills Ltd':
            return 'AAYML-CO'+str(now.year)
        if company_name =='MSA Textiles Ltd':
            return 'MTL-CO'+str(now.year) 
        if company_name =='AA Coarse Spun Ltd':
            return 'AACSL-CO'+str(now.year)   
        if company_name =='AA Synthetic Fibres Ltd':
            return 'AASFL-CO'+str(now.year)
        if company_name =='Kader Compact Spinning Ltd':
            return 'KCSL-CO'+str(now.year)
        else:
            return 'WHOM-CO'+str(now.year)        


    # def products_total_quantity(self,invoice_lines_product_quantity):
    #     total_quantity= []
    #     idx = 0
    #     for r in invoice_lines_product_quantity:
    #         total_quantity.append(r['quantity'])
    #         in_com = sum(total_quantity)
    #         combine = int(in_com)
    #     return combine           

    # def split_commodity(self,commodity_names):
    #     names= []
    #     idx = 0
    #     for r in commodity_names:
    #         names.append(r['commodity'])
    #         combine = '\n \n'.join([str(i) for i in names])  
    #     return combine

    # def split_truck_challan_created_date(self,dates):
    #     names= []
    #     idx = 0
    #     for r in dates:
    #         names.append(r['truck_challan_created_date'])
    #         combine = '\n \n'.join([str(i) for i in names])  
    #     return combine

    # def split_delivery_challan_created_date(self,dates):
    #     names= []
    #     idx = 0
    #     for r in dates:
    #         names.append(r['delivery_challan_created_date'])
    #         combine = '\n \n'.join([str(i) for i in names])  
    #     return combine