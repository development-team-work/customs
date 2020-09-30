# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import http, _

class Ribbon(http.Controller):

    @http.route('/ribbon_response/', auth='public', website=True)
    def rebbon_response(self, **kw):
        person=http.request.env[kw['model']].search([('id','=',int(kw['id']))])
        return http.request.render('ribbon.ajax_response', {
            'person': person
        })


    @http.route('/ribbon/<model("res.partner"):person>/', auth='public', website=True)
    def ribbon_model(self, person):
        forces=http.request.env['ribbon.force'].search([('id','>',0)])
        posts=http.request.env['ribbon.post'].search([('id','>',0)])
        units=http.request.env['ribbon.force.unit'].search([('id','>',0)])
        ranks=http.request.env['ribbon.rank'].search([('id','>',0)])
        return http.request.render('ribbon.ribbon_personel', {
            'posts': posts,
            'person': person,
            'units': units,
            'ranks': ranks,
            'forces': forces,
        })