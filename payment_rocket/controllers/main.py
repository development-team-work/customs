# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from eagle import http
from eagle.http import request

_logger = logging.getLogger(__name__)


class RocketController(http.Controller):
    _notify_url = '/payment/rocket/init/'
    _return_url = '/payment/rocket/'
    _cancel_url = '/payment/rocket/'

    @http.route([
        '/payment/rocket/info',
    ], type='http', auth='none', csrf=False)
    def rocket_form_feedback(self, **post):
        _logger.info('Beginning form_feedback with post data %s', pprint.pformat(post))  # debug
        request.env['payment.transaction'].sudo().form_feedback(post, 'rocket')
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/payment/rocket/init/', auth='public')
    def index(self, **kw):
        return http.request.render('payment_rocket.rocket_form', {
            'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
        })