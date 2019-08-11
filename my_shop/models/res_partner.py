# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from eagle import _,fields, models,api

class res_partner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(index=True, translate=True)
    is_writer=fields.Boolean("Is a Writer",default=False)
    is_publisher=fields.Boolean("Is a Publisher",default=False)
    # book_ids=fields.Many2many('product.template',string="Books")
    published=fields.One2many('product.template','publisher_id',string="Publications")
    written=fields.Many2many('product.template','writer_ids',string="Written Books")
