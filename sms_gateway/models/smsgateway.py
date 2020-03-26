import requests
from odoo import _,fields, models,api
import datetime

class SmsGatewayAccount(models.Model):
    _name='eagle.smsgateway.account'
    _description = "SMS Getway Account Details"
    name=fields.Char("Account Name/ Mobile No")
    sms_gateway_id=fields.Many2one("eagle.smsgateway",string="SMS Gateway Provider Name",required=True)
    credentials=fields.One2many("smsgateway.account.credential",'account_id',"Credentials")
    credential_value=fields.Char("value")

    @api.onchange('sms_gateway_id')
    def sms_gateway_id_onchange(self):
        for rec in self:
            credents=rec.sms_gateway_id.parameter_ids
            for cre in credents:
                rec.credentials=self.env['eagle.smsgateway.parameters'].search([('sms_gateway_id','=',rec.sms_gateway_id.id)])
            # for cred in credents:
                # credentials=self.env[]

class SMSAcountCredentials(models.Model):
    _name = "smsgateway.account.credential"
    account_id=fields.Many2one('eagle.smsgateway.account',"Account Name")
    gateway_id=fields.Many2one("eagle.smsgateway",string="SMS Gateway",related='account_id.sms_gateway_id')
    parameter_id=fields.Many2one('eagle.smsgateway.parameters',"Credential Name")
    parameter_value=fields.Char("Credential Value")
class SmsGatewayParameters(models.Model):
    _name='eagle.smsgateway.parameters'
    _description = "list of parameters for the sms gateways"
    sms_gateway_id=fields.Many2one("eagle.smsgateway","SMS Gateway")
    name=fields.Char("Parameter Name")
    parameter_value=fields.Char("Parameter Value")


class Message(models.Model):
    _name="eagle.smsgateway.message"
    message_id=fields.Integer("SMS ID",)
    device=fields.Many2one("eagle.smsgateway.device","From Device")
    message=fields.Char("Message")
    phone_number=fields.Char("To")
    updated_at=fields.Datetime("Posted at")
    sent_at=fields.Datetime("Sent at")
    sms_status=fields.Selection([(1,"Pending"),
                                 (2,"Sent"),
                                 (3,"Failed")])
    created_at=fields.Datetime("created on",default=datetime.datetime.utcnow())
    _sql_constraints = [
        ('message_id_unique', 'unique(message_id)', 'Message Id Must Be Unique'),
    ]


    def send_sms(self):
        for rec in self:
            body = [{'device_id': rec.device_id,'phone_number':rec.phone_number,'message':rec.message}]
            response= rec.device.sms_gateway._make_post('message/send', body)
            rec.message_id=response[0]["id"]
            rec.updated_at=response[0]["updated_at"].replace('T'," ")
            if response[0]["status"]=='pending':
                rec.sms_status=1


        return response
    def get_sms(self):
        for rec in self:
            url = 'message/{}'.format(rec.message_id)
            response= rec.device.sms_gateway._make_get(url)
            if response["status"]=='sent':
                rec.sms_status=2
                rec.sent_at = response["updated_at"].replace('T', " ")
            if response["status"]=='failed':
                rec.sms_status=3
                rec.sent_at = response["updated_at"].replace('T', " ")
            return response
class SMSGateway(models.Model):
    _name="eagle.smsgateway"
    name=fields.Char("SMS Gateway Provider")
    model_id=fields.Char("Model Name")
    parameter_ids=fields.One2many('eagle.smsgateway.parameters',"sms_gateway_id","Parameters")
    _sql_constraints = [
        ('model_id_unique', 'unique(model_id)', 'SMS model Must Be Unique'),
        ('getway_name_unique', 'unique(name)', 'SMS Provider Must Be Unique'),
    ]

    # base_endpoint=fields.Char("Base EndPoint")
    # api_key=fields.Char("API Key")

    # def __init__(self, "api_key"):
    #     self.api_key = api_key

    def _get_headers(self):
        return {'Authorization': self.api_key}


    def _make_post(self,endpoint,body):
        url = self.base_endpoint + endpoint
        return requests.post(url, json=body, headers=self._get_headers()).json()
    def _make_get(self, endpoint):
        url = self.base_endpoint + endpoint
        return requests.get(url, headers=self._get_headers()).json()

    # def _make_post(self, endpoint, body):
    #     url = SMSGateway.BASE_ENDPOINT + endpoint
    #     return requests.post(url, json=body, headers=self._get_headers()).json()
    #
    # def search_devices(self, filters=None):
    #     return self._make_post('device/search', filters)
    #
    # def get_device(self, device_id):
    #     url = 'device/{}'.format(device_id)
    #     return self._make_get(url)
    #
    # def send_sms(self, *messages: Message):
    #     body = [m.__dict__ for m in messages]
    #     return self._make_post('message/send', body)
    #
    # def cancel_sms(self, *ids: int):
    #     body = [{'id': sms_id} for sms_id in ids]
    #     return self._make_post('message/cancel', body)
    #
    # def get_sms(self, sms_id: int):
    #     url = 'message/{}'.format(sms_id)
    #     return self._make_get(url)
    #
    # def search_sms(self, filters=None):
    #     return self._make_post('message/search', filters)
