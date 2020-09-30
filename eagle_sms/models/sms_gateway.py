# -*- coding: utf-8 -*-

import time
import urllib3
import json
from odoo import _,fields, models,api

class smsSMS(models.Model):
    _name = 'sms.gateway'
    name=fields.Char("Gateway Name")
    model_name=fields.Char("Getway Model Name")
    website=fields.Char("website")
    send_to_string = fields.Char("String for Send to")
    msg_string = fields.Char("String for SMS Body")
    user_string = fields.Char("String for User")
    password_string = fields.Char("String for Password")

    endpoint_sending=fields.Char("Endpoint for Sending ")
    method_sending=fields.Char("Request method for Sending ")

    endpoint_cancel=fields.Char("Endpoint for Cancel ")
    method_cancel=fields.Char("Request method for Cancel")

    endpoint_check=fields.Char("Endpoint for Check ")
    method_check=fields.Char("Request method for Check")

    endpoint_search=fields.Char("Endpoint for Search ")
    method_search=fields.Char("Request method for Search")


