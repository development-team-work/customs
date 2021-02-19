# -*- coding: utf-8 -*-
from odoo import http

# class Dsblsc(http.Controller):
#     @http.route('/dsblsc/dsblsc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dsblsc/dsblsc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dsblsc.listing', {
#             'root': '/dsblsc/dsblsc',
#             'objects': http.request.env['dsblsc.dsblsc'].search([]),
#         })

#     @http.route('/dsblsc/dsblsc/objects/<model("dsblsc.dsblsc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dsblsc.object', {
#             'object': obj
#         })