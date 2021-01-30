# coding: utf-8

import json
import logging

import dateutil.parser
import pytz
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons.payment_sslcommerz.controllers.main import SSLCommerzController
from odoo.tools.float_utils import float_compare


_logger = logging.getLogger(__name__)


class AcquirerSSLCommerz(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[
        ('sslcommerz', 'SSL Commerz')
    ], ondelete={'sslcommerz': 'set default'})
    # todo new values to adopt ssl
    store_id = fields.Char("Store Id")
    store_pass =fields.Char("Password")
    # issandbox = None
    # mode = None
    # sessionkey = fields.Char('Session Key', required_if_provider='sslcommerz', groups='base.group_user')
    def createSessionUrl(self):
        if self.state=='test':
            mode="sandbox"
        else:
            mode='securepay'
        url= "https://" + mode + ".sslcommerz.com/gwprocess/v4/api.php"
        return url
    def createSession(self, post_body):
        """
        Some mandatory parameters need to pass to SSLCommerz. It identify your customers and orders. Also you have to pass the success, fail, cancel url to redirect your customer after pay.
        Please follow this link https://developer.sslcommerz.com/.
        And Pass value with post_body
        """
        post_body['store_id'] = self.store_id
        post_body['store_passwd'] = self.store_pass
        response = requests.post(self.createSessionUrl, data=post_body)
        return response
        # return self.call_api('POST', self.createSessionUrl, post_body)

    # end New values for sssl
    sslcommerz_email_account = fields.Char('Email', required_if_provider='sslcommerz', groups='base.group_user')
    sslcommerz_seller_account = fields.Char(
        'Merchant Account ID', groups='base.group_user',
        help='The Merchant ID is used to ensure communications coming from SSL Commerz are valid and secured.')
    sslcommerz_use_ipn = fields.Boolean('Use IPN', default=True, help='SSL Commerz Instant Payment Notification', groups='base.group_user')
    sslcommerz_pdt_token = fields.Char(string='PDT Identity Token', help='Payment Data Transfer allows you to receive notification of successful payments as they are made.', groups='base.group_user')
    # Default sslcommerz fees
    fees_dom_fixed = fields.Float(default=0.35)
    fees_dom_var = fields.Float(default=3.4)
    fees_int_fixed = fields.Float(default=0.35)
    fees_int_var = fields.Float(default=3.9)

    def _get_feature_support(self):
        """Get advanced feature support by provider.

        Each provider should add its technical in the corresponding
        key for the following features:
            * fees: support payment fees computations
            * authorize: support authorizing payment (separates
                         authorization and capture)
            * tokenize: support saving payment data in a payment.tokenize
                        object
        """
        res = super(AcquirerSSLCommerz, self)._get_feature_support()
        res['fees'].append('sslcommerz')
        return res


    @api.model
    def _get_sslcommerz_urls(self, environment):
        """ SSL Commerz URLS """

        if environment == 'prod':
            return {
                'sslcommerz_form_url': 'https://www.sslcommerz.com/cgi-bin/webscr',
                # 'sslcommerz_rest_url': 'https://api.sslcommerz.com/v1/oauth2/token',
            }
        else:
            return {
                'sslcommerz_form_url': 'https://sandbox.sslcommerz.com/gwprocess/v3/api.php',
                # 'sslcommerz_rest_url': 'https://api.sandbox.sslcommerz.com/v1/oauth2/token',
            }

    def sslcommerz_compute_fees(self, amount, currency_id, country_id):
        """ Compute sslcommerz fees.

            :param float amount: the amount to pay
            :param integer country_id: an ID of a res.country, or None. This is
                                       the customer's country, to be compared to
                                       the acquirer company country.
            :return float fees: computed fees
        """
        if not self.fees_active:
            return 0.0
        country = self.env['res.country'].browse(country_id)
        if country and self.company_id.country_id.id == country.id:
            percentage = self.fees_dom_var
            fixed = self.fees_dom_fixed
        else:
            percentage = self.fees_int_var
            fixed = self.fees_int_fixed
        fees = (percentage / 100.0 * amount + fixed) / (1 - percentage / 100.0)
        return fees

    def sslcommerz_form_generate_values(self, values):
        base_url = self.get_base_url()

        sslcommerz_tx_values = dict(values)
        sslcommerz_tx_values.update({
            # 'cmd': '_xclick',
            'store_id': self.store_id,
            'store_pass': self.store_pass,
            'store_pass': self.store_pass,
            'item_name': '%s: %s' % (self.company_id.name, values['reference']),
            'tran_id': values['reference'],
            'item_number': values['reference'],
            'amount': values['amount'],
            'total_amount': values['amount'],
            'currency': values['currency'].name ,
            'currency_code': values['currency'] and values['currency'].name or '',
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get('partner_country').code or '',
            'state': values.get('partner_state') and (values.get('partner_state').code or values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'first_name': values.get('partner_first_name'),
            'last_name': values.get('partner_last_name'),
            'sslcommerz_return': urls.url_join(base_url, SSLCommerzController._return_url),
            # notify url
            'success_url': urls.url_join(base_url, SSLCommerzController._notify_url),
            # Cancel Url
            'fail_url': urls.url_join(base_url, SSLCommerzController._cancel_url),
            'handling': '%.2f' % sslcommerz_tx_values.pop('fees', 0.0) if self.fees_active else False,
            'custom': json.dumps({'return_url': '%s' % sslcommerz_tx_values.pop('return_url')}) if sslcommerz_tx_values.get('return_url') else False,
        })
        return sslcommerz_tx_values

    def sslcommerz_get_form_action_url(self):
        self.ensure_one()
        environment = 'prod' if self.state == 'enabled' else 'test'
        return self._get_sslcommerz_urls(environment)['sslcommerz_form_url']


class TxSSLCommerz(models.Model):
    _inherit = 'payment.transaction'

    sslcommerz_txn_type = fields.Char('Transaction type')

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    @api.model
    def _sslcommerz_form_get_tx_from_data(self, data):
        reference, txn_id = data.get('item_number'), data.get('txn_id')
        if not reference or not txn_id:
            error_msg = _('SSL Commerz: received data with missing reference (%s) or txn_id (%s)') % (reference, txn_id)
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        # find tx -> @TDENOTE use txn_id ?
        txs = self.env['payment.transaction'].search([('reference', '=', reference)])
        if not txs or len(txs) > 1:
            error_msg = 'SSL Commerz: received data for reference %s' % (reference)
            if not txs:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return txs[0]

    def _sslcommerz_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        _logger.info('Received a notification from SSL Commerz with IPN version %s', data.get('notify_version'))
        if data.get('test_ipn'):
            _logger.warning(
                'Received a notification from SSL Commerz using sandbox'
            ),

        # TODO: txn_id: shoudl be false at draft, set afterwards, and verified with txn details
        if self.acquirer_reference and data.get('txn_id') != self.acquirer_reference:
            invalid_parameters.append(('txn_id', data.get('txn_id'), self.acquirer_reference))
        # check what is buyed
        if float_compare(float(data.get('mc_gross', '0.0')), (self.amount + self.fees), 2) != 0:
            invalid_parameters.append(('mc_gross', data.get('mc_gross'), '%.2f' % (self.amount + self.fees)))  # mc_gross is amount + fees
        if data.get('mc_currency') != self.currency_id.name:
            invalid_parameters.append(('mc_currency', data.get('mc_currency'), self.currency_id.name))
        if 'handling_amount' in data and float_compare(float(data.get('handling_amount')), self.fees, 2) != 0:
            invalid_parameters.append(('handling_amount', data.get('handling_amount'), self.fees))
        # check buyer
        if self.payment_token_id and data.get('payer_id') != self.payment_token_id.acquirer_ref:
            invalid_parameters.append(('payer_id', data.get('payer_id'), self.payment_token_id.acquirer_ref))
        # check seller
        if data.get('receiver_id') and self.acquirer_id.sslcommerz_seller_account and data['receiver_id'] != self.acquirer_id.sslcommerz_seller_account:
            invalid_parameters.append(('receiver_id', data.get('receiver_id'), self.acquirer_id.sslcommerz_seller_account))
        if not data.get('receiver_id') or not self.acquirer_id.sslcommerz_seller_account:
            # Check receiver_email only if receiver_id was not checked.
            # In SSL Commerz, this is possible to configure as receiver_email a different email than the business email (the login email)
            # In Odoo, there is only one field for the SSL Commerz email: the business email. This isn't possible to set a receiver_email
            # different than the business email. Therefore, if you want such a configuration in your SSL Commerz, you are then obliged to fill
            # the Merchant ID in the SSL Commerz payment acquirer in Odoo, so the check is performed on this variable instead of the receiver_email.
            # At least one of the two checks must be done, to avoid fraudsters.
            if data.get('receiver_email') and data.get('receiver_email') != self.acquirer_id.sslcommerz_email_account:
                invalid_parameters.append(('receiver_email', data.get('receiver_email'), self.acquirer_id.sslcommerz_email_account))
            if data.get('business') and data.get('business') != self.acquirer_id.sslcommerz_email_account:
                invalid_parameters.append(('business', data.get('business'), self.acquirer_id.sslcommerz_email_account))

        return invalid_parameters

    def _sslcommerz_form_validate(self, data):
        status = data.get('payment_status')
        former_tx_state = self.state
        res = {
            'acquirer_reference': data.get('txn_id'),
            'sslcommerz_txn_type': data.get('payment_type'),
        }
        if not self.acquirer_id.sslcommerz_pdt_token and not self.acquirer_id.sslcommerz_seller_account and status in ['Completed', 'Processed', 'Pending']:
            template = self.env.ref('payment_sslcommerz.mail_template_sslcommerz_invite_user_to_configure', False)
            if template:
                render_template = template._render({
                    'acquirer': self.acquirer_id,
                }, engine='ir.qweb')
                mail_body = self.env['mail.render.mixin']._replace_local_links(render_template)
                mail_values = {
                    'body_html': mail_body,
                    'subject': _('Add your SSL Commerz account to Odoo'),
                    'email_to': self.acquirer_id.sslcommerz_email_account,
                    'email_from': self.acquirer_id.create_uid.email_formatted,
                    'author_id': self.acquirer_id.create_uid.partner_id.id,
                }
                self.env['mail.mail'].sudo().create(mail_values).send()

        if status in ['Completed', 'Processed']:
            try:
                # dateutil and pytz don't recognize abbreviations PDT/PST
                tzinfos = {
                    'PST': -8 * 3600,
                    'PDT': -7 * 3600,
                }
                date = dateutil.parser.parse(data.get('payment_date'), tzinfos=tzinfos).astimezone(pytz.utc).replace(tzinfo=None)
            except:
                date = fields.Datetime.now()
            res.update(date=date)
            self._set_transaction_done()
            if self.state == 'done' and self.state != former_tx_state:
                _logger.info('Validated SSL Commerz payment for tx %s: set as done' % (self.reference))
                return self.write(res)
            return True
        elif status in ['Pending', 'Expired']:
            res.update(state_message=data.get('pending_reason', ''))
            self._set_transaction_pending()
            if self.state == 'pending' and self.state != former_tx_state:
                _logger.info('Received notification for SSL Commerz payment %s: set as pending' % (self.reference))
                return self.write(res)
            return True
        else:
            error = 'Received unrecognized status for SSL Commerz payment %s: %s, set as error' % (self.reference, status)
            res.update(state_message=error)
            self._set_transaction_cancel()
            if self.state == 'cancel' and self.state != former_tx_state:
                _logger.info(error)
                return self.write(res)
            return True
