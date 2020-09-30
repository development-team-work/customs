# -*- coding: utf-8 -*-

import time
import urllib3
import json
from odoo import _,fields, models,api

class smsgatewayme(models.Model):
    _name = 'sms.gateway.me'
    _description = "SMS Gateway Me"
    def send_sms(self,send_to,msg,send_from,password,database_id):
        http = urllib3.PoolManager()
        data = {"Content": {"phone_number": send_to, "message": msg, "device_id": send_from,}}
        encoded_data = json.dumps(data).encode('utf-8')
        r = http.request('POST', 'https://smsgateway.me/api/v4/message/send', headers={
            'Authorization': password, 'Content-Type': 'application/json'},
                         body=encoded_data)
        print(r)
        print(r.status)
        if json.loads(r.data)[0]['status'] == 'pending':
            self.state = 'outgoing'
        self.sms_id = json.loads(r.data)[0]['id']
        self.env['sms.sms'].search([("id","=",database_id)]).sms_id = json.loads(r.data)[0]['id']
    def check_sms(self,send_to,msg,send_from,password,database_id):
        http = urllib3.PoolManager()
        data = {"search": { "field": "phone_number", "operator": "=","value": "01720569256"}}
        encoded_data = json.dumps(data).encode('utf-8')
        r = http.request('POST', 'https://smsgateway.me/api/v4/message/search', headers={
            'Authorization': password, 'Content-Type': 'application/json'},
                         body=encoded_data)
        print(r)
        #here i got the sms from server
        # now to manipulate it as i wish
        print(r.data)
        print(r.data[0])
