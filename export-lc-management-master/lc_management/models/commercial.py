import itertools
import psycopg2
import re
import datetime

import eagle.addons.decimal_precision as dp

from eagle import api, fields, models, tools, _
from eagle.exceptions import ValidationError, except_orm, UserError
from eagle.tools import amount_to_text_en
import random


class CommercialInvoiceModel(models.Model):
    _name = 'commercial_invoice.model'
    _rec_name = "name"
    _order = "id desc"

    name = fields.Char(string='Commercial Invoice Number')
    commercial_invoice_created_date = fields.Date(string='Created Date',default=fields.Date.today())
    # customer_invoice_id = fields.Many2one('account.invoice',string='Customer Invoice No.')
    pi_id = fields.Many2one('sale.order',string='Proforma Invoice No.')
    lc_service_obj= fields.Many2one('lc_informations.model', string="L/C No.")
    customer_name = fields.Char(string='Customer Name')
    customer_name2 = fields.Char(string='Customer Name')
    customer_full_address = fields.Text(string='Customer Address')
    proforma_invoice_id = fields.Text(string='Proforma Invoice No.')
    proforma_invoice_created_date = fields.Date(string='Proforma Invoice Date')
    transport = fields.Char(string='Means of Transport', default="By Truck")
    supplier_factory_name = fields.Char(string='Delivery From Factory Name')
    supplier_factory_address = fields.Text(string='Delivery From Factory Address', default="Ex Factory, Nagarhawla Shreepur, Gazipur.")
    beneficiary_vat_no = fields.Char(string='Beneficiary VAT No:')
    erc_no = fields.Char(string='ERC No')
    country_of_origin = fields.Char(string='Country Of Origin')
    country_of_origin2 = fields.Char(string='Country Of Origin')
    destination_address = fields.Text(string='Destination')
    client_shipping_factory_address = fields.Text(string='Factory Address') 
    lc_id = fields.Char('L/C id')
    lc_num = fields.Char('L/C No.')
    lc_num2 = fields.Char(string='L/C No.')
    lc_date = fields.Date(string='L/C Dated')
    lc_date2 = fields.Date(string='L/C Dated')
    issuing_bank = fields.Text(string='Issuing Bank')
    vat_code = fields.Char(string='VAT/BIN No.' )
    irc_num = fields.Char(string='IRC No.' )
    bin_num = fields.Char(string='BIN No.' ) 
    tin_num = fields.Char(string='TIN No.' )
    amend_no = fields.Char(string='Amend No/Date' )
    
    ordered_products_name = fields.Text(string='ordered_products_name') 
    ordered_products_number_of_bags = fields.Text(string='ordered_products_number_of_bags') 
    ordered_products_quantity = fields.Text(string='ordered_products_quantity') 
    gross_weights = fields.Text(string='gross weights')
    total_gross_weight = fields.Char(string='gross weight', default="0.00")
    total_gross_weight2 = fields.Char(string='gross weight', default="0.00")
    total_bags = fields.Char(string='Total Bags', default="0")
    total_bags2 = fields.Char(string='Total Bags', default="0")
    ordered_products_price_of_unit = fields.Text(string='ordered_products_price_of_unit')
    ordered_products_amount = fields.Text(string='ordered_products_amount')
    ordered_products_total_quantity = fields.Char(string='ordered_products_total_quantity', default="0")
    ordered_products_total_amount = fields.Char(string='Total', default="0.00")
    ordered_products_total_amount_in_word = fields.Char(string='ordered_products_total_amount_in_word')
    currency_symbol_name = fields.Char(string='currency_symbol_name')
    currency_symbol_name1 = fields.Char(string='currency_symbol_name')
    currency_symbol_name2 = fields.Char(string='currency_symbol_name')
    currency_symbol = fields.Char(string='currency_symbol')
    currency_symbol1 = fields.Char(string='currency_symbol')
    currency_symbol2 = fields.Char(string='currency_symbol')
    contact_no = fields.Text(string='contact no')
    only_seq_num = fields.Char(string='only_seq_num', size=255)
    num_of_bags = fields.Char(string='num_of_bags', size=255)
    delivery_order_num = fields.Char(string='Delivery Order Number')  
    delivery_challan_num = fields.Char(string='Delivery Challan Number')
    delivery_order_created_date = fields.Date(string='Delivery Order Created date')
    delivery_order_num_created = fields.Text(string='Delivery Order Num date')
    partner_id = fields.Char(string='Partner')
    commodity = fields.Char(string='commodity')
    place_of_delivery = fields.Char(string="place_of_delivery")
    document_status = fields.Char(string='Document Status', default='set_for_LC')

    lc_line_ids = fields.One2many(comodel_name = 'lc_product_line.model', inverse_name = 'parent_id', string = 'Children Ids')

    active_id_field = fields.Char(string='Active',default=lambda self: self._context.get('active_idl'))


    # bill_of_echange
    boe_letter1 = fields.Text(string="BOE Letter1", default="At 120 days SIGHT of this First of Exchange (Second being unpaid) pay to the order of")
    boe_letter11 = fields.Text(string="BOE Letter1", default="At 120 days SIGHT of this Second of Exchange (First being unpaid) pay to the order of")
    boe_letter2 = fields.Text(string="BOE Letter2")
    boe_letter3 = fields.Text(string="BOE Letter3")
    beneficiary_bank_name = fields.Char(string='Beneficiary Bank Name' )
    beneficiary_bank_brunch = fields.Char(string='Bank Brunch' )
    beneficiary_bank_address = fields.Char(string='Bank Address' )
    swift_code = fields.Char(string='Swift Code' )
    truck_receive_date = fields.Date(string="Truck Recv Date",default=fields.Date.today())
    truck_no = fields.Char(string="Truck No", default="Dhaka Metro U-140196")
    freight = fields.Char(string='Freight', default="Pre-paid" )
    del_challan_date = fields.Date(string='Del. Challan Date',default=fields.Date.today())
    lc_bank_name = fields.Char(string='LC Bank Name' )
    lc_bank_brunch = fields.Char(string='LC Bank Branch' )  
    lc_bank_address = fields.Char(string='LC Bank Address' )
    benificiary_name = fields.Char(string="company_name" )
    document_status = fields.Char(string='Document Status', default='set_for_LC')

    truck_receipt_no = fields.Text(string="Truck Receipt No.", default="Cover Van No. DM-TA-18186, DM-TA-14-3518, DM-TA-14-1465, DM-TA-14-1876") 
    delivery_form_date = fields.Date(string="Delivery From Date",default=fields.Date.today())
    delivery_to_date = fields.Date(string="Delivery To Date",default=fields.Date.today())
    delivery_challans_names = fields.Text(string="Delivery Challan No.")

    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        if not vals:
            vals = {}
        seq_obj = self.env['ir.sequence']
        seq_obj2 = self.env['ir.sequence']
        invoice_num = seq_obj.next_by_code('commercial_invoice_report_num') or 'New'
        only_num = seq_obj2.next_by_code('only_num') or 'New_seqq'
        vals['name'] = invoice_num
        vals['only_seq_num'] = only_num
        return super(CommercialInvoiceModel, self).create(vals)

    def contex_pass(self):
        active_idls = self.env.context.get('active_idl', False)
        self.write({'active_id_field': active_idls})
        return True

        



    # raise UserError(_(invoice_id))
    @api.onchange('lc_service_obj')
    def onchange_lc_service_obj(self):
        res= {}
        if self.lc_service_obj:
            active_id = self.active_id_field
            if active_id: 
                    lc_obj= self.env['lc_informations.model'].browse(self.lc_service_obj.id) 
                    lc_id = lc_obj.id
                    lc_name = lc_obj.name
                    pi_id = lc_obj.pi_no_id
                    service_obj= self.env['sale.order'].browse(pi_id.id)  
                    service_obj2= self.env['res.partner'].browse(service_obj.partner_id.id)
                    currency_symbol= self.env['res.currency'].browse(service_obj.currency_id.id)
                    cus_name = service_obj2.name
                    
                    # cus_full_address = service_obj2.head_office_address
                    # cus_factory_addr = service_obj2.factory_office_address 
                    cus_addr = str(service_obj2.street) 
                    commodity = service_obj.commodity
                    place_of_delivery = service_obj.place_of_delivery_addr
                    lc_id = service_obj.lc_num_id
                    lc_service_objj= self.env['lc_informations.model']
                    rec = lc_service_objj.browse(lc_id.id)
                    lc_org_bank_name = rec.org_bank_name.name
                    lc_bank_name = rec.bank_name2
                    lc_bank_branch = rec.bank_branch
                    lc_bank_address = rec.bank_address
                    bank_info = str(lc_org_bank_name)
                    c_no1 = rec.export_con_no 
                    c_date1 = rec.export_con_no_created_date 
                    c_no2 = rec.export_lc_no 
                    c_date2 = rec.export_lc_no_created_date 
                    c_no3 = rec.sales_con_no 
                    c_date3 = rec.sales_con_no_created_date 
                    c_no4 = rec.tt_no 
                    c_date4 = rec.tt_no_created_date 
                    c_no5 = rec.exp_sale_con_no 
                    c_date5 = rec.exp_sale_con_no_created_date 
                    c_no6 = rec.pur_con_no 
                    c_date6 = rec.pur_con_no_created_date 
                    c_no7 = rec.exp_dc_no 
                    c_date7 = rec.exp_dc_no_created_date 
                    c_no8 = rec.bg_bank_dc_no 
                    c_date8 = rec.bg_bank_dc_no_created_date 
                    c_no9 = rec.extra_field 
                    combine_con = ''
                    if c_no1:
                        combine_con += 'Export Contract No. ' +str(c_no1)+ ' dated ' + str(c_date1)
                    if c_no2:
                        combine_con += ' Export L/C No. ' +str(c_no2)+ ' dated ' + str(c_date2)
                    if c_no3:
                        combine_con += ' Sales Contract No. ' +str(c_no3)+ ' dated ' + str(c_date3)   
                    if c_no4:
                        combine_con += ' TT No. ' +str(c_no4)+ ' dated ' + str(c_date4)
                    if c_no5:
                        combine_con += ' Export Sales Contract No. ' +str(c_no5)+ ' dated ' + str(c_date5)    
                    if c_no6:
                        combine_con += ' Purchase Contract No. ' +str(c_no6)+ ' dated ' + str(c_date6)
                    if c_no7:
                        combine_con += ' Export D/C No. ' +str(c_no7)+ ' dated ' + str(c_date7)
                    if c_no8:
                        combine_con += ' Bangladesh Bank D/C No. ' +str(c_no8)+ ' dated ' + str(c_date8)
                    if c_no9:
                        combine_con += '' +str(c_no9)         
                    contract_no = combine_con
                    vat_no = rec.vat_no
                    irc_no = rec.irc_no
                    bin_no = rec.bin_no
                    tin_no = rec.tin_no

                    stock_ids = self.env['stock.picking'].search([('lc_no','=',lc_id.id),('process','=','set_for_LC'),('state','=','done')])
                    if not stock_ids:
                        raise UserError(_("No document ready for set L/C document under PI No. %s !")% (service_obj.name,))
                    else:
                            
                            if stock_ids:
                                stock_id_list = []
                                challan_name_list = []
                                pi_ids_and_date_list = []
                                do_no_list = []
                                delivery_order_date_list = []
                                delivery_order_num_created_date_list = []
                                # truck_no_list = []
                                for stock_id in stock_ids:
                                    stock_id_list.append(stock_id.id) 

                                pi_no_date_seen = set()    
                                do_no_seen = set()    
                                for stoc_id in stock_id_list :
                                    stock_picking_line = self.env['stock.picking'].browse(stoc_id) 
                                    if stock_picking_line.name:
                                        challan_name_list.append(stock_picking_line.name)
                                    if stock_picking_line.origin:
                                        pi_id_date_search= self.env['sale.order'].search([('name','=ilike',stock_picking_line.origin),])
                                        invoice_name = pi_id_date_search.name
                                        if invoice_name not in pi_no_date_seen:
                                            pi_no_date_seen.add(invoice_name)
                                            invoice_date = pi_id_date_search.confirmation_date
                                            only_invoice_dat = datetime.datetime.strptime(invoice_date, '%Y-%m-%d %H:%M:%S')
                                            only_invoice_date = only_invoice_dat.strftime('%d-%m-%Y')
                                            concate_id_date = invoice_name + ' dated '+ str(only_invoice_date)
                                            pi_ids_and_date_list.append(concate_id_date)
                                    if stock_picking_line.do_no:        
                                        do_no = stock_picking_line.do_no   
                                        if do_no not in do_no_seen:
                                            do_no_seen.add(do_no)
                                            do_no_list.append(do_no)
                                            pi_id_date_search= self.env['stock.picking'].search([('do_no','=ilike',do_no), ('backorder_id','=',False)])
                                            do_date = pi_id_date_search.create_date
                                            only_do_dat = datetime.datetime.strptime(do_date, '%Y-%m-%d %H:%M:%S')
                                            only_do_date1 = only_do_dat.strftime('%Y-%m-%d')
                                            only_do_date = only_do_dat.strftime('%d-%m-%Y')
                                            delivery_order_date_list.append(only_do_date1)
                                            concate_do_date = do_no + ' dated '+ str(only_do_date)
                                            delivery_order_num_created_date_list.append(concate_do_date)

                            delivery_challans_names = ',\n'.join(challan_name_list)     
                            pi_ids_and_date = ', '.join(pi_ids_and_date_list)  
                            do_no = ', '.join(do_no_list)  
                            delivery_order_date = ',\n'.join(delivery_order_date_list) 
                            delivery_order_num_created_date = ',\n'.join(delivery_order_num_created_date_list)  
                            # truck_no_names = ',\n'.join(truck_no_list)  

                            stock_line_pool_ids = self.env['stock.pack.operation'].search([('picking_id','=',stock_id_list),])  

                            num_of_bags = service_obj.bags_of_packing
                            ordered_products_all = self.split_products_all(stock_line_pool_ids,num_of_bags) 

                            lc_product_line_obj = self.env['lc_product_line.model']
                            lc_line_vals = {}
                            
                            active_id = self.active_id_field
                            product_id_list = ordered_products_all.get('product_id_list')    
                            product_name_list = ordered_products_all.get('product_name_list')    
                            product_gross_list = ordered_products_all.get('product_gross_list') 
                            product_qnt_list = ordered_products_all.get('product_qnt_list')   
                            price_unit_list = ordered_products_all.get('price_unit_list')    
                            price_subtotal_list = ordered_products_all.get('price_subtotal_list') 
                            num_of_bag_list = ordered_products_all.get('num_of_bag_list') 
                            for x in range(len(product_id_list)):
                                pr_ids = product_id_list[x]
                                pr_names = product_name_list[x] 
                                pr_gross = product_gross_list[x]
                                pr_qnt = product_qnt_list[x]
                                pri_unit = price_unit_list[x]
                                pri_sub = price_subtotal_list[x]
                                num_bag = num_of_bag_list[x]
                                lc_line_vals['parent_id'] = active_id
                                lc_line_vals['active_id'] = int(active_id)
                                lc_line_vals['product_id'] = pr_ids
                                lc_line_vals['product_name'] = pr_names
                                lc_line_vals['number_of_bags'] = num_bag  
                                lc_line_vals['product_gross'] = pr_gross
                                lc_line_vals['product_quant'] = pr_qnt
                                lc_line_vals['unit_price'] = pri_unit
                                lc_line_vals['total_price'] = pri_sub
                                lc_product_line_obj._create_lc_line_from_vals(lc_line_vals)
                            total_qnt = ordered_products_all.get('total_qnt') 
                            for x in range(len(total_qnt)):
                                total_quantity = total_qnt[x]
                            total_gross = ordered_products_all.get('total_gross') 
                            for x in range(len(total_gross)):
                                total_gross_weight = total_gross[x]
                            total_pri = ordered_products_all.get('total_pri') 
                            for x in range(len(total_pri)):
                                total_price = total_pri[x] 
                            total_pri_word = ordered_products_all.get('total_pri_word') 
                            for x in range(len(total_pri_word)):
                                total_price_in_word = total_pri_word[x]  
                            total_bags = ordered_products_all.get('total_bags') 
                            for x in range(len(total_pri_word)):
                                total_bags = total_bags[x]       

                            amend_no_list = []
                            proforma_invoice_ids= self.env['sale.order'].search([('lc_num_id','=',lc_name),]).ids
                            for proforma_invoice_line in proforma_invoice_ids:
                                amend = self.env['sale.order'].browse(proforma_invoice_line)
                                if amend.amend_no:
                                    amend_no_list.append(amend.amend_no)
                            amend_names = ', '.join(amend_no_list)   
                            boe_letter2_text = "Value Received and charged the same to the account of " + cus_name +", "+ cus_addr
                            boe_letter3_text = "DRAWN under L/C No. " + rec.name + " dated " + rec.created_date + " Issued by " + lc_bank_name + ", against "+ contract_no 
                            beneficiary_bank_name = service_obj.org_beneficiary_bank_name.bank_name 
                            beneficiary_bank_brunch = service_obj.beneficiary_bank_branch
                            beneficiary_bank_address = service_obj.beneficiary_bank_address
                            swift_code = service_obj.swift_code
                            # benificiary_name = service_obj.benificiary_name
                            benificiary_name = service_obj.company_id.name

                    res = {'value':{
                        'partner_id' : service_obj.partner_id.id,
                        'customer_name':cus_name,
                        'customer_name2':service_obj2.name, 
                        'customer_full_address':cus_addr,
        #               'client_shipping_factory_address':cus_factory_addr,
        #               'destination_address': cus_factory_addr,
                        'erc_no':service_obj.erc_no,
                        'country_of_origin':service_obj.country_of_origin.name,
                        'country_of_origin2':service_obj.country_of_origin.name,
                        'num_of_bags': service_obj.bags_of_packing,
                        'lc_id':lc_id.id,
                        'lc_num':rec.name,
                        'lc_num2':rec.name,
                        'lc_date':rec.created_date,
                        'issuing_bank':bank_info,
                        'lc_date2':rec.created_date,
                        'vat_code':rec.vat_no,
                        'irc_num':rec.irc_no,
                        'bin_num':rec.bin_no, 
                        'tin_num':rec.tin_no,
                        'amend_no':amend_names,
                        'currency_symbol_name':currency_symbol.name,
                        'currency_symbol_name1':currency_symbol.name,
                        'currency_symbol_name2':currency_symbol.name,
                        'currency_symbol':currency_symbol.symbol,
                        'currency_symbol1':currency_symbol.symbol,
                        'currency_symbol2':currency_symbol.symbol, 
                        'delivery_order_num':do_no,  
                        'delivery_order_created_date':delivery_order_date, 
                        'delivery_order_num_created':delivery_order_num_created_date, 
                        'proforma_invoice_id' : pi_ids_and_date,
                        'contact_no' : contract_no,
                        'pi_id' : pi_id,
                        'commodity' : commodity,      
                        'place_of_delivery' : place_of_delivery,    
                        'total_gross_weight' : total_gross_weight,  
                        'ordered_products_total_quantity' : int(total_quantity),  
                        'ordered_products_total_amount' : total_price, 
                        'ordered_products_total_amount_in_word' : total_price_in_word,
                        'total_bags' : int(total_bags),
                        'boe_letter2': boe_letter2_text,
                        'boe_letter3': boe_letter3_text,
                        'beneficiary_bank_name': beneficiary_bank_name,
                        'beneficiary_bank_brunch': beneficiary_bank_brunch,
                        'beneficiary_bank_address': beneficiary_bank_address, 
                        'swift_code': swift_code, 
                        'lc_bank_name': lc_bank_name,
                        'lc_bank_brunch': rec.bank_branch, 
                        'lc_bank_address': lc_bank_address,  
                        'benificiary_name': benificiary_name,  
                        'delivery_challans_names': delivery_challans_names,
                        # 'truck_no': truck_no_names,
                        'beneficiary_vat_no': service_obj.bin_no,
                    }}
            else:
                raise UserError(_('Please Click on Set Documents button and create an Active Id.'))
        

        return res    

    # raise UserError(_(stock_line_pool_ids))
    def split_products_all(self,stock_line_pool_ids,num_of_bags):
            
            bags = int(num_of_bags)

            final_dict = {"product_id_list": [], "product_name_list": [], "product_gross_list": [], "product_qnt_list": [], "price_unit_list": [], "price_subtotal_list": [], "num_of_bag_list": [], "total_qnt": [], "total_gross": [], "total_pri": [], "total_pri_word": [], "total_bags": []}  

            test_dict = dict()
            p_key_list = list()
            for stock_line in stock_line_pool_ids:
                prod_id = stock_line.product_id.id
                prod_name = stock_line.product_id.name
                prod_qnt = stock_line.qty_done
                prod_gross = stock_line.qty_done * 1.04
                prod_unit_price = stock_line.product_id.list_price
                prod_sub_total = stock_line.product_id.list_price * stock_line.qty_done
                prod_num_of_bags = stock_line.qty_done / bags

                key_name = str(prod_name)
                if key_name in test_dict: 
                    test_dict[key_name][1] = test_dict[str(prod_name)][1] + prod_qnt 
                    test_dict[key_name][2] = test_dict[str(prod_name)][2] + prod_gross 
                    test_dict[key_name][4] = test_dict[str(prod_name)][4] + prod_sub_total 
                    test_dict[key_name][5] = test_dict[str(prod_name)][5] + prod_num_of_bags 
                else:
                    p_key_list.append(key_name)
                    f_list=list()
                    f_list.append(prod_id)
                    f_list.append(prod_qnt)
                    f_list.append(prod_gross)
                    f_list.append(prod_unit_price)     
                    f_list.append(prod_sub_total)
                    f_list.append(prod_num_of_bags)
                    test_dict.update({key_name:f_list})    

            product_qnt_total = 0
            product_gross_total = 0
            product_sub_total = 0
            product_num_of_bags_total = 0
            for keys in p_key_list:  
                product_id = test_dict[keys][0]
                final_dict["product_id_list"].append(product_id)
                product_name= keys
                final_dict["product_name_list"].append(product_name)
                product_gross = test_dict[keys][2]
                final_dict["product_gross_list"].append(product_gross) 
                product_qnt = test_dict[keys][1]
                final_dict["product_qnt_list"].append(product_qnt) 
                price_subtotal = test_dict[keys][4]
                final_dict["price_subtotal_list"].append(price_subtotal) 
                price_unit = test_dict[keys][3]
                final_dict["price_unit_list"].append(price_unit) 
                num_of_bag = test_dict[keys][5]
                final_dict["num_of_bag_list"].append(num_of_bag) 

                
                product_qnt_total += test_dict[keys][1]
                product_gross_total += test_dict[keys][2]
                product_sub_total += test_dict[keys][4]
                product_num_of_bags_total += test_dict[keys][5]

            final_dict["total_qnt"].append(product_qnt_total) 
            final_dict["total_gross"].append(product_gross_total) 
            final_dict["total_pri"].append(product_sub_total) 
            words = amount_to_text_en.amount_to_text(product_sub_total, 'en', 'Dollars')  
            final_dict["total_pri_word"].append(words) 
            final_dict["total_bags"].append(product_num_of_bags_total) 
       

            return final_dict    

    
    # @api.multi
    # def confirm_lc(self):
        # pi_no = self.pi_no
        # commercial_invoice_name = self.commercial_invoice_name
        # process_status_done = 'Done'
        # process_status_set_for_LC = 'set_for_LC'
        # self.write({})

        # self._cr.execute("SELECT id FROM bill_of_exchange_model WHERE commercial_invoice_name = %s AND document_status = %s",(commercial_invoice_name,process_status_set_for_LC))
        # lines = self.env['bill_of_exchange.model'].browse([r[0] for r in self._cr.fetchall()])

        # if lines:
        #     for inv in self:
        #         self._cr.execute("UPDATE bill_of_exchange_model SET document_status=%s WHERE commercial_invoice_name=%s AND document_status=%s",(process_status_done,commercial_invoice_name,process_status_set_for_LC))
        #         self._cr.execute("UPDATE account_invoice SET process=%s,process_status=%s WHERE pi_no=%s AND process=%s",(process_status_done,process_status_done,pi_no,process_status_set_for_LC))
        #         self.invalidate_cache()
                
        # else:
        #     raise except_orm(_('else'))               
          
        # return True    

    
        
    # raise Warning(_(invoice_lines_product_all))
    def numToWords(self,num,join=True):
        '''words = {} convert an integer number into words'''
        units = ['','one','two','three','four','five','six','seven','eight','nine']
        teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen', \
                'seventeen','eighteen','nineteen']
        tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy', \
                'eighty','ninety']
        thousands = ['','thousand','million','billion','trillion','quadrillion', \
                    'quintillion','sextillion','septillion','octillion', \
                    'nonillion','decillion','undecillion','duodecillion', \
                    'tredecillion','quattuordecillion','sexdecillion', \
                    'septendecillion','octodecillion','novemdecillion', \
                    'vigintillion']
        words = []
        if num==0: words.append('zero')
        else:
            numStr = '%d'%num
            numStrLen = len(numStr)
            groups = (numStrLen+2)/3
            numStr = numStr.zfill(groups*3)
            for i in range(0,groups*3,3):
                h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
                g = groups-(i/3+1)
                if h>=1:
                    words.append(units[h])
                    words.append('hundred')
                if t>1:
                    words.append(tens[t])
                    if u>=1: words.append(units[u])
                elif t==1:
                    if u>=1: words.append(teens[u])
                    else: words.append(tens[t])
                else:
                    if u>=1: words.append(units[u])
                if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+',')
        if join: return ' '.join(words)
        return words


    
class LcProductLines(models.Model):
    _name = 'lc_product_line.model'

    parent_id = fields.Many2one(comodel_name='commercial_invoice.model', string="Parent")
    active_id = fields.Many2one(string="Active Id")
    product_id = fields.Many2one(comodel_name='product.product', string="Product")
    product_name = fields.Char(string="Product Name")
    number_of_bags = fields.Integer(string="No. Of Bags", default=0,)  
    product_gross = fields.Float(string="Product Gross Weight")
    product_quant = fields.Integer(string="Qty in kgs")
    unit_price = fields.Float(string="Unit Price")
    total_price = fields.Float(string="Total Price")
    

    def _create_lc_line_from_vals(self,lc_line_vals):
        return self.env['lc_product_line.model'].create(lc_line_vals)