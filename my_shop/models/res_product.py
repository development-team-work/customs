# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from eagle import _,fields, models,api

class productBook(models.Model):
    _inherit = 'product.template'
    is_book=fields.Boolean("Is A Book",default=False)
    writer_ids=fields.Many2many("res.partner",'written',string="Writer")
    publisher_id=fields.Many2one("res.partner",string="Publisher")




