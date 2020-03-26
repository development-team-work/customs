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


class bKashController(http.Controller):
    _notify_url = '/payment/bkash/' #'/payment/paypal/ipn/'
    _return_url = '/payment/bkash/dpn/'
    _cancel_url = '/payment/bkash/cancel/'

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
                _logger.warning('bKash: error processing pdt response: %s', line)

        return status, pdt_post

    def bkash_validate_data(self, **post):
        """ bKash IPN: three steps validation to ensure data correctness

         - step 1: return an empty HTTP 200 response -> will be done at the end
           by returning ''
         - step 2: POST the complete, unaltered message back to bKash (preceded
           by cmd=_notify-validate or _notify-synch for PDT), with same encoding
         - step 3: bkash send either VERIFIED or INVALID (single word) for IPN
                   or SUCCESS or FAIL (+ data) for PDT

        Once data is validated, process it. """
        res = False
        post['cmd'] = '_notify-validate'
        reference = post.get('item_number')
        tx = None
        if reference:
            tx = request.env['payment.transaction'].search([('reference', '=', reference)])
        bkash_urls = request.env['payment.acquirer']._get_bkash_urls(tx and tx.acquirer_id.environment or 'prod')
        pdt_request = bool(post.get('amt'))  # check for spefific pdt param
        if pdt_request:
            # this means we are in PDT instead of DPN like before
            # fetch the PDT token
            post['at'] = tx and tx.acquirer_id.bkash_pdt_token or ''
            post['cmd'] = '_notify-synch'  # command is different in PDT than IPN/DPN
        validate_url = bkash_urls['bkash_form_url']
        urequest = requests.post(validate_url, post)
        urequest.raise_for_status()
        resp = urequest.text
        if pdt_request:
            resp, post = self._parse_pdt_response(resp)
        if resp in ['VERIFIED', 'SUCCESS']:
            _logger.info('bKash: validated data')
            res = request.env['payment.transaction'].sudo().form_feedback(post, 'bkash')
            if not res:
                tx.sudo()._set_transaction_error('Validation error occured. Please contact your administrator.')
        elif resp in ['INVALID', 'FAIL']:
            _logger.warning('bKash: answered INVALID/FAIL on data verification')
            tx.sudo()._set_transaction_error('Invalid response from bKash. Please contact your administrator.')
        else:
            _logger.warning('bKash: unrecognized bkash answer, received %s instead of VERIFIED/SUCCESS or INVALID/FAIL (validation: %s)' % (resp, 'PDT' if pdt_request else 'IPN/DPN'))
            tx.sudo()._set_transaction_error('Unrecognized error from bKash. Please contact your administrator.')
        return res



    @http.route('/payment/bkash/', type='http', auth='public', csrf=False)
    def bkash_init(self, **post):
        """ bKash IPN. """
        _logger.info('Beginning bKash IPN form_feedback with post data %s', pprint.pformat(post))  # debug
        try:
            self.bkash_validate_data(**post)
        except ValidationError:
            _logger.exception('Unable to validate the bKash payment')
        return http.request.render('payment_bkash.bkash_form',post)

    @http.route('/payment/bkash/dpn', type='http', auth="none", methods=['POST', 'GET'], csrf=False)
    def bkash_dpn(self, **post):
        """ bKash DPN """
        _logger.info('Beginning bKash DPN form_feedback with post data %s', pprint.pformat(post))  # debug
        try:
            res = self.bkash_validate_data(**post)
        except ValidationError:
            _logger.exception('Unable to validate the bKash payment')
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/payment/bkash/cancel', type='http', auth="none", csrf=False)
    def bkash_cancel(self, **post):
        """ When the user cancels its bKash payment: GET on this route """
        _logger.info('Beginning bKash cancel with post data %s', pprint.pformat(post))  # debug
        return werkzeug.utils.redirect('/payment/process')
