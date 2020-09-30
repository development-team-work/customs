# -*- coding: utf-8 -*-

import time
import urllib3
import json
from odoo import _,fields, models,api

class smsSMS(models.Model):
    _inherit = 'sms.sms'
    sms_id=fields.Char("SMS ID")
    sms_gateway_account_id=fields.Many2one("sms.gateway.account","SMS Gateway Account ID")



    def send_sms(self):
        self.env[self.sms_gateway_account_id.gateway_id.model_name].send_sms(self.number,self.body,self.sms_gateway_account_id.user_id,self.sms_gateway_account_id.password,self.id)
    def check_sms(self):
        self.env[self.sms_gateway_account_id.gateway_id.model_name].check_sms(self.number,self.body,self.sms_gateway_account_id.user_id,self.sms_gateway_account_id.password,self.id)
