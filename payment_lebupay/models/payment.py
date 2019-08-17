# coding: utf-8
from hashlib import sha1
import logging
# import urllib
# import urlparse

from eagle import api, fields, models, _
from eagle.addons.payment.models.payment_acquirer import ValidationError
from eagle.addons.payment_lebupay.controllers.main import LebupayController
from eagle.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)


def normalize_keys_upper(data):
    """Set all keys of a dictionnary to uppercase

    Lebupay parameters names are case insensitive
    convert everything to upper case to be able to easily detected the presence
    of a parameter by checking the uppercase key only
    """
    return {key.upper(): val for key, val in data.items()}


class AcquirerLebupay(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('lebupay', 'Lebupay')], default='lebupay')
    accesskey = fields.Char('Access Key', required_if_provider='lebupay', groups='base.group_user')
    secretkey = fields.Char('Secret key', required_if_provider='lebupay', groups='base.group_user')

    def _get_lebupay_urls(self, environment):
       
        if environment == 'prod':
            return {
                'lebupay_form_url': 'https://checkout.buckaroo.nl/html/',
            }
        else:
            return {
                'lebupay_form_url': 'https://testcheckout.buckaroo.nl/html/',
            }


    @api.multi
    def get_last_order_id(self):

        query = "SELECT id FROM sale_order ORDER BY id DESC LIMIT 1"
        self.env.cr.execute(query)
        data = self.env.cr.dictfetchall()[0]
        lastOrder_id = data['id']
        return lastOrder_id

    @api.multi
    def get_last_order_number(self):

        query = "SELECT name FROM sale_order ORDER BY id DESC LIMIT 1"
        self.env.cr.execute(query)
        data = self.env.cr.dictfetchall()[0]
        lastOrder_number = data['name']
        return lastOrder_number   

    @api.multi
    def get_product_id(self):

        query = "SELECT company_id FROM sale_order_line WHERE order_id=%s ORDER BY id DESC LIMIT 1"
        params = (
           self.get_last_order_id(),
        )
        self.env.cr.execute(query,params)
        data = self.env.cr.dictfetchall()[0]
        company_id = data['company_id']
        return company_id  
    
    @api.multi
    def get_warehouse_id(self):

        query = "SELECT warehouse_id FROM sale_order ORDER BY id DESC LIMIT 1"
        self.env.cr.execute(query)
        data = self.env.cr.dictfetchall()[0]
        warehouseid = data['warehouse_id']
        return warehouseid  
    
    @api.multi
    def get_picking_id(self):

        query = "SELECT id FROM stock_picking_type WHERE warehouse_id=%s AND code=%s ORDER BY id DESC LIMIT 1"
        params = (
           self.get_warehouse_id(),
           'outgoing',
        )
        self.env.cr.execute(query,params)
        data = self.env.cr.dictfetchall()[0]
        picking_id = data['id']
        return picking_id

    @api.multi
    def get_location_id(self):

        query = "SELECT default_location_src_id FROM stock_picking_type WHERE warehouse_id=%s AND code=%s ORDER BY id DESC LIMIT 1"
        params = (
           self.get_warehouse_id(),
           'outgoing',
        )
        self.env.cr.execute(query,params)
        data = self.env.cr.dictfetchall()[0]
        default_location_src_id = data['default_location_src_id']
        return default_location_src_id


    @api.multi
    def lebupay_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        lebupay_tx_values = dict(values)
        lebupay_tx_values.update({
            'accesskey': self.accesskey,
            'secretkey': self.secretkey,
            'amount': values['amount'],
            'currency': values['currency'] and values['currency'].name or '',

            'address_city': values['partner_city'],
            'address_country': values['partner_country'] and values['partner_country'].name or '',
            'email': values['partner_email'],
            'address_zip': values['partner_zip'],
            'name': values['partner_name'],
            'id': values['partner_id'],
            'phone': values['partner_phone'],
        
            'last_order_id':self.get_last_order_id(),
            'last_order_number':self.get_last_order_number(),


            'last_order_product_id':self.get_product_id(),
            'last_order_wareouse_id':self.get_warehouse_id(),
            'last_order_picking_id':self.get_picking_id(),
            'last_order_location_id':self.get_location_id(),

            
            'invoicenumber': values['reference'],
            'test': False if self.environment == 'prod' else True,
        })
       
        return lebupay_tx_values

    @api.multi
    def lebupay_get_form_action_url(self):
        return self._get_lebupay_urls(self.environment)['lebupay_form_url']

