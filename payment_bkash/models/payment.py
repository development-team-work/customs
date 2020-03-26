# coding: utf-8

import json
import logging

import dateutil.parser
import pytz
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons.payment_bkash.controllers.main import bKashController
from odoo.tools.float_utils import float_compare


_logger = logging.getLogger(__name__)


class AcquirerbKash(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('bkash', 'bKash')])
    agent_no=fields.Char("bKash Agent No")
    bkash_email_account = fields.Char('bKash Email ID', required_if_provider='bkash', groups='base.group_user')
    bkash_seller_account = fields.Char(
        'bKash Merchant ID', groups='base.group_user',
        help='The Merchant ID is used to ensure communications coming from bKash are valid and secured.')
    bkash_use_ipn = fields.Boolean('Use IPN', default=True, help='bKash Instant Payment Notification', groups='base.group_user')
    bkash_pdt_token = fields.Char(string='bKash PDT Token', help='Payment Data Transfer allows you to receive notification of successful payments as they are made.', groups='base.group_user')
    # Server 2 server
    bkash_api_enabled = fields.Boolean('Use Rest API', default=False)
    bkash_api_username = fields.Char('Rest API Username', groups='base.group_user')
    bkash_api_password = fields.Char('Rest API Password', groups='base.group_user')
    bkash_api_access_token = fields.Char('Access Token', groups='base.group_user')
    bkash_api_access_token_validity = fields.Datetime('Access Token Validity', groups='base.group_user')
    # Default bkash fees
    fees_dom_fixed = fields.Float(default=0.0)
    fees_dom_var = fields.Float(default=1.85)
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
        res = super(AcquirerbKash, self)._get_feature_support()
        res['fees'].append('bkash')
        return res

    @api.model
    def _get_bkash_urls(self, environment):
        """ bKash URLS """
        if environment == 'prod':
            return {
                'bkash_form_url': '/payment/bkash/',
                'bkash_rest_url': '/payment/bkash/',
            }
        else:
            return {
                'bkash_form_url': '/payment/bkash/',
                'bkash_rest_url': '/payment/bkash/',
            }


    def bkash_compute_fees(self, amount, currency_id, country_id):
        """ Compute bkash fees.

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
        fees = (percentage / 100.0 * amount) + fixed / (1 - percentage / 100.0)
        return fees


    def bkash_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        bkash_tx_values = dict(values)
        bkash_tx_values.update({
            'seller_account':self.bkash_seller_account,
            'cmd': '_xclick',
            'business': self.bkash_email_account,
            'item_name': '%s: %s' % (self.company_id.name, values['reference']),
            'item_number': values['reference'],
            'amount': values['amount'],
            'currency_code': values['currency'] and values['currency'].name or '',
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get('partner_country').code or '',
            'state': values.get('partner_state') and (values.get('partner_state').code or values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'first_name': values.get('partner_first_name'),
            'last_name': values.get('partner_last_name'),
            'bkash_return': urls.url_join(base_url, bKashController._return_url),
            'notify_url': urls.url_join(base_url, bKashController._notify_url),
            'cancel_return': urls.url_join(base_url, bKashController._cancel_url),
            'handling': '%.2f' % bkash_tx_values.pop('fees', 0.0) if self.fees_active else False,
            'custom': json.dumps({'return_url': '%s' % bkash_tx_values.pop('return_url')}) if bkash_tx_values.get('return_url') else False,
        })
        return bkash_tx_values


    def bkash_get_form_action_url(self):
        return self._get_bkash_urls(self.environment)['bkash_form_url']


class TxbKash(models.Model):
    _inherit = 'payment.transaction'

    bkash_txn_type = fields.Char('Transaction type')

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    @api.model
    def _bkash_form_get_tx_from_data(self, data):
        reference, txn_id = data.get('item_number'), data.get('txn_id')
        if not reference or not txn_id:
            error_msg = _('bKash: received data with missing reference (%s) or txn_id (%s)') % (reference, txn_id)
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        # find tx -> @TDENOTE use txn_id ?
        txs = self.env['payment.transaction'].search([('reference', '=', reference)])
        if not txs or len(txs) > 1:
            error_msg = 'bKash: received data for reference %s' % (reference)
            if not txs:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return txs[0]


    def _bkash_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        _logger.info('Received a notification from bKash with IPN version %s', data.get('notify_version'))
        if data.get('test_ipn'):
            _logger.warning(
                'Received a notification from bKash using sandbox'
            ),

        # TODO: txn_id: shoudl be false at draft, set afterwards, and verified with txn details
        if self.acquirer_reference and data.get('txn_id') != self.acquirer_reference:
            invalid_parameters.append(('txn_id', data.get('txn_id'), self.acquirer_reference))
        # check what is buyed
        if float_compare(float(data.get('mc_gross', '0.0')), (self.amount + self.fees), 2) != 0:
            invalid_parameters.append(('mc_gross', data.get('mc_gross'), '%.2f' % self.amount))  # mc_gross is amount + fees
        if data.get('mc_currency') != self.currency_id.name:
            invalid_parameters.append(('mc_currency', data.get('mc_currency'), self.currency_id.name))
        if 'handling_amount' in data and float_compare(float(data.get('handling_amount')), self.fees, 2) != 0:
            invalid_parameters.append(('handling_amount', data.get('handling_amount'), self.fees))
        # check buyer
        if self.payment_token_id and data.get('payer_id') != self.payment_token_id.acquirer_ref:
            invalid_parameters.append(('payer_id', data.get('payer_id'), self.payment_token_id.acquirer_ref))
        # check seller
        if data.get('receiver_id') and self.acquirer_id.bkash_seller_account and data['receiver_id'] != self.acquirer_id.bkash_seller_account:
            invalid_parameters.append(('receiver_id', data.get('receiver_id'), self.acquirer_id.bkash_seller_account))
        if not data.get('receiver_id') or not self.acquirer_id.bkash_seller_account:
            # Check receiver_email only if receiver_id was not checked.
            # In bKash, this is possible to configure as receiver_email a different email than the business email (the login email)
            # In Eagle, there is only one field for the bKash email: the business email. This isn't possible to set a receiver_email
            # different than the business email. Therefore, if you want such a configuration in your bKash, you are then obliged to fill
            # the Merchant ID in the bKash payment acquirer in Eagle, so the check is performed on this variable instead of the receiver_email.
            # At least one of the two checks must be done, to avoid fraudsters.
            if data.get('receiver_email') != self.acquirer_id.bkash_email_account:
                invalid_parameters.append(('receiver_email', data.get('receiver_email'), self.acquirer_id.bkash_email_account))

        return invalid_parameters


    def _bkash_form_validate(self, data):
        status = data.get('payment_status')
        res = {
            'acquirer_reference': data.get('txn_id'),
            'bkash_txn_type': data.get('payment_type'),
        }
        if status in ['Completed', 'Processed']:
            _logger.info('Validated bKash payment for tx %s: set as done' % (self.reference))
            try:
                # dateutil and pytz don't recognize abbreviations PDT/PST
                tzinfos = {
                    'PST': -8 * 3600,
                    'PDT': -7 * 3600,
                }
                date = dateutil.parser.parse(data.get('payment_date'), tzinfos=tzinfos).astimezone(pytz.utc)
            except:
                date = fields.Datetime.now()
            res.update(date=date)
            self._set_transaction_done()
            return self.write(res)
        elif status in ['Pending', 'Expired']:
            _logger.info('Received notification for bKash payment %s: set as pending' % (self.reference))
            res.update(state_message=data.get('pending_reason', ''))
            self._set_transaction_pending()
            return self.write(res)
        else:
            error = 'Received unrecognized status for bKash payment %s: %s, set as error' % (self.reference, status)
            _logger.info(error)
            res.update(state_message=error)
            self._set_transaction_cancel()
            return self.write(res)
