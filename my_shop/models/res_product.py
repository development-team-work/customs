# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from eagle import _,fields, models,api

class productBook(models.Model):
    _inherit = 'product.template'
    is_book=fields.Boolean("Is A Book",default=False)
    publisher_id=fields.Many2one("res.partner",string="Publisher")
    writer_ids=fields.Many2many("res.partner",'res_partner_product_template_rel','book_ids','writer_ids',string="Writer")
    prefix = fields.Char("Prefix")
    suffix = fields.Char("Suffix")

class product_product(models.Model):
    _inherit = "product.product"
    pricelist_item_ids = fields.One2many(
        'product.pricelist.item','product_id',string='Pricelist Items')
    product_price_list_item_count = fields.Integer(
        '# Pricelist', compute='_compute_product_pricelist_items_count')


    @api.multi

    def _compute_product_pricelist_items_count(self):
        self.product_price_list_item_count = len(self.with_prefetch().pricelist_item_ids)


