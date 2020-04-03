# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api
from smsgateway import SMSGateway, Message



class smsSend(models.Model):
    _name="sms.sms"
    client = fields.Char(default='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhZG1pbiIsImlhdCI6MTU3MDQ2MzcyOCwiZXhwIjo0MTAyNDQ0ODAwLCJ1aWQiOjQ3MDc5LCJyb2xlcyI6WyJST0xFX1VTRVIiXX0.8A1fb1HKuRA1hvNu1vMob4vZ8LnkrilKTmAMJ3YwSRo')
