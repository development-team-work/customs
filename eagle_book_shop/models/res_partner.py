# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.osv.expression import get_unaccent_wrapper
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'
    is_writer = fields.Boolean("Is a Writer", default=False)
    is_publisher = fields.Boolean("Is a Publisher", default=False)
    book_ids = fields.Many2many('product.template', string="Books")
    written_books = fields.Many2many('product.template', 'writer_book_rel', 'writer_ids', 'written_books',string="Written Books")
    published_books=fields.Many2many('product.template', 'publisher_book_rel', 'publisher_ids', 'published_books',string="Published Books")

    @api.onchange("is_writer")
    def create_related_ecommerce_category_writer(self):
        # todo create a ecommerce category for the writer
        if self.is_writer:
            ecom_categ=self.env['product.public.category'].search([('related_writer_id','=',self._origin.id )])
            if len(ecom_categ)==0:
                ecom_categ.create({'name':self.name,'related_writer_id':self._origin.id})


    @api.onchange("is_publisher")
    def create_related_ecommerce_category_publisher(self):
        if self.is_publisher:
            ecom_categ = self.env['product.public.category'].search([('related_publisher_id', '=', self._origin.id)])
            if len(ecom_categ) == 0:
                ecom_categ.create({'name': self.name, 'related_publisher_id': self._origin.id})