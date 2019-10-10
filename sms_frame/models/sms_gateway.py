# -*- coding: utf-8 -*-
from openerp import api, fields, models


class SmsGateway(models.Model):
    _name = "sms.gateway"

    name = fields.Char(required=True, string='Gateway Name')
    gateway_model_name = fields.Char(required='True', string='Gateway Model Name')

    gateway_url = fields.Char("Gateway Url", required='True')
    param_to_mobile = fields.Char("Parameter For Receiver No", required='True')
    param_sid = fields.Char("Parameter For SID", required='True')
    param_message = fields.Char("Parameter For SMS Body", required='True')
    param_user = fields.Char("Parameter For User Name", required='True')
    param_password = fields.Char("Parameter For User Password", required='True')