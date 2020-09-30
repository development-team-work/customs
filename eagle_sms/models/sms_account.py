# -*- coding: utf-8 -*-

import time
import urllib3
import json
from odoo import _,fields, models,api


class smsSMS(models.Model):
    _name = 'sms.gateway.account'
    name=fields.Char("Account Name")
    gateway_id = fields.Many2one("sms.gateway","Gateway_id")
    user_string=fields.Char("User String" , related="gateway_id.user_string")
    user_id=fields.Char("User_id")
    password_string = fields.Char("User String" , related = "gateway_id.password_string")
    password=fields.Char("password")
