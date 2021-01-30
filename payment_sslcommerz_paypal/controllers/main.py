# -*- coding: utf-8 -*-

import json
import logging
import pprint

import requests
import werkzeug
from werkzeug import urls

from odoo import http
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class SSLCommerzController(http.Controller):
    _notify_url = '/payment/sslcommerz/ipn/'
    _return_url = '/payment/sslcommerz/dpn/'
    _cancel_url = '/payment/sslcommerz/cancel/'

    def _parse_pdt_response(self, response):
        """ Parse a text response for a PDT verification.

            :param str response: text response, structured in the following way:
                STATUS\nkey1=value1\nkey2=value2...\n
             or STATUS\nError message...\n
            :rtype tuple(str, dict)
            :return: tuple containing the STATUS str and the key/value pairs
                     parsed as a dict
        """
        lines = [line for line in response.split('\n') if line]
        status = lines.pop(0)

        pdt_post = {}
        for line in lines:
            split = line.split('=', 1)
            if len(split) == 2:
                pdt_post[split[0]] = urls.url_unquote_plus(split[1])
            else:
                _logger.warning('SSL Commerz: error processing pdt response: %s', line)

        return status, pdt_post

    def sslcommerz_validate_data(self, **post):
        """ SSL Commerz IPN: three steps validation to ensure data correctness

         - step 1: return an empty HTTP 200 response -> will be done at the end
           by returning ''
         - step 2: POST the complete, unaltered message back to SSL Commerz (preceded
           by cmd=_notify-validate or _notify-synch for PDT), with same encoding
         - step 3: sslcommerz send either VERIFIED or INVALID (single word) for IPN
                   or SUCCESS or FAIL (+ data) for PDT

        Once data is validated, process it. """
        res = False
        post['cmd'] = '_notify-validate'
        reference = post.get('item_number')
        tx = None
        if reference:
            tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        if not tx:
            # we have seemingly received a notification for a payment that did not come from
            # odoo, acknowledge it otherwise sslcommerz will keep trying
            _logger.warning('received notification for unknown payment reference')
            return False
        sslcommerz_url = tx.acquirer_id.sslcommerz_get_form_action_url()
        pdt_request = bool(post.get('amt'))  # check for specific pdt param
        if pdt_request:
            # this means we are in PDT instead of DPN like before
            # fetch the PDT token
            post['at'] = tx and tx.acquirer_id.sslcommerz_pdt_token or ''
            post['cmd'] = '_notify-synch'  # command is different in PDT than IPN/DPN
        urequest = requests.post(sslcommerz_url, post)
        urequest.raise_for_status()
        resp = urequest.text
        if pdt_request:
            resp, post = self._parse_pdt_response(resp)
        if resp in ['VERIFIED', 'SUCCESS']:
            _logger.info('SSL Commerz: validated data')
            res = request.env['payment.transaction'].sudo().form_feedback(post, 'sslcommerz')
            if not res and tx:
                tx._set_transaction_error('Validation error occured. Please contact your administrator.')
        elif resp in ['INVALID', 'FAIL']:
            _logger.warning('SSL Commerz: answered INVALID/FAIL on data verification')
            if tx:
                tx._set_transaction_error('Invalid response from SSL Commerz. Please contact your administrator.')
        else:
            _logger.warning('SSL Commerz: unrecognized sslcommerz answer, received %s instead of VERIFIED/SUCCESS or INVALID/FAIL (validation: %s)' % (resp, 'PDT' if pdt_request else 'IPN/DPN'))
            if tx:
                tx._set_transaction_error('Unrecognized error from SSL Commerz. Please contact your administrator.')
        return res

    @http.route('/payment/sslcommerz/ipn/', type='http', auth='public', methods=['POST'], csrf=False)
    def sslcommerz_ipn(self, **post):
        """ SSL Commerz IPN. """
        _logger.info('Beginning SSL Commerz IPN form_feedback with post data %s', pprint.pformat(post))  # debug
        try:
            self.sslcommerz_validate_data(**post)
        except ValidationError:
            _logger.exception('Unable to validate the SSL Commerz payment')
        return ''

    @http.route('/payment/sslcommerz/dpn', type='http', auth="public", methods=['POST', 'GET'], csrf=False)
    def sslcommerz_dpn(self, **post):
        """ SSL Commerz DPN """
        _logger.info('Beginning SSL Commerz DPN form_feedback with post data %s', pprint.pformat(post))  # debug
        try:
            res = self.sslcommerz_validate_data(**post)
        except ValidationError:
            _logger.exception('Unable to validate the SSL Commerz payment')
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/payment/sslcommerz/cancel', type='http', auth="public", csrf=False)
    def sslcommerz_cancel(self, **post):
        """ When the user cancels its SSL Commerz payment: GET on this route """
        _logger.info('Beginning SSL Commerz cancel with post data %s', pprint.pformat(post))  # debug
        return werkzeug.utils.redirect('/payment/process')
