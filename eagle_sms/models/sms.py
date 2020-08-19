# -*- coding: utf-8 -*-

import time
import urllib3
import json
from odoo import _,fields, models,api

class smsTest(models.Model):
    _name="sms.test"
    device_id=fields.Char("Device Id")
    authorisation=fields.Char("Authorisation")
    send_to=fields.Char("Receiver")
    message=fields.Char("Mesage")
    def send_sms(self):
        http = urllib3.PoolManager()
        data ={"Content":{"phone_number": self.send_to,"message": self.message,"device_id": self.device_id}}
        encoded_data = json.dumps(data).encode('utf-8')
        r = http.request('POST', 'https://smsgateway.me/api/v4/message/send', headers={
            'Authorization' : self.authorisation,'Content-Type': 'application/json'},
            body=encoded_data)
        print (r.status)
        print (json.loads(r.data))
    def kirim_pesan(nomer,isi_pesan):
        time.sleep(5)
        pesan("08xxxx","[SIMO]--")





