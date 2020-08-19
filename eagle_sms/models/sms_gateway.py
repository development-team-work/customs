# -*- coding: utf-8 -*-

import time
import urllib3
import json
from odoo import _,fields, models,api

class smsSMS(models.Model):
    _inherit = 'sms.sms'
    sms_id=fields.Char("SMS ID")
    device_id = fields.Char("Device Id")
    authorisation = fields.Char("Authorisation")


    def send_sms(self):
        http = urllib3.PoolManager()
        data ={"Content":{"phone_number": self.number,"message": self.body,"device_id": self.device_id}}
        encoded_data = json.dumps(data).encode('utf-8')
        r = http.request('POST', 'https://smsgateway.me/api/v4/message/send', headers={
            'Authorization' : self.authorisation,'Content-Type': 'application/json'},
            body=encoded_data)
        print (r)
        print (r.status)
        if json.loads(r.data)[0]['status']=='pending':
            self.state='outgoing'
        self.sms_id=json.loads(r.data)[0]['id']
    def check_sms_status(self):
        http = urllib3.PoolManager()
        data ={"Content":{"phone_number": self.number,"message": self.body,"device_id": self.device_id}}
        encoded_data = json.dumps(data).encode('utf-8')
        r = http.request("GET", "https://smsgateway.me/api/v4/message/"+self.sms_id, headers={
            'Authorization' : self.authorisation,'Content-Type': 'application/json'},
            body=encoded_data)
        print (r)
        print (r.status)
        print(json.loads(r.data)['status'])
    def kirim_pesan(nomer,isi_pesan):
        time.sleep(5)
        pesan("08xxxx","[SIMO]--")





