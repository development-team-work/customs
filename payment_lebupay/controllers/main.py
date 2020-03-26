# -*- coding: utf-8 -*-

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class LebupayController(http.Controller):
    
    _return_url = '/payment/lebupay/return'
    _cancel_url = '/payment/lebupay/cancel'
    _exception_url = '/payment/lebupay/error'
    _reject_url = '/payment/lebupay/reject'

    @http.route([
        '/payment/lebupay/return',
        '/payment/lebupay/cancel',
        '/payment/lebupay/error',
        '/payment/lebupay/reject',
    ], type='http', auth='none', csrf=False)
    def lebupay_return(self, **post):
        """ Lebupay."""
        _logger.info('Lebupay: entering form_feedback with post data %s', pprint.pformat(post))  # debug
        request.env['payment.transaction'].sudo().form_feedback(post, 'lebupay')
        post = {key.upper(): value for key, value in post.items()}
        return_url = post.get('ADD_RETURNDATA') or '/'
        return werkzeug.utils.redirect(return_url)


    @http.route('/page/paymentsuccess', auth='public', website=True)
    def paymentsuccess(self, **kw):
        return http.request.render('payment_lebupay.paymentsuccess', {
            'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
        })

    @http.route('/page/paymentfailure', auth='public', website=True)
    def paymentfailure(self, **kw):
        return http.request.render('payment_lebupay.paymentfailure', {
            'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
        })